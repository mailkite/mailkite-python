# `registerDomain`

Register (buy) a domain on the customer's behalf; provisions mail DNS and adds it to the account in one call. Charges the registrar.

**HTTP:** `POST /api/domains/register`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `domain` | string | ✓ |  |
| `contact` | object | ✓ |  |
| `years` | integer |  |  |
| `dryRun` | boolean |  |  |

## Returns

`any`

## Example

```python
res = mk.registerDomain({
    "domain": "acme.com",
    "contact": [object Object],
    "years": 1,
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
