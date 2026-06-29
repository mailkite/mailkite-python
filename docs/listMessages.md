# `listMessages`

List stored messages, newest first. Optionally page with `before` (a `received_at` cursor) and `limit`; omit both for the default newest 100. Response is a bare array — paginate by passing the last row's `received_at` as the next `before`.

**HTTP:** `GET /api/messages`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `before` | query (optional) | Cursor: return only messages with `received_at` strictly less than this (epoch ms). Omit for the first page. |
| `limit` | query (optional) | Max rows to return, 1–200. Omitted = newest 100 (the pre-pagination default). |

## Returns

`any`

## Example

```python
res = mk.listMessages()
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
