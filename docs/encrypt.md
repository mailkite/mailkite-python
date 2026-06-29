# `encrypt`

Encrypt a UTF-8 string to a domain's RSA public key (SPKI/PEM), returning the at-rest envelope JSON (`{v,keyAlg,fp,enc,iv,wrappedKey,ciphertext}`). Hybrid scheme: a fresh AES-256-GCM content key wrapped with RSA-OAEP(SHA-256) — byte-compatible with MailKite's own at-rest encryption. Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `plaintext` | string | ✓ | The UTF-8 string to encrypt (e.g. a message body you're about to store). |
| `publicKey` | string | ✓ | The recipient domain's RSA public key in SPKI/PEM form (-----BEGIN PUBLIC KEY-----)… |

## Returns

`string`

## Example

```python
res = mk.encrypt({ … })
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
