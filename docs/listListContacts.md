# `listListContacts`

List the contacts that are members of a list, newest first. Optionally page with `before` (a `last_seen_at`/`created_at` cursor) and `limit`. Response is a bare array — paginate by passing the last row's `last_seen_at` (or `created_at`) as the next `before`.

**HTTP:** `GET /api/lists/{id}/contacts`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `id` | path | — |
| `before` | query (optional) | Cursor: return only members with `last_seen_at` (or `created_at`) strictly less than this (epoch ms). Omit… |
| `limit` | query (optional) | Max rows to return (default 100, max 500). |

## Returns

`any`

## Example

```python
res = mk.listListContacts("lst_1")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
