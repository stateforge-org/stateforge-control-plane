from __future__ import annotations

import importlib.util
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
        self.assertEqual(catalog_tool.EXPECTED_COMPONENTS, {
            component["identifier"] for component in catalog["components"]
        })

    def test_catalog_membership_does_not_imply_renderer_availability(self) -> None:
        catalog = catalog_tool.load_and_validate()

        self.assertEqual("not_implemented", catalog["renderer_registry"]["status"])
        self.assertEqual([], catalog["renderer_registry"]["supported_component_identifiers"])
        self.assertEqual(
            catalog_tool.EXPECTED_COMPONENTS,
            set(catalog["renderer_registry"]["unsupported_component_identifiers"]),
        )

    def test_unresolved_design_choices_are_visible_as_proposals(self) -> None:
        catalog = catalog_tool.load_and_validate()

        self.assertEqual("proposed", catalog["status"])
        self.assertEqual("proposed", catalog_tool.read_json(
            catalog_tool.CATALOG / "decisions.json"
        )["status"])
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
        self.assertIn("new major identifier", catalog["compatibility"]["policy"]["meaning_change"])

    def test_generated_docs_and_provider_artifact_are_reproducible(self) -> None:
        outputs = catalog_tool.expected_outputs(catalog_tool.load_and_validate())

        for path, expected in outputs.items():
            with self.subTest(path=path.relative_to(ROOT)):
                self.assertTrue(path.exists())
                self.assertEqual(expected, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
