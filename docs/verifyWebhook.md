# `verifyWebhook`

Verify the `x-mailkite-signature` header on an inbound webhook delivery. Runs entirely locally (HMAC-SHA256 over `${t}.${payload}`) — no network call. Returns true only when the signature matches and the event is within the freshness window.

**Local** — runs in the SDK, no network call.

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `payload` | string | ✓ | The raw, unparsed webhook request body — the exact bytes you received. |
| `signature` | string | ✓ | The `x-mailkite-signature` header value, e.g. `t=1750000000000,v1=4f1a9c…`. |
| `secret` | string | ✓ | Your webhook signing secret (from the dashboard). |
| `toleranceMs` | integer |  | Reject events whose timestamp is more than this many milliseconds old, to block replays… |

## Returns

`boolean`

## Example

```python
res = mk.verifyWebhook({
    "signature": "t=1750000000000,v1=3d790f831e170ddba4d001f27532bf2c1fc68ebed52eef72fe453dfa1196b03c",
    "payload": "{"type":"email.received","id":"evt_123","message":"It works."}",
    "secret": "whsec_mailkite_test",
    "toleranceMs": 0,
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
