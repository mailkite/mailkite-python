# MailKite for Python

Official [MailKite](https://mailkite.dev) SDK. One low-level `request()` plus one
method per endpoint. Zero dependencies — standard library only. Python 3.7+.

## Install

```bash
pip install mailkite-dev
```

> Published as `mailkite-dev` for now (the `mailkite` name is being reclaimed). The
> import is unchanged — `from mailkite import MailKite`.

## Usage

```python
import os
from mailkite import MailKite

mk = MailKite(os.environ["MAILKITE_API_KEY"])

res = mk.send({
    "from": "hello@myapp.ai",
    "to": "ada@example.com",
    "subject": "Your invoice #1042",
    "html": "<p>Thanks! Receipt attached.</p>",
})
```

Point at a different base URL with `MailKite(key, "https://api.mailkite.dev")`.

## Methods

`send(message)`, `agent(message)`, `route(message)`, `listDomains()`, `createDomain({"domain": ...})`,
`getDomain(id)`, `deleteDomain(id)`, `verifyDomain(id)`,
`setWebhook(id, {"url": ...})`, `deleteWebhook(id)`, `testWebhook(id)`,
`checkDomainAvailability(domain)`, `registerDomain({"domain": ..., "contact": {...}})`,
`listRoutes()`, `createRoute({...})`, `listMessages()`, `getMessage(id)`,
`retryDelivery(id)`.

## Errors

```python
from mailkite import MailKiteError

try:
    mk.send(msg)
except MailKiteError as e:
    print(e.status, e.message)
```

See the [full docs](https://mailkite.dev/docs/libraries).
