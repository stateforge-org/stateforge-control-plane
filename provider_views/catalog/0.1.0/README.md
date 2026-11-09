# Provider Views catalog for Control Plane 0.1.0

This directory is the editable source for the Control Plane-owned Provider
Views catalog. Each core component contract has its own JSON file under
`components/`. Surface contracts, binding sources, proposed product decisions,
compatibility policy, and the non-normative workload corpus are kept as shared
documents beside those definitions.

Edit source files here. Do not edit `generated/provider-views-catalog-0.1.0.json`
or `docs/provider-views-catalog.md` by hand; regenerate them with:

```sh
python3 tools/provider_views_catalog.py
```

Validate source references and ensure generated files are current with:

```sh
python3 tools/provider_views_catalog.py --check
python3 -m unittest discover -s tests
```

The catalog defines the component contracts available to this Control Plane
release. An identifier's meaning is preserved; incompatible changes require a
new major identifier while retaining the old contract.
