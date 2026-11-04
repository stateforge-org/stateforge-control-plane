#!/usr/bin/env python3
"""Validate and compile the Control Plane-owned Provider Views catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "provider_views" / "catalog" / "v1"
COMPONENTS = CATALOG / "components"
GENERATED = CATALOG / "generated"
DOCS = ROOT / "docs" / "provider-views-catalog.md"

EXPECTED_COMPONENTS = {
    "stateforge.ui/layout.stack@1",
    "stateforge.ui/layout.grid@1",
    "stateforge.ui/layout.section@1",
    "stateforge.ui/layout.tabs@1",
    "stateforge.ui/layout.steps@1",
    "stateforge.ui/input.form@1",
    "stateforge.ui/input.field@1",
    "stateforge.ui/input.object@1",
    "stateforge.ui/input.array@1",
    "stateforge.ui/input.key_value@1",
    "stateforge.ui/input.code@1",
    "stateforge.ui/input.secret@1",
    "stateforge.ui/content.text@1",
    "stateforge.ui/content.markdown@1",
    "stateforge.ui/data.key_value@1",
    "stateforge.ui/data.table@1",
    "stateforge.ui/data.tree@1",
    "stateforge.ui/data.code@1",
    "stateforge.ui/data.diff@1",
    "stateforge.ui/data.log@1",
    "stateforge.ui/status.badge@1",
    "stateforge.ui/status.progress@1",
    "stateforge.ui/status.timeline@1",
    "stateforge.ui/data.metric@1",
    "stateforge.ui/data.chart@1",
    "stateforge.ui/data.topology@1",
    "stateforge.ui/data.artifacts@1",
    "stateforge.ui/media.image@1",
    "stateforge.ui/action.operation_submit@1",
    "stateforge.ui/action.operation_cancel@1",
}
EXPECTED_DECISIONS = {
    "binding-sources",
    "conditions-and-repetition",
    "component-property-schemas",
    "evidence-surface",
    "host-actions",
    "reference-corpus",
}
EXPECTED_SURFACES = {
    "stateforge.ui/surface.provider.overview@1",
    "stateforge.ui/surface.operation.request@1",
    "stateforge.ui/surface.operation.run@1",
    "stateforge.ui/surface.operation.result@1",
    "stateforge.ui/surface.trigger.policy@1",
    "stateforge.ui/surface.trigger.event@1",
    "stateforge.ui/surface.evidence@1",
}
EXPECTED_BINDING_SOURCES = {
    "provider.descriptor@1",
    "provider.health@1",
    "provider.statistics@1",
    "provider.capabilities@1",
    "operation.input_schema@1",
    "operation.request_context@1",
    "operation.run@1",
    "operation.result@1",
    "trigger.declaration@1",
    "trigger.policy@1",
    "trigger.event@1",
    "evidence.record@1",
}
SCHEMA_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
}
SCHEMA_KEYWORDS = {
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "minimum",
    "maximum",
    "maxLength",
    "minItems",
    "maxItems",
    "enum",
}
ALLOWED_ASSET_MEDIA_TYPES = {"image/png", "image/svg+xml"}


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path.relative_to(ROOT)}: {exc}") from None


def _schema_errors(value: Any, schema: dict[str, Any], at: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type in SCHEMA_TYPES:
        py_type = SCHEMA_TYPES[expected_type]
        if expected_type == "integer":
            valid = isinstance(value, int) and not isinstance(value, bool)
        elif expected_type == "number":
            valid = isinstance(value, (int, float)) and not isinstance(value, bool)
        else:
            valid = isinstance(value, py_type)
        if not valid:
            return [f"{at}: expected {expected_type}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{at}: value is outside enum")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{at}: below minimum")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{at}: above maximum")
    if isinstance(value, str):
        if len(value) > schema.get("maxLength", len(value)):
            errors.append(f"{at}: exceeds maxLength")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{at}: below minItems")
        if len(value) > schema.get("maxItems", len(value)):
            errors.append(f"{at}: exceeds maxItems")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(_schema_errors(item, item_schema, f"{at}[{index}]"))
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{at}: missing required property {required}")
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{at}: unknown property {key}")
        for key, item in value.items():
            if key in properties:
                errors.extend(
                    _schema_errors(item, properties[key], f"{at}.{key}")
                )
    return errors


def _schema_definition_errors(schema: dict[str, Any], at: str) -> list[str]:
    errors: list[str] = []
    unknown = set(schema) - SCHEMA_KEYWORDS
    if unknown:
        errors.append(f"{at}: unsupported schema keywords {sorted(unknown)}")
    schema_type = schema.get("type")
    if schema_type not in SCHEMA_TYPES:
        errors.append(f"{at}: unsupported or missing JSON Schema type")
    properties = schema.get("properties", {})
    if schema_type != "object" and properties:
        errors.append(f"{at}: only object schemas may define properties")
    if schema_type == "array" and not isinstance(schema.get("items"), dict):
        errors.append(f"{at}: array schema must define items")
    for required in schema.get("required", []):
        if required not in properties:
            errors.append(f"{at}: required property {required} is not defined")
    for key, child in properties.items():
        errors.extend(_schema_definition_errors(child, f"{at}.{key}"))
    if isinstance(schema.get("items"), dict):
        errors.extend(_schema_definition_errors(schema["items"], f"{at}[]"))
    if "enum" in schema and not isinstance(schema["enum"], list):
        errors.append(f"{at}: enum must be an array")
    if schema_type == "string" and not {"maxLength", "enum"}.intersection(schema):
        errors.append(f"{at}: string properties must be bounded")
    if schema_type == "array" and "maxItems" not in schema:
        errors.append(f"{at}: array properties must be bounded")
    return errors


def load_and_validate() -> dict[str, Any]:
    surfaces_doc = read_json(CATALOG / "surfaces.json")
    sources_doc = read_json(CATALOG / "binding-sources.json")
    decisions_doc = read_json(CATALOG / "decisions.json")
    compatibility_doc = read_json(CATALOG / "compatibility.json")
    reference_corpus_doc = read_json(CATALOG / "reference-corpus.json")
    registry = read_json(CATALOG / "renderer-registry.json")
    surfaces = {item["identifier"]: item for item in surfaces_doc["surfaces"]}
    sources = {item["identifier"]: item for item in sources_doc["sources"]}
    errors: list[str] = []

    if len(surfaces) != len(surfaces_doc["surfaces"]):
        errors.append("surface identifiers must be unique")
    if len(sources) != len(sources_doc["sources"]):
        errors.append("binding source identifiers must be unique")
    if set(surfaces) != EXPECTED_SURFACES:
        errors.append("surface inventory does not match the seven catalog surfaces")
    if set(sources) != EXPECTED_BINDING_SOURCES:
        errors.append("binding-source inventory does not match the proposed contract")
    for source in sources.values():
        if not source["surfaces"]:
            errors.append(f"binding source {source['identifier']} has no surface")
        for surface in source["surfaces"]:
            if surface not in surfaces:
                errors.append(
                    f"binding source {source['identifier']} references unknown "
                    f"surface {surface}"
                )
            elif source["identifier"] not in surfaces[surface]["bindings"]:
                errors.append(
                    f"surface {surface} does not list source {source['identifier']}"
                )

    component_files = sorted(COMPONENTS.glob("*.json"))
    components = [read_json(path) for path in component_files]
    by_id = {item["identifier"]: item for item in components}
    if len(by_id) != len(components):
        errors.append("component identifiers must be unique")
    actual_ids = set(by_id)
    if actual_ids != EXPECTED_COMPONENTS:
        errors.append(
            f"component inventory mismatch; missing={sorted(EXPECTED_COMPONENTS - actual_ids)}, "
            f"unexpected={sorted(actual_ids - EXPECTED_COMPONENTS)}"
        )
    if len(components) != 30:
        errors.append(f"expected 30 component files, found {len(components)}")
    if reference_corpus_doc.get("normative_for_protocol") is not False:
        errors.append("Control Plane reference corpus must not become Protocol conformance")
    if len(reference_corpus_doc.get("examples", [])) != 7:
        errors.append("reference corpus must retain the seven catalog workloads")

    meanings = {
        item["identifier"]: item["meaning"]
        for item in compatibility_doc["initial_meaning_baseline"]
    }
    if set(meanings) != EXPECTED_COMPONENTS:
        errors.append("compatibility meaning baseline does not cover all core identifiers")
    for identifier, component in by_id.items():
        if not re.search(r"@[1-9][0-9]*$", identifier):
            errors.append(f"{identifier}: component identifier must end in a positive major version")
        if identifier in meanings and component.get("purpose") != meanings[identifier]:
            errors.append(
                f"{identifier}: meaning changed; introduce a new major identifier "
                "and retain the old descriptor"
            )

    for component in components:
        identifier = component.get("identifier", "<missing identifier>")
        applicable = component.get("applicable_surfaces", [])
        if not applicable:
            errors.append(f"{identifier}: no applicable surfaces")
        for surface in applicable:
            if surface not in surfaces:
                errors.append(f"{identifier}: unknown surface {surface}")
        schema = component.get("properties_schema")
        if not isinstance(schema, dict) or schema.get("type") != "object":
            errors.append(f"{identifier}: properties_schema must describe an object")
        else:
            errors.extend(_schema_definition_errors(schema, f"{identifier}.properties"))
            if schema.get("additionalProperties") is not False:
                errors.append(f"{identifier}: property schema must be closed")
        example = component.get("example", {})
        errors.extend(
            _schema_errors(
                example.get("properties", {}),
                schema or {},
                f"{identifier}.example.properties",
            )
        )
        slots = {slot.get("name"): slot for slot in component.get("binding_slots", [])}
        if len(slots) != len(component.get("binding_slots", [])):
            errors.append(f"{identifier}: duplicate binding slot")
        for slot in slots.values():
            slot_sources = slot.get("sources", [])
            if not slot_sources:
                errors.append(f"{identifier}: slot {slot['name']} has no sources")
            for source_id in slot_sources:
                if source_id not in sources:
                    errors.append(
                        f"{identifier}: slot {slot['name']} references unknown source "
                        f"{source_id}"
                    )
                elif not any(
                    surface in applicable for surface in sources[source_id]["surfaces"]
                ):
                    errors.append(
                        f"{identifier}: source {source_id} is unavailable on all "
                        "applicable surfaces"
                    )
        example_bindings = example.get("bindings", {})
        if set(example_bindings) != set(slots):
            errors.append(f"{identifier}: example must demonstrate every binding slot")
        for slot_name, binding in example_bindings.items():
            slot = slots.get(slot_name)
            if slot is None:
                errors.append(f"{identifier}: example uses undeclared slot {slot_name}")
                continue
            source_id = binding.get("source_identifier")
            if source_id not in slot["sources"]:
                errors.append(
                    f"{identifier}: example source {source_id} is not allowed in "
                    f"slot {slot_name}"
                )
            if not isinstance(binding.get("pointer"), str):
                errors.append(f"{identifier}: example binding pointer must be a string")
            elif source_id in sources and not any(
                surface in applicable for surface in sources[source_id]["surfaces"]
            ):
                errors.append(
                    f"{identifier}: example source {source_id} is unavailable on "
                    "all applicable surfaces"
                )
        for slot in component.get("asset_slots", []):
            if not slot.get("media_types"):
                errors.append(f"{identifier}: asset slot {slot['name']} has no media types")
            if set(slot.get("media_types", [])) - ALLOWED_ASSET_MEDIA_TYPES:
                errors.append(f"{identifier}: asset slot {slot['name']} has unsupported media type")
        fallback_ids = component["fallback_guidance"][
            "recommended_core_components"
        ]
        if any(target not in by_id for target in fallback_ids):
            errors.append(f"{identifier}: fallback references unknown core component")
        if component.get("catalog_status") != "proposed":
            errors.append(f"{identifier}: expected proposed status pending catalog review")
        child_rule = component.get("children", {})
        if child_rule.get("allowed"):
            families = set(child_rule.get("allowed_component_families", []))
            if not families or not families <= {
                "layout", "input", "content", "data", "status", "media", "action"
            }:
                errors.append(f"{identifier}: invalid child component families")
            for family in families:
                if not any(
                    item_id.startswith(f"stateforge.ui/{family}.")
                    for item_id in by_id
                ):
                    errors.append(f"{identifier}: child family {family} has no catalog entries")
            matched_property = child_rule.get("child_count_matches_property")
            if matched_property and matched_property not in schema.get("properties", {}):
                errors.append(f"{identifier}: child-count property is not declared")
        elif child_rule.get("maximum_per_node") != 0:
            errors.append(f"{identifier}: leaf component must have zero child capacity")

    for example in reference_corpus_doc.get("examples", []):
        if not example.get("identifiers"):
            errors.append(f"{example.get('provider', '<unknown>')}: corpus identifiers are missing")
        for component_id in example.get("component_identifiers", []):
            if component_id not in by_id:
                errors.append(
                    f"{example.get('provider', '<unknown>')}: corpus references unknown "
                    f"component {component_id}"
                )

    decision_ids = {decision["id"] for decision in decisions_doc["decisions"]}
    if decision_ids != EXPECTED_DECISIONS or decisions_doc.get("status") != "proposed":
        errors.append("the six unresolved PDF decisions must remain explicitly proposed")
    supported = registry.get("supported_component_identifiers", [])
    if any(identifier not in by_id for identifier in supported):
        errors.append("renderer registry references a component outside the catalog")
    if registry.get("status") == "not_implemented" and supported:
        errors.append("not_implemented renderer registry cannot claim support")
    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))
    registry_artifact = dict(registry)
    registry_artifact["unsupported_component_identifiers"] = sorted(
        actual_ids - set(supported)
    )
    return {
        "catalog_version": 1,
        "ownership": "stateforge-control-plane",
        "status": "proposed",
        "surfaces": surfaces_doc["surfaces"],
        "binding_sources": sources_doc["sources"],
        "components": sorted(components, key=lambda item: item["identifier"]),
        "decisions": decisions_doc["decisions"],
        "compatibility": compatibility_doc,
        "reference_corpus": reference_corpus_doc,
        "renderer_registry": registry_artifact,
    }


def render_reference(catalog: dict[str, Any]) -> str:
    lines = [
        "# Provider Views catalog",
        "",
        "> Status: proposed. The entries define Control Plane contracts; they do not assert that every renderer is implemented or enabled.",
        "",
        "The Control Plane owns this catalog. Provider tooling may consume the generated JSON; Protocol transports the generic presentation tree and does not own this component registry.",
        "",
        "## Surfaces",
        "",
        "| Surface | Purpose | Binding sources |",
        "| --- | --- | --- |",
    ]
    for surface in catalog["surfaces"]:
        lines.append(
            f"| `{surface['identifier']}` | {surface['purpose']} | "
            f"{', '.join(f'`{item}`' for item in surface['bindings'])} |"
        )
    lines.extend(
        [
            "",
            "## Renderer availability",
            "",
            f"Registry status: `{catalog['renderer_registry']['status']}`. "
            f"Currently registered: {len(catalog['renderer_registry']['supported_component_identifiers'])}; "
            f"catalog entries without a renderer: {len(catalog['renderer_registry']['unsupported_component_identifiers'])}.",
            "",
            "Catalog membership alone never makes a renderer available. The Control Plane build must register and verify an implementation before advertising support.",
            "",
            "## Core components",
            "",
            "| Component | Purpose | Surfaces | Binding slots |",
            "| --- | --- | --- | --- |",
        ]
    )
    for component in catalog["components"]:
        lines.append(
            f"| `{component['identifier']}` | {component['purpose']} | "
            f"{', '.join(f'`{item}`' for item in component['applicable_surfaces'])} | "
            f"{', '.join(f'`{item['name']}`' for item in component['binding_slots']) or 'None'} |"
        )
    for component in catalog["components"]:
        lines.extend(
            [
                "",
                f"### `{component['identifier']}`",
                "",
                component["purpose"],
                "",
                "Catalog status: proposed. Properties are presentation-only; operational schemas remain authoritative.",
                "",
                "**Properties**",
                "",
            ]
        )
        properties = component["properties_schema"].get("properties", {})
        if properties:
            lines.extend(["| Property | JSON Schema |", "| --- | --- |"])
            for name, schema in properties.items():
                lines.append(
                    f"| `{name}` | `{json.dumps(schema, sort_keys=True, separators=(',', ':'))}` |"
                )
        else:
            lines.append("None.")
        lines.extend(["", "**Binding slots**", ""])
        if component["binding_slots"]:
            lines.extend(
                ["| Slot | Expected shape | Sources |", "| --- | --- | --- |"]
            )
            for slot in component["binding_slots"]:
                lines.append(
                    f"| `{slot['name']}` | {slot['data_shape']} | "
                    f"{', '.join(f'`{item}`' for item in slot['sources'])} |"
                )
        else:
            lines.append("None.")
        asset_slots = component["asset_slots"]
        lines.extend(["", "**Asset slots**", ""])
        if asset_slots:
            lines.extend(["| Slot | Permitted media types |", "| --- | --- |"])
            for slot in asset_slots:
                lines.append(
                    f"| `{slot['name']}` | "
                    f"{', '.join(f'`{item}`' for item in slot['media_types'])} |"
                )
        else:
            lines.append("None.")
        child_rule = component["children"]
        child_description = (
            f"Up to {child_rule['maximum_per_node']} children from "
            f"{', '.join(child_rule.get('allowed_component_families', []))}."
            if child_rule["allowed"]
            else "Leaf component; children are not allowed."
        )
        if child_rule.get("child_count_matches_property"):
            child_description += (
                " Child count must match property `"
                f"{child_rule['child_count_matches_property']}`."
            )
        lines.extend(
            [
                "",
                "**Children**",
                "",
                child_description,
                "",
                "**Fallback guidance**",
                "",
                "Provider may supply a complete core-component fallback. "
                "Recommended: "
                + (
                    ", ".join(
                        f"`{item}`"
                        for item in component["fallback_guidance"][
                            "recommended_core_components"
                        ]
                    )
                    or "none specified"
                )
                + ".",
                "",
                "**Example**",
                "",
                "```json",
                json.dumps(component["example"], ensure_ascii=False, indent=2),
                "```",
            ]
        )
    lines.extend(
        [
            "",
            "## Reference Provider corpus",
            "",
            "These seven cases are illustrative Control Plane design and renderer-test fixtures, not normative Protocol requirements.",
            "",
            "| Provider | Operation or trigger | Contract pressure |",
            "| --- | --- | --- |",
        ]
    )
    for example in catalog["reference_corpus"]["examples"]:
        lines.append(
            f"| {example['provider']} | {', '.join(f'`{item}`' for item in example['identifiers'])} | {example['contract_pressure']} |"
        )
    lines.extend(
        [
            "",
            "## Proposed decisions",
            "",
            "These defaults are explicit proposals pending product review. Operational schemas remain authoritative; component properties only affect presentation.",
            "",
        ]
    )
    lines.extend(f"- **{item['id']}**: {item['proposal']}" for item in catalog["decisions"])
    lines.extend(
        [
            "",
            "## Compatibility",
            "",
            "An existing versioned identifier keeps its meaning. Meaning changes and incompatible property, binding, surface, asset-slot, child, or fallback changes require a new major identifier; retain the old descriptor. The initial purpose baseline is in `catalog/v1/compatibility.json`.",
        ]
    )
    lines.append("")
    return "\n".join(lines)


def expected_outputs(catalog: dict[str, Any]) -> dict[Path, str]:
    return {
        GENERATED / "provider-views-catalog-v1.json": json.dumps(
            catalog, ensure_ascii=False, indent=2, sort_keys=True
        )
        + "\n",
        DOCS: render_reference(catalog),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated catalog artifacts are missing or stale",
    )
    args = parser.parse_args()
    try:
        catalog = load_and_validate()
        outputs = expected_outputs(catalog)
        if args.check:
            stale = [
                path.relative_to(ROOT).as_posix()
                for path, expected in outputs.items()
                if not path.exists() or path.read_text(encoding="utf-8") != expected
            ]
            if stale:
                raise ValueError(f"generated artifacts are stale: {', '.join(stale)}")
        else:
            for path, content in outputs.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    except (KeyError, TypeError, ValueError) as exc:
        print(f"Provider Views catalog validation failed:\n{exc}", file=sys.stderr)
        return 1
    print("Provider Views catalog valid: 7 surfaces, 12 binding sources, 30 components.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
