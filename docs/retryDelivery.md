# `retryDelivery`

Re-deliver a stored message to its webhook.

**HTTP:** `POST /api/deliveries/{id}/retry`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `id` | path | — |

## Returns

`any`

## Example

```python
res = mk.retryDelivery("dlv_1")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
