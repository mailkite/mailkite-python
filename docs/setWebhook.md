# `setWebhook`

Set or replace the domain's catch-all webhook.

**HTTP:** `PUT /api/domains/{id}/webhook`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | string | ✓ |  |

## Returns

`any`

## Example

```python
res = mk.setWebhook({
    "id": "dom_1",
    "url": "https://app.com/hooks/mailkite",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
