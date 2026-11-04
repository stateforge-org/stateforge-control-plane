# Provider Views Catalog

The Control Plane owns the machine-readable Provider Views catalog under
`catalog/v1/`. It describes component contracts; it does not mean a renderer
for every catalog entry is implemented or enabled.

Run `python3 tools/provider_views_catalog.py` to validate the source catalog and
regenerate the Provider-consumable artifact and reference page. Run
`python3 -m unittest discover -s tests` to verify catalog invariants and
generated-file reproducibility.

The property schemas and the six catalog-wide choices in
`catalog/v1/decisions.json` are proposed defaults derived from the MVP catalog
PDF. They are explicit so they can be reviewed and refined; they are not
silently treated as an SFP wire contract or as renderer availability.
