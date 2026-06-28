# `semanticSearch`

Semantic search over the MailKite documentation — returns the most relevant doc sections for a natural-language query (hybrid vector + keyword search over https://mailkite.dev/docs). Public; no authentication required.

**HTTP:** `GET /v1/docs/search`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `query` | query | — |

## Returns

`semantic-search-response` — see the [`semantic-search-response`](https://mailkite.dev/docs/api-reference) schema.

## Example

```python
res = mk.semanticSearch("domains")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
