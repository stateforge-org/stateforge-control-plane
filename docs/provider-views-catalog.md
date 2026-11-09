# Provider Views catalog

> Control Plane version: `0.1.0` · catalog SHA-256: `20c0ef72fe7f651bf9e5f245fbad74f136c61e39189cbef8d7384f84c254f66a`

The Control Plane owns this catalog. Provider tooling may consume the generated JSON; Protocol transports the generic presentation tree and does not own this component registry.

## Surfaces

| Surface | Purpose | Binding sources |
| --- | --- | --- |
| `stateforge.ui/surface.provider.overview@1` | Provider identity, description, health, statistics, assets, and capability navigation. | `provider.descriptor@1`, `provider.health@1`, `provider.statistics@1`, `provider.capabilities@1` |
| `stateforge.ui/surface.operation.request@1` | Configure and review an operation request. | `operation.input_schema@1`, `operation.request_context@1` |
| `stateforge.ui/surface.operation.run@1` | Follow an admitted operation's current state and progress. | `operation.run@1` |
| `stateforge.ui/surface.operation.result@1` | Present terminal results, outputs, references, and artifacts. | `operation.result@1` |
| `stateforge.ui/surface.trigger.policy@1` | Present a trigger while it is selected and configured in policy. | `trigger.declaration@1`, `trigger.policy@1` |
| `stateforge.ui/surface.trigger.event@1` | Present one published trigger occurrence. | `trigger.event@1` |
| `stateforge.ui/surface.evidence@1` | Present structured evidence and audit material associated with an operation or trigger. | `evidence.record@1` |

## Core components

| Component | Purpose | Surfaces | Binding slots |
| --- | --- | --- | --- |
| `stateforge.ui/action.operation_cancel@1` | Request placement of the host-controlled cancellation action. | `stateforge.ui/surface.operation.run@1` | None |
| `stateforge.ui/action.operation_submit@1` | Request placement of the host-controlled admission action. | `stateforge.ui/surface.operation.request@1` | None |
| `stateforge.ui/content.markdown@1` | Sanitized restricted Markdown. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `markdown` |
| `stateforge.ui/content.text@1` | Plain trusted text. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `text` |
| `stateforge.ui/data.artifacts@1` | Results, checkpoints, evidence, and references. | `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.evidence@1` | `artifacts` |
| `stateforge.ui/data.chart@1` | Line, area, bar, or scatter series. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `series` |
| `stateforge.ui/data.code@1` | Read-only code or structured text. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `value` |
| `stateforge.ui/data.diff@1` | Before/after or proposed/current differences. | `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.evidence@1` | `before`, `after` |
| `stateforge.ui/data.key_value@1` | Labels and scalar values. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `value` |
| `stateforge.ui/data.log@1` | Bounded streaming or retained log output. | `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `entries` |
| `stateforge.ui/data.metric@1` | One important numeric measurement. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `value` |
| `stateforge.ui/data.table@1` | Repeated objects or records. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `rows` |
| `stateforge.ui/data.topology@1` | Nodes and relationships. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `graph` |
| `stateforge.ui/data.tree@1` | Nested structured data. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `value` |
| `stateforge.ui/input.array@1` | Repeated structured values. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `schema` |
| `stateforge.ui/input.code@1` | Structured text, JSON, YAML, or expression editor. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `schema` |
| `stateforge.ui/input.field@1` | Schema-compatible scalar control. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `field_schema` |
| `stateforge.ui/input.form@1` | Complete schema-generated form. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `schema` |
| `stateforge.ui/input.key_value@1` | Arbitrary property-map editor. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `schema` |
| `stateforge.ui/input.object@1` | Nested object editor. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `schema` |
| `stateforge.ui/input.secret@1` | A writeOnly secret value. | `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.trigger.policy@1` | `field_schema` |
| `stateforge.ui/layout.grid@1` | Responsive grid. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/layout.section@1` | Titled, optionally collapsible section. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/layout.stack@1` | Vertical or horizontal content flow. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/layout.steps@1` | Ordered stages or procedures. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/layout.tabs@1` | Alternate related representations. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.request@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/media.image@1` | Content-addressed PNG or sanitized SVG. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.policy@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | None |
| `stateforge.ui/status.badge@1` | Compact semantic state. | `stateforge.ui/surface.provider.overview@1`, `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `state` |
| `stateforge.ui/status.progress@1` | Determinate or staged progress. | `stateforge.ui/surface.operation.run@1` | `progress` |
| `stateforge.ui/status.timeline@1` | Ordered events, conditions, or checkpoints. | `stateforge.ui/surface.operation.run@1`, `stateforge.ui/surface.operation.result@1`, `stateforge.ui/surface.trigger.event@1`, `stateforge.ui/surface.evidence@1` | `events` |

### `stateforge.ui/action.operation_cancel@1`

Request placement of the host-controlled cancellation action.

**Properties**

None.

**Binding slots**

None.

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {},
  "bindings": {}
}
```

