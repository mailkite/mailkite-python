# `sendBroadcast`

Send a broadcast now, or pass an ISO 8601 `scheduledAt` to schedule it. A one-click unsubscribe is always added. Returns the status and resolved audience count.

**HTTP:** `POST /api/broadcasts/{id}/send`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `scheduledAt` | string |  |  |

## Returns

`any`

## Example

```python
res = mk.sendBroadcast({
    "id": "bct_1",
    "scheduledAt": "2026-07-01T15:00:00Z",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
