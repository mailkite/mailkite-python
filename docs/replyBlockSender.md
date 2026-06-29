# `replyBlockSender`

Control-mode reply a webhook consumer returns to tell MailKite to block the sender — the string `{"status":"ok","actions":[{"type":"block-sender"}]}`. Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

_None._

## Returns

`string`

## Example

```python
res = mk.replyBlockSender()
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
