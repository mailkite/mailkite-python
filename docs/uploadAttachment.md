# `uploadAttachment`

Upload a file to MailKite storage and get back a secure, time-limited URL. Reference the returned `url` as an attachment in send() (`{ filename, url }`) or link it inline in your HTML — instead of base64-inlining large files on every send. Give the file ONE of four ways: a local `path` (read and streamed as raw bytes by the CLI/SDK/local MCP), a remote `url` (MailKite fetches and re-hosts it), base64 `content`, or — over raw HTTP — the file bytes as the POST body with `?filename=`. `retentionDays` (7/30/90/365, default 7) sets how long the file and URL live.

**HTTP:** `POST /v1/attachments`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `filename` | string |  | The file's name, e.g. "invoice.pdf". Shown to recipients on download. Optional when it… |
| `path` | string |  | Local filesystem path to the file. Read client-side by the CLI, SDKs, and the local MCP… |
| `url` | string |  | A remote http(s) URL. MailKite fetches it and re-hosts the bytes under your account. Max… |
| `content` | string |  | The file bytes, base64-encoded. The lowest-common-denominator fallback when you can't… |
| `contentType` | string |  | MIME type, e.g. "application/pdf". Defaults to application/octet-stream (or is inferred… |
| `retentionDays` | integer |  | How long the file (and its signed URL) stays valid. One of 7, 30, 90, 365. Defaults to 7. |

## Returns

`upload-attachment-response` — see the [`upload-attachment-response`](https://mailkite.dev/docs/api-reference) schema.

## Example

```python
res = mk.uploadAttachment({
    "filename": "po.pdf",
    "content": "JVBERi0xLjQK",
    "contentType": "application/pdf",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
