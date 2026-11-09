from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "provider_views_catalog", ROOT / "tools" / "provider_views_catalog.py"
)
assert SPEC is not None and SPEC.loader is not None
catalog_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog_tool)


class ProviderViewsCatalogTests(unittest.TestCase):
    def test_catalog_is_complete_and_cross_references_resolve(self) -> None:
        catalog = catalog_tool.load_and_validate()

        self.assertEqual(7, len(catalog["surfaces"]))
        self.assertEqual(12, len(catalog["binding_sources"]))
        self.assertEqual(30, len(catalog["components"]))
        self.assertEqual(7, len(catalog["reference_corpus"]["examples"]))
        self.assertFalse(catalog["reference_corpus"]["normative_for_protocol"])
        self.assertEqual(
            catalog_tool.EXPECTED_COMPONENTS,
            {component["identifier"] for component in catalog["components"]},
        )

    def test_catalog_contains_no_maturity_or_renderer_status(self) -> None:
        catalog = catalog_tool.load_and_validate()

        serialized = json.dumps(catalog)
        for obsolete in ("catalog_status", "renderer_registry", "renderer-registry.json"):
            with self.subTest(obsolete=obsolete):
                self.assertNotIn(obsolete, serialized)
        self.assertNotIn('"status":', serialized)

    def test_catalog_provenance_uses_the_full_control_plane_version(self) -> None:
        catalog = catalog_tool.load_and_validate()

        self.assertEqual("0.1.0", catalog["control_plane_version"])
        self.assertNotIn("catalog_version", catalog)
        self.assertRegex(catalog["catalog_sha256"], re.compile(r"^[0-9a-f]{64}$"))
        catalog_content = {
            key: value
            for key, value in catalog.items()
            if key not in {"control_plane_version", "catalog_sha256"}
        }
        canonical = json.dumps(
            catalog_content,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(
            hashlib.sha256(canonical).hexdigest(), catalog["catalog_sha256"]
        )
        self.assertEqual(
            f"provider-views-catalog-{catalog['control_plane_version']}.json",
            catalog_tool.CATALOG_ARTIFACT.name,
        )

    def test_catalog_sources_do_not_declare_an_independent_version(self) -> None:
        for filename in (
            "binding-sources.json",
            "compatibility.json",
            "decisions.json",
            "reference-corpus.json",
            "surfaces.json",
        ):
            with self.subTest(filename=filename):
                document = catalog_tool.read_json(catalog_tool.CATALOG / filename)
                self.assertNotIn("catalog_version", document)

    def test_unresolved_design_choices_are_visible_as_proposals(self) -> None:
        catalog = catalog_tool.load_and_validate()

        self.assertEqual(
            catalog_tool.EXPECTED_DECISIONS,
            {decision["id"] for decision in catalog["decisions"]},
        )

    def test_versioned_component_meanings_have_a_compatibility_baseline(self) -> None:
        catalog = catalog_tool.load_and_validate()

        baseline = catalog["compatibility"]["initial_meaning_baseline"]
        self.assertEqual(
            catalog_tool.EXPECTED_COMPONENTS,
            {component["identifier"] for component in baseline},
        )
        self.assertIn(
            "new major identifier", catalog["compatibility"]["policy"]["meaning_change"]
        )

    def test_generated_docs_and_provider_artifact_are_reproducible(self) -> None:
        outputs = catalog_tool.expected_outputs(catalog_tool.load_and_validate())

        for path, expected in outputs.items():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.exists())
                self.assertEqual(expected, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
