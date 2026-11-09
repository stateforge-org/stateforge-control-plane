# Provider Views architecture

This document defines the intended Provider Views contract for the first
Control Plane release. It is an architecture agreement, not a claim that the
authoring API or Control Plane renderers shown below already exist. The
machine-readable catalog in `catalog/0.1.0/` remains the authority for
component details. This document does not add or change a catalog entry.

## What a Provider declares

A Provider can attach a view to itself, an operation, or a trigger. A view
selects one **presentation surface** and provides a rooted tree of catalog
components. Layout components arrange children. Leaf components show data,
collect schema-governed input, indicate status, or request a host-controlled
action. Each component has catalog-defined properties, named binding slots,
asset slots, and child rules. A binding identifies a Control Plane-owned data
source and, optionally, a JSON Pointer into it. The Provider does not supply
the value of that source merely by declaring the binding.

The composition model is inspired by SwiftUI's readable nesting and reusable
declarations. It is not an embedded web application or a way to run Provider
code in the browser. Authors may choose component order, layout, labels,
supported conditions and repetition, and approved visual assets. The Control
Plane decides how each component is actually drawn and interacted with.

The seven surfaces in the 0.1.0 catalog cover Provider Overview; operation
request, run, and result; trigger policy and event; and evidence. A Provider
view may omit optional surfaces. An omitted or rejected view falls back to the
Control Plane's generic schema-driven presentation. It never removes the
underlying operation or trigger.

### Intended authoring shape

This example records the proposed high-level authoring experience. The
`views.view`, `views.bind`, `provider_view`, and `run_view` integration points
are **not yet shipped APIs**. The generated component factories are a lower
level building block; Provider Python is responsible for the ergonomic
attachment and compilation shown here.

```python
from stateforge_provider import Provider, operation
from stateforge_provider_views import views

OVERVIEW = views.view(
    views.layout.stack(
        direction="vertical",
        children=[
            views.content.text(text="Nginx service"),
            views.status.badge(
                label="Provider health",
                bind_state=views.bind.provider.health(),
            ),
        ],
    ),
)

RUN = views.view(
    views.layout.stack(
        direction="vertical",
        children=[
            views.content.markdown(markdown="### Restarting Nginx"),
            views.status.timeline(
                bind_events=views.bind.operation_run.events(),
            ),
            views.status.progress(
                show_percentage=True,
                bind_progress=views.bind.operation_run.progress(),
            ),
        ],
    ),
)

class NginxProvider(Provider):
    provider_view = OVERVIEW

    @operation("example.nginx/restart@1", run_view=RUN)
    async def restart(self, request, context):
        ...
```

The Provider Overview tree is attached to the Provider declaration. The run
tree is attached to exactly the declared operation identifier. Equivalent
attachment points are needed for operation request/result and trigger
policy/event views, but their precise Provider Python signatures are left to
that repository's authoring milestone. A typed result field can also carry
display hints; those hints must compile to the same catalog tree model rather
than create a second rendering contract. View helpers may be split across
Python modules and reused without changing the wire shape.

| Declaration target | Surface | Typical composition | Data resolved by the Control Plane |
| --- | --- | --- | --- |
| Provider | Provider Overview | Description, health badge, metrics, capability navigation | Accepted Provider descriptor, current health, statistics, allowed capabilities |
| One operation | Operation Request | Schema-driven form and host submit action | Input schema and approved request context |
| One operation | Operation Run | Explanation, steps/timeline, percentage and status | Admitted operation's current progress and non-secret observations |
| One operation | Operation Result | Result summary, table, diff, logs or artifacts | Validated terminal result and references |
| One trigger | Trigger Policy | Trigger description and schema-driven policy configuration | Trigger declaration and Control Plane policy |
| One trigger | Trigger Event | Event summary and structured payload display | Accepted, validated trigger event |
| Operation or trigger | Evidence | Audit-oriented evidence components | Control Plane-selected evidence record |

The table identifies destinations, not an obligation to use every component.
The author selects a surface and builds a tree valid for that surface; the
Control Plane still generates the canonical form and result display from
schemas when custom presentation is missing.

## Ownership and translation

| Owner | Responsibility | Must not own |
| --- | --- | --- |
| Control Plane | Canonical versioned catalog; surface and binding-source contracts; validation, data resolution, renderers, accessibility, responsive behavior, theming, and host-controlled actions. | Provider Python authoring syntax or SFP wire definitions. |
| `stateforge-provider-views` | Deterministically generate version-specific typed component helpers and matching developer documentation from a pinned Control Plane catalog export. | A competing component registry, renderer, or Provider runtime. |
| Provider Python | Public Provider/operation/trigger view attachment API; compile author declarations into the SFP presentation model; validate early with the matching generated catalog API. | Control Plane rendering or independent catalog semantics. |
| SFP (`stateforge-protocol`) | Generic `ProviderPresentation`, `PresentationTarget`, `PresentationSurface`, `ComponentNode`, `DataBinding`, asset, condition, and repetition wire types and wire-level validation. | Catalog-specific component identifiers, property schemas, renderer applicability, or UI policy. |

