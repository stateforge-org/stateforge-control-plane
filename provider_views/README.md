# Provider Views Catalog

[Provider Views architecture](ARCHITECTURE.md) defines the intended
declarative authoring, translation, and Control Plane rendering boundaries.
It is an architecture contract, not a released authoring API.

The Control Plane owns the machine-readable Provider Views catalog under
`catalog/0.1.0/`, matching this Control Plane release. The catalog has no
independent version. Generated artifacts record the full Control Plane version
and a digest of the catalog content. A destructive catalog change requires a
Control Plane major-version bump. Every component contract in the catalog is
part of the Control Plane's rendering surface.

Run `python3 tools/provider_views_catalog.py` to validate the source catalog and
regenerate the Provider-consumable artifact and reference page. Run
`python3 -m unittest discover -s tests` to verify catalog invariants and
generated-file reproducibility.

The property schemas and the six catalog-wide choices in
`catalog/0.1.0/decisions.json` are explicit Control Plane UI contracts derived
from the MVP catalog PDF. They are not SFP wire contracts.