### `stateforge.ui/action.operation_submit@1`

Request placement of the host-controlled admission action.

**Properties**

None.

**Binding slots**

None.

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {},
  "bindings": {}
}
```

### `stateforge.ui/content.markdown@1`

Sanitized restricted Markdown.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `markdown` | `{"maxLength":16000,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `markdown` | string | `provider.descriptor@1`, `provider.health@1`, `provider.statistics@1`, `provider.capabilities@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "markdown": "## Status"
  },
  "bindings": {
    "markdown": {
      "source_identifier": "provider.descriptor@1",
      "pointer": "/description"
    }
  }
}
```

### `stateforge.ui/content.text@1`

Plain trusted text.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `text` | `{"maxLength":4000,"type":"string"}` |
| `tone` | `{"enum":["neutral","muted","accent"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `text` | string | `provider.descriptor@1`, `provider.health@1`, `provider.statistics@1`, `provider.capabilities@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "text": "Provider ready",
    "tone": "neutral"
  },
  "bindings": {
    "text": {
      "source_identifier": "provider.descriptor@1",
      "pointer": "/displayName"
    }
  }
}
```

### `stateforge.ui/data.artifacts@1`

Results, checkpoints, evidence, and references.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `compact` | `{"type":"boolean"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `artifacts` | array of artifact references | `operation.result@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: `stateforge.ui/data.table@1`.

**Example**

```json
{
  "properties": {
    "compact": false
  },
  "bindings": {
    "artifacts": {
      "source_identifier": "operation.result@1",
      "pointer": "/artifacts"
    }
  }
}
```

### `stateforge.ui/data.chart@1`

Line, area, bar, or scatter series.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `kind` | `{"enum":["line","area","bar","scatter"],"type":"string"}` |
| `xLabel` | `{"maxLength":80,"type":"string"}` |
| `yLabel` | `{"maxLength":80,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `series` | array of series or points | `provider.statistics@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: `stateforge.ui/data.table@1`.

**Example**

```json
{
  "properties": {
    "kind": "line",
    "xLabel": "Time",
    "yLabel": "Value"
  },
  "bindings": {
    "series": {
      "source_identifier": "provider.statistics@1",
      "pointer": "/series"
    }
  }
}
```

### `stateforge.ui/data.code@1`

Read-only code or structured text.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `language` | `{"enum":["json","yaml","text","shell"],"type":"string"}` |
| `wrap` | `{"type":"boolean"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `value` | string or JSON value | `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "language": "json",
    "wrap": true
  },
  "bindings": {
    "value": {
      "source_identifier": "operation.result@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/data.diff@1`

Before/after or proposed/current differences.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `beforeLabel` | `{"maxLength":100,"type":"string"}` |
| `afterLabel` | `{"maxLength":100,"type":"string"}` |
| `format` | `{"enum":["text","json","yaml"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `before` | JSON value | `operation.result@1`, `evidence.record@1` |
| `after` | JSON value | `operation.result@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "beforeLabel": "Before",
    "afterLabel": "After",
    "format": "json"
  },
  "bindings": {
    "before": {
      "source_identifier": "operation.result@1",
      "pointer": "/before"
    },
    "after": {
      "source_identifier": "operation.result@1",
      "pointer": "/after"
    }
  }
}
```

### `stateforge.ui/data.key_value@1`

Labels and scalar values.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `value` | object or scalar map | `provider.descriptor@1`, `provider.health@1`, `provider.statistics@1`, `provider.capabilities@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {},
  "bindings": {
    "value": {
      "source_identifier": "provider.descriptor@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/data.log@1`

Bounded streaming or retained log output.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `maxLines` | `{"maximum":5000,"minimum":1,"type":"integer"}` |
| `autoFollow` | `{"type":"boolean"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `entries` | string or array of log records | `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "maxLines": 200,
    "autoFollow": false
  },
  "bindings": {
    "entries": {
      "source_identifier": "operation.run@1",
      "pointer": "/logs"
    }
  }
}
```

### `stateforge.ui/data.metric@1`

One important numeric measurement.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":100,"type":"string"}` |
| `unit` | `{"maxLength":40,"type":"string"}` |
| `precision` | `{"maximum":6,"minimum":0,"type":"integer"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `value` | number or metric object | `provider.statistics@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Requests",
    "unit": "count",
    "precision": 0
  },
  "bindings": {
    "value": {
      "source_identifier": "provider.statistics@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/data.table@1`

Repeated objects or records.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `caption` | `{"maxLength":160,"type":"string"}` |
| `columns` | `{"items":{"additionalProperties":false,"properties":{"key":{"maxLength":128,"type":"string"},"label":{"maxLength":128,"type":"string"}},"required":["key","label"],"type":"object"},"maxItems":32,"type":"array"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `rows` | array of objects | `provider.capabilities@1`, `provider.statistics@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "caption": "Recent events",
    "columns": [
      {
        "key": "name",
        "label": "Name"
      }
    ]
  },
  "bindings": {
    "rows": {
      "source_identifier": "provider.capabilities@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/data.topology@1`

Nodes and relationships.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `layout` | `{"enum":["auto","horizontal","vertical"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `graph` | nodes-and-edges object | `provider.statistics@1`, `provider.capabilities@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: `stateforge.ui/data.table@1`.

**Example**

```json
{
  "properties": {
    "layout": "auto"
  },
  "bindings": {
    "graph": {
      "source_identifier": "provider.statistics@1",
      "pointer": "/topology"
    }
  }
}
```

### `stateforge.ui/data.tree@1`

Nested structured data.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `initialDepth` | `{"maximum":16,"minimum":0,"type":"integer"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `value` | JSON object or array | `operation.request_context@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Resource",
    "initialDepth": 2
  },
  "bindings": {
    "value": {
      "source_identifier": "operation.result@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/input.array@1`

Repeated structured values.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `description` | `{"maxLength":500,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Up to 256 children from layout, input.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Interfaces"
  },
  "bindings": {
    "schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": "/properties/interfaces"
    }
  }
}
```

### `stateforge.ui/input.code@1`

Structured text, JSON, YAML, or expression editor.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `language` | `{"enum":["json","yaml","text","expression"],"type":"string"}` |
| `rows` | `{"maximum":80,"minimum":3,"type":"integer"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "language": "json",
    "rows": 12
  },
  "bindings": {
    "schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/input.field@1`

Schema-compatible scalar control.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `description` | `{"maxLength":500,"type":"string"}` |
| `placeholder` | `{"maxLength":160,"type":"string"}` |
| `widget` | `{"enum":["auto","text","textarea","number","checkbox","select","radio","slider","date-time"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `field_schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "widget": "auto"
  },
  "bindings": {
    "field_schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": "/properties/name"
    }
  }
}
```

### `stateforge.ui/input.form@1`

Complete schema-generated form.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `title` | `{"maxLength":160,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Up to 256 children from layout, input.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "title": "Configure operation"
  },
  "bindings": {
    "schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/input.key_value@1`

Arbitrary property-map editor.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `description` | `{"maxLength":500,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Tags"
  },
  "bindings": {
    "schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": "/properties/tags"
    }
  }
}
```

### `stateforge.ui/input.object@1`

Nested object editor.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `description` | `{"maxLength":500,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `schema` | JSON Schema object | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Up to 256 children from layout, input.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Network settings"
  },
  "bindings": {
    "schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": "/properties/network"
    }
  }
}
```

### `stateforge.ui/input.secret@1`

A writeOnly secret value.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":160,"type":"string"}` |
| `description` | `{"maxLength":500,"type":"string"}` |
| `placeholder` | `{"maxLength":160,"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `field_schema` | writeOnly JSON Schema property | `operation.input_schema@1`, `trigger.declaration@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Credential"
  },
  "bindings": {
    "field_schema": {
      "source_identifier": "operation.input_schema@1",
      "pointer": "/properties/credential"
    }
  }
}
```

### `stateforge.ui/layout.grid@1`

Responsive grid.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `columns` | `{"maximum":12,"minimum":1,"type":"integer"}` |
| `gap` | `{"enum":["small","medium","large"],"type":"string"}` |

**Binding slots**

None.

**Asset slots**

None.

**Children**

Up to 256 children from layout, input, content, data, status, media, action.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "columns": 2
  },
  "bindings": {}
}
```

