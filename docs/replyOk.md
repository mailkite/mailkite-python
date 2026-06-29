# `replyOk`

The acknowledgement body a webhook consumer returns to confirm it processed the event — the string `{"status":"ok"}`. Send it with a 2xx when the route is in `ack` mode (or always — it's harmless in `lenient` mode). Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

_None._

## Returns

`string`

## Example

```python
res = mk.replyOk()
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
