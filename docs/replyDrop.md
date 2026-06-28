# `replyDrop`

Control-mode reply a webhook consumer returns to tell MailKite to drop (discard) the message — the string `{"status":"drop"}`. Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

_None._

## Returns

`string`

## Example

```python
res = mk.replyDrop()
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
