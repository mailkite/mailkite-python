# `createDomain`

Add a domain. Returns the domain + DNS records.

**HTTP:** `POST /api/domains`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `domain` | string | ✓ |  |

## Returns

`any`

## Example

```python
res = mk.createDomain({
    "domain": "app.mailkite.dev",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