### `stateforge.ui/layout.section@1`

Titled, optionally collapsible section.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `title` | `{"maxLength":160,"type":"string"}` |
| `collapsible` | `{"type":"boolean"}` |
| `initiallyCollapsed` | `{"type":"boolean"}` |

**Binding slots**

None.

**Asset slots**

None.

**Children**

Up to 256 children from layout, input, content, data, status, media, action.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "title": "Details",
    "collapsible": false
  },
  "bindings": {}
}
```

### `stateforge.ui/layout.stack@1`

Vertical or horizontal content flow.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `direction` | `{"enum":["vertical","horizontal"],"type":"string"}` |
| `gap` | `{"enum":["none","small","medium","large"],"type":"string"}` |

**Binding slots**

None.

**Asset slots**

None.

**Children**

Up to 256 children from layout, input, content, data, status, media, action.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "direction": "vertical"
  },
  "bindings": {}
}
```

### `stateforge.ui/layout.steps@1`

Ordered stages or procedures.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `labels` | `{"items":{"maxLength":80,"type":"string"},"maxItems":64,"minItems":1,"type":"array"}` |
| `currentIndex` | `{"minimum":0,"type":"integer"}` |

**Binding slots**

None.

**Asset slots**

None.

**Children**

Up to 64 children from layout, input, content, data, status, media, action. Child count must match property `labels`.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "labels": [
      "Prepare",
      "Apply"
    ],
    "currentIndex": 0
  },
  "bindings": {}
}
```

### `stateforge.ui/layout.tabs@1`

Alternate related representations.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `labels` | `{"items":{"maxLength":80,"type":"string"},"maxItems":16,"minItems":1,"type":"array"}` |
| `selectedIndex` | `{"minimum":0,"type":"integer"}` |

**Binding slots**

None.

**Asset slots**

None.

**Children**

Up to 16 children from layout, input, content, data, status, media, action. Child count must match property `labels`.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "labels": [
      "Summary",
      "Details"
    ],
    "selectedIndex": 0
  },
  "bindings": {}
}
```

