# `testWebhook`

Send a signed test event to the domain's webhook.

**HTTP:** `POST /api/domains/{id}/webhook/test`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `id` | path | — |

## Returns

`any`

## Example

```python
res = mk.testWebhook("dom_1")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
