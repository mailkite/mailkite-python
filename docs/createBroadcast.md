# `createBroadcast`

Create a broadcast draft. `from` is required; set `audience` to { type: "all" } or { type: "list", id: "lst_…" }. Returns the broadcast with its id (bct_…). Send it with sendBroadcast.

**HTTP:** `POST /api/broadcasts`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string |  |  |
| `from` | string | ✓ |  |
| `replyTo` | string |  |  |
| `subject` | string |  |  |
| `preview` | string |  |  |
| `audience` | object |  |  |
| `templateId` | string |  |  |
| `html` | string |  |  |
| `text` | string |  |  |
| `footerAddress` | string |  |  |

## Returns

`any`

## Example

```python
res = mk.createBroadcast({
    "from": "news@app.mailkite.dev",
    "subject": "Launch week",
    "audience": [object Object],
    "html": "<h1>We shipped</h1>",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
