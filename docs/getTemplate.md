# `getTemplate`

Get one template (full: subject, html, text, theme). Works for your templates (tpl_…) and base templates (base_…).

**HTTP:** `GET /api/templates/{id}`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `id` | path | — |

## Returns

`any`

## Example

```python
res = mk.getTemplate("tpl_1")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
