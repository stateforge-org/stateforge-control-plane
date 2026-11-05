# StateForge Control Plane repository instructions

Read root `STATEFORGE_DPT.md` for milestone ownership and the generated
delivery snapshot. For milestone work, follow
`.agents/skills/stateforge-dpt-milestone/SKILL.md`. It applies equally to
agents reached through `AGENTS.md` or this file.

Use `stateforge-python-development` for Python, packaging, tests, and docs;
use `stateforge-pr-review` for PR preparation or review assistance. These
skills live under `.claude/skills/`.

## Ownership boundaries

- The Control Plane owns the Provider Views catalog, renderer registry,
  renderer extensions, Control Plane-versioned catalog snapshots,
  renderer-specific validation,
  and UI rendering.
- SFP owns the generic wire representation and context-independent protocol
  validation. Do not put Control Plane component catalogs, renderer schemas,
  or renderer-specific behavior into SFP.
- Provider Python owns Provider runtime behavior and its authoring API. The
  Control Plane catalog may generate authoring helpers, but those helpers do
  not make the Provider authoritative for renderer availability.
- Treat each catalog snapshot as part of the full Control Plane release
  version; do not assign the catalog an independent version. Preserve
  immutable snapshots while a Control Plane build accepts them. Destructive
  catalog changes require a Control Plane major-version bump. Component
  identifiers remain versioned contracts; use a new identifier version when
  old and new component contracts must coexist.
- Do not make Provider runtime fetch the catalog from the Control Plane.
  Generated artifacts and validation inputs must be reproducible and
  versioned.

## Delivery and verification

- Work only on the human-selected Issue and its mapped DPT step. Use the Issue
  acceptance criteria and DPT for ownership, prerequisites, and required
  result. Surface material disagreements rather than resolving them silently.
- Preserve the repository's configured Python, test, documentation, and
  frontend checks. Add or update behavioral tests for observable changes.
- Do not edit `STATEFORGE_DPT.md`, its manifest, revision, or statuses to
  report implementation progress. Plan management is a separate workflow.
- Humans own pushing, Issue/PR mutations, PR creation, formal review, and
  merging. Local commits do not complete a milestone. End with verification
  evidence and a human-readable PR draft.
