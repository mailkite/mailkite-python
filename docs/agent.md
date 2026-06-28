# `agent`

Send a message to one of your inbox agents and get its reply. Defaults to the account's default agent; pass `routeId` or `address` to target a specific agent, or `model` to override the model. This is separate from inbound routing — it does not match or override routes.

**HTTP:** `POST /v1/agent`

## Parameters

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | ✓ | The message for the agent — it reads this as the incoming email body and decides what to… |
| `subject` | string |  | Optional subject line the agent sees on the message. |
| `from` | string |  | Optional sender address the agent sees as the originator. Defaults to the account's API… |
| `html` | string |  | Optional HTML body. `text` is still required — the agent reasons over the plain-text… |
| `routeId` | string |  | Target a specific agent by its route id (rte_…). Omit to use the account's default agent… |
| `address` | string |  | Target the agent whose route matches this address. Alternative to routeId. |
| `model` | string |  | Override the model the agent runs on for this call (e.g. claude-sonnet-4-6). |

## Returns

`agent-response` — see the [`agent-response`](https://mailkite.dev/docs/api-reference) schema.

## Example

```python
res = mk.agent({
    "text": "What's my current balance?",
})
```

---

[← All methods](../README.md#api-methods) · [Docs](https://mailkite.dev/docs) · [mailkite.dev](https://mailkite.dev)
