# `removeListContact`

Remove one contact from a list (the contact itself is kept).

**HTTP:** `DELETE /api/lists/{id}/contacts/{contactId}`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `id` | path | — |
| `contactId` | path | — |

## Returns

`any`

## Example

```python
res = mk.removeListContact("lst_1", "ctr_1")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
