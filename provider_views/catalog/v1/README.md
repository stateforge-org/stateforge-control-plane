# Catalog v1 source

This directory is the editable source for the Control Plane-owned Provider
Views catalog. Each core renderer registration has its own JSON file under
`components/`. Surface contracts, binding sources, proposed product decisions,
compatibility policy, and the non-normative workload corpus are kept as shared
documents beside those definitions.

Edit source files here. Do not edit `generated/provider-views-catalog-v1.json`
or `docs/provider-views-catalog.md` by hand; regenerate them with:

```sh
python3 tools/provider_views_catalog.py
```

Validate source references and ensure generated files are current with:

```sh
python3 tools/provider_views_catalog.py --check
python3 -m unittest discover -s tests
```

All six catalog-wide decisions and all per-component property contracts are
currently marked proposed. Review them before treating this baseline as a
stable Control Plane API. An identifier's meaning is preserved; incompatible
changes require a new major identifier while retaining the old contract.
