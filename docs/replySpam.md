# `replySpam`

Control-mode reply a webhook consumer returns to tell MailKite to mark the message as spam — the string `{"status":"spam"}`. Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

_None._

## Returns

`string`

## Example

```python
res = mk.replySpam()
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