The intended path is:

1. A Provider author composes typed components using the generated API for a
   particular Control Plane version and attaches views through Provider Python.
2. Provider Python compiles the trees into the generic SFP presentation
   snapshot returned alongside the manifest. It does not alter the manifest's
   operational declarations or JSON Schemas.
3. The Agent carries the accepted presentation snapshot without inventing
   catalog semantics. Its session and revision checks remain in force.
4. The Control Plane validates against its own product-version catalog,
   including the surface, component, property, binding, asset, and child
   contracts. It resolves approved data sources for the current context and
   renders the tree with its own
   implementations.
5. If the presentation is absent, invalid, or incompatible, the Control Plane
   uses its generic presentation from the operational schemas. It does not
   reject an otherwise valid operation or trigger merely because the visual
   overlay cannot render.

The Provider Views package version follows the **complete Control Plane
product version**, initially `0.1.0`. It is not keyed only to major `0` or
to a separate catalog version. Component identifiers such as
`stateforge.ui/status.badge@1` have their own major contract suffix; that
suffix is not the catalog's release version. Generation must record its exact
Control Plane source revision and digest so package, documentation, and
renderer implementation can be checked against the same catalog snapshot.

## Operational truth and presentation limits

An operation's input and result JSON Schemas and a trigger's payload JSON
Schema remain authoritative. A view may choose how values are arranged and
explained; it cannot add or remove a capability, redefine a field, change a
required field into an optional one, hide a required field from an actionable
request, change admission or execution behavior, or claim a result that does
not validate against the declared schema. The Control Plane must preserve a
usable schema-derived path for every operation and trigger, including when a
view is unavailable.

Control Plane data is available to a node only when all three checks pass:
the current surface permits the source, the component's named slot accepts
the source and data shape, and the selected JSON Pointer resolves to an
allowed non-secret value. A binding is not authorization to read arbitrary
Control Plane state. Secret-bearing `writeOnly` request values and private
runtime data are not presentation sources. Host-controlled actions such as
submit and cancel retain Control Plane authorization and confirmation rules;
the Provider may place their catalog components but cannot redefine what they
do.

Provider declarations may contain only catalog-recognized, bounded data.
They cannot carry arbitrary HTML, CSS, JavaScript, executable frontend
extensions, arbitrary filesystem paths, URLs for remote-resource loading, or
instructions to install code. Assets must be packaged through the approved
content-addressed asset path and validated for type, size, and use. The
generic SFP schema contains renderer-requirement metadata, but that field is
not permission to execute Provider-supplied code; the MVP Control Plane must
reject or ignore unsupported extension requirements and retain generic
presentation. A future extension-host policy would require a separate
product and security decision.

## Renderer contract

A published catalog entry is a promise of Control Plane behavior on its
declared surfaces. Before release, each entry needs a renderer that honors its
properties, bindings, children, assets, fallback, keyboard/accessibility
semantics, and responsive behavior, plus tests for those rules. A shared
primitive may implement multiple entries, but it must preserve each entry's
distinct behavior. A generic placeholder is not conformance.

This is a release gate for later catalog and renderer work, not a claim that
all renderers in the current source tree already exist. C3 neither changes
catalog membership nor implements a renderer.

Renderers receive resolved, validated data and a component declaration. They
do not fetch Provider-controlled resources, evaluate arbitrary expressions,
or interpret source code in component properties. The renderer registry is a
Control Plane implementation detail, not an author-controlled catalog. The
Provider Views editor may preview declarations during development, but it is
not the runtime renderer, a new protocol participant, or a second catalog
owner. End-to-end verification must ultimately include a real Provider
declaration travelling through SFP to the Control Plane renderer.

## Frontend stack decision

The Control Plane frontend will use **React, TypeScript, and Vite**. React
will implement the Control Plane-owned component renderers and shared UI
primitives. TypeScript will provide typed renderer interfaces and should be
checked or generated against the versioned catalog contracts. Vite will
provide the development server and production bundling for the self-hosted
Control Plane frontend; it is the build tool, not the UI framework.

This stack choice does not make React a Provider-facing dependency. The
catalog JSON, generated Provider authoring API, and SFP presentation payload
remain framework-neutral. Providers declare catalog components and data;
they do not send React components or executable frontend code. React remains
an internal Control Plane implementation detail, so replacing it later would
not require changing Provider declarations, SFP messages, or component
identifiers.