### `stateforge.ui/media.image@1`

Content-addressed PNG or sanitized SVG.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `fit` | `{"enum":["contain","cover"],"type":"string"}` |
| `caption` | `{"maxLength":160,"type":"string"}` |

**Binding slots**

None.

**Asset slots**

| Slot | Permitted media types |
| --- | --- |
| `image` | `image/png`, `image/svg+xml` |

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "fit": "contain"
  },
  "bindings": {}
}
```

### `stateforge.ui/status.badge@1`

Compact semantic state.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `label` | `{"maxLength":100,"type":"string"}` |
| `tone` | `{"enum":["neutral","info","success","warning","danger"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `state` | string or object | `provider.health@1`, `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "label": "Ready",
    "tone": "success"
  },
  "bindings": {
    "state": {
      "source_identifier": "provider.health@1",
      "pointer": ""
    }
  }
}
```

### `stateforge.ui/status.progress@1`

Determinate or staged progress.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `showPercentage` | `{"type":"boolean"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `progress` | number or progress object | `operation.run@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "showPercentage": true
  },
  "bindings": {
    "progress": {
      "source_identifier": "operation.run@1",
      "pointer": "/progress"
    }
  }
}
```

### `stateforge.ui/status.timeline@1`

Ordered events, conditions, or checkpoints.

**Properties**

| Property | JSON Schema |
| --- | --- |
| `orientation` | `{"enum":["vertical","horizontal"],"type":"string"}` |

**Binding slots**

| Slot | Expected shape | Sources |
| --- | --- | --- |
| `events` | array of event objects | `operation.run@1`, `operation.result@1`, `trigger.event@1`, `evidence.record@1` |

**Asset slots**

None.

**Children**

Leaf component; children are not allowed.

**Fallback guidance**

Provider may supply a complete core-component fallback. Recommended: none specified.

**Example**

```json
{
  "properties": {
    "orientation": "vertical"
  },
  "bindings": {
    "events": {
      "source_identifier": "operation.run@1",
      "pointer": "/events"
    }
  }
}
```

## Reference Provider corpus

These seven cases are illustrative Control Plane design and renderer-test fixtures, not normative Protocol requirements.

| Provider | Operation or trigger | Contract pressure |
| --- | --- | --- |
| AWS EC2 | `instance.launch@1` | Deep request objects, network interfaces, block devices, tags, mutually exclusive options, and results containing multiple instances. |
| Kubernetes | `deployment.apply@1`, `deployment.degraded@1` | Large nested manifests, repeated configuration, resource diffs, rollout conditions, replica metrics, logs, and topology. |
| PostgreSQL | `database.point_in_time_recover@1` | Mutually exclusive recovery targets, backup selection, tablespace mappings, staged progress, WAL evidence, and recovery timelines. |
| Model training | `training.start@1`, `training.metric_threshold@1` | Arbitrary hyperparameters, datasets, distributed compute, time-series metrics, checkpoints, images, models, and downloadable artifacts. |
| Cloudflare | `ruleset.deploy@1` | Ordered rules, nested logical expressions, a visual expression builder, validation results, and configuration diffs. |
| GitHub | `pull_request.changed@1` | A deeply nested event containing repository, actor, pull request, change, and delivery metadata. |
| systemd | `service.restart@1`, `service.failed@1` | A simple baseline with one resource selector, short progress, status, journal output, and a small trigger payload. |

## Proposed decisions

These defaults are explicit proposals pending product review. Operational schemas remain authoritative; component properties only affect presentation.

- **binding-sources**: Use only the versioned, surface-scoped binding sources declared in binding-sources.json. Sources are host-provided snapshots; Provider-authored views cannot cross surfaces, executions, or sessions, and raw operation request values are excluded.
- **conditions-and-repetition**: Use the four SFP v1 condition operators EXISTS, NOT_EXISTS, EQUALS, and NOT_EQUALS. Repetition uses a named item scope and is capped at the SFP v1 maximum of 1024 items; renderers may impose lower limits.
- **component-property-schemas**: Give every core component a closed JSON Schema for presentation-only properties. Keep operational fields, requiredness, authorization, and execution semantics exclusively in the operational schema and host policy.
- **evidence-surface**: Keep one shared stateforge.ui/surface.evidence@1 surface for operation and trigger evidence; the host supplies the evidence record kind and data.
- **host-actions**: Treat operation_submit and operation_cancel as requests to place host-controlled UI actions only. They cannot execute Provider code or grant permission; authorization, availability, confirmation, label, and visibility remain Control Plane decisions.
- **reference-corpus**: Use all seven catalog corpus examples as illustrative Control Plane fixtures, not normative SFP conformance requirements.

## Compatibility

An existing versioned identifier keeps its meaning. Meaning changes and incompatible property, binding, surface, asset-slot, child, or fallback changes require a new major identifier; retain the old descriptor. A destructive catalog change is released with a Control Plane major-version bump. The initial purpose baseline is in `provider_views/catalog/0.1.0/compatibility.json`.
