# `decrypt`

Decrypt a MailKite at-rest envelope JSON with your RSA private key (PKCS8/PEM), returning the original UTF-8 string. Reverses `encrypt` / MailKite's at-rest encryption (RSA-OAEP(SHA-256) unwrap → AES-256-GCM open). Local, no network call.

**Local** — runs in the SDK, no network call.

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `envelope` | string | ✓ | The at-rest envelope JSON string ({v,keyAlg,fp,enc,iv,wrappedKey,ciphertext}) from… |
| `privateKey` | string | ✓ | Your RSA private key in PKCS8/PEM form (-----BEGIN PRIVATE KEY-----) — the match to the… |

## Returns

`string`

## Example

```python
res = mk.decrypt({
    "envelope": "{"v":1,"keyAlg":"RSA-OAEP-256","fp":"c3be15f1703b8841e3be563d41970eae6431124e84f9ed1748b4e5af372e099c","enc":"A256GCM","iv":"OHxFNxJU/ySQhl4l","wrappedKey":"lwrH9IiLjJIq1+jvCMpBJ+63vP6jMotJ1eB4OrdShQ4ZGv/jlP+eUkVxa/hK9Xnp9Jez0yLASkKoO2vCxPy5CWKLk1rsOSdkc3G1Kg8A301cgg3+DNuM5SeaTkWRcjNIcZvKF0CBt/EB5pzqekVATwf3LojjzFenXZdCFzF2L/XSi0fmChvTj3RbFNRQczMPW2PVp4nhULylbVP9HUv1MNVH8Y42+kqUPzAelolM7l4hDgB1ujqcXGwAQ0w+xViyzt1mLsj+jcYZv2xbcsPS7/LG6bW+24DTnh61Tpd3jr9VAlqUF/vWtJ7Vxa3bh17AeQzl2x6chwDx+BJlC3Yr+g==","ciphertext":"q01r4+Kkv2DiczxhkFC+AHOi2ru5djNOoY4RfF2R5hADtYelZebpXS7T23zgJtxc7L/4TJ+UZIbxKjfnNfj9"}",
    "privateKey": "-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC9E2ll8K9E314m
jPfFkDBmImKFyvnqBJnqHukcAteqs99kK5QSx5wmg7PUw/9Ti/HTOr2V6lgXy6d+
XbZl3XjCaFkmgTgKF9Zz8TtIQVUJNlmw1ztKEFr+yILoFovNxnND5WR+Nd5BUC6W
W8sOAjswB21WthjDyVfEVSOHHRdYHcKAiF6e7yISDL5p9rcLFGjV37dvmH0DcskJ
uYNwuAXlsEi4NIC3u4hK23pP9BEkDEmf0rmbSHugTl/VyzAlUiN/wUEcGu9Rl5iD
pIar+Vnbyr8ze6RNChWKcNjCZdGgI1mLDItbPEtW1IPvtyP6ymGuUqwl+C553q2t
huCURvlrAgMBAAECggEAWua+QXhZi28oQLh9VspfunrFizVuuYfEx75crE7hiPw5
ZltdMTouZIXlK2Gfm3coqDkRdMXZ3HbY6/P6ATddG3o3gj+VxaR4Qf20VqSyUV+D
93VC1/TNCrkz1okgZaoHOJlMmzEizZvTCg7PrMh91DV957ZcaaSfQZD9J7RgyMeS
C393/TI2IBR3nFQQMuNt0Rx0uXy2/T18hNQl2eSL+L2V+oCMERRetWzn9rQMDXI7
iLmh/dxE4gcTdSIflAUonWSFH6e9o8p+yJja4J966wP+B7j2dqmFr/09gBa3djHv
Ey+nhTYpfTrfYKnnE2pcXpFHWhd1iyRls93+Mb/RwQKBgQDqCyTLa8hjeeAun7fq
2piRrFVr8NRVrFQwLmA8/3lcjXhCC80FG+SdSaZBJPD7EFDT3xePl/OnQmSHSnpR
D+vklHVPAO4n3aMa/HKFgpxasxpUqRddzL6bBFNHpBgQR9Wv6hPiDP42SS7//uQF
krduS20kKsnrpGogy48zJQLfYwKBgQDO0E+PMmshHWbWDEE7Fjoe0dZtPx7CSG0B
KXj5G+njHltUxPxodAYb95dUHQl/sFy3JpNcyBk8P+qlc/fhqojR/fE3+qK+EHjw
KW/Ka4vEegtwdTXIeG4WgpTtFOjY7qsGHSFk2rFFjDrYtCMq6IBIClqk+dueCg52
QsEHXQRwWQKBgQDBDNQa3xr5wswCaUhhdlImxsnnMU1UJcODwp0rc2d9ykuJ3wYL
0sguXVO/pGMKFJk3Smu6zBH0wzT8y5g9SS7A6xwgQJoxVAZ3+gfUzLl/rwBnGNrn
Sj1mzJiNHXOj6jz+z8v6x9DgolkcW/lmB3E6jwjFrm3D62iHCKFkBIFsFQKBgAGq
i/mLXnGV2w4+awge1bkJ18BpkcXe74Hi46aeIvRBelrke2QcCzCOfhmfYkQ1F4oi
NW257vodSbariIO47AFFGnxo+Iave0n0C4KF+0pJ8W2mhBhpX/muc6S1VmrpAVe7
RFmbqXH1/0NfsCjYVrA95R0PJkXPru4k+4kjprWBAoGAHtU/VXiOqSagIo3J/Bm5
yUcJdbbguV/T9PPVu/Lq8SypCd5vqmwgYRmG+mIJEd/VYRkCZn3gbqNCn5OfbJh5
G4Xatr7aofxyz2Qon/nix8Ut1+s1Npg1ugkz/atr4CZ4QArk8JmwsCReWJXCjKLX
2WObKEWjGhgwths3MrC/CDw=
-----END PRIVATE KEY-----",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
