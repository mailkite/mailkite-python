# `updateList`

Rename a contact list.

**HTTP:** `PATCH /api/lists/{id}`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | ✓ |  |

## Returns

`any`

## Example

```python
res = mk.updateList({
    "id": "lst_1",
    "name": "VIPs",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
