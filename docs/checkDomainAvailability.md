# `checkDomainAvailability`

Check whether a domain is available to register, and at what price. Read-only — no charge.

**HTTP:** `GET /api/domains/register/check`

## Parameters

| Name | In | Description |
| --- | --- | --- |
| `domain` | query | — |

## Returns

`any`

## Example

```python
res = mk.checkDomainAvailability("acme.com")
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
