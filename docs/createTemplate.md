# `createTemplate`

Create a template. Pass `baseId` to clone a base template into your own, or provide name/subject/html/text/theme directly.

**HTTP:** `POST /api/templates`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `baseId` | string |  | Clone this base template (base_…) into your own. When set, name is optional (defaults to… |
| `name` | string |  | Template name. Required unless baseId is given. |
| `subject` | string |  | Default subject line for sends. |
| `html` | string |  | Rendered, send-ready HTML. |
| `text` | string |  | Plaintext fallback. |
| `json` | string |  | Editor (TipTap) JSON source, for re-editing in the dashboard. |
| `theme` | string |  | Brand tokens JSON (bg, surface, primary, text, logo, …). |

## Returns

`any`

## Example

```python
res = mk.createTemplate({
    "baseId": "base_welcome",
    "name": "My Welcome",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
