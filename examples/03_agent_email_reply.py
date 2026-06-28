# An AI email agent: inbound email → Claude drafts a reply → MailKite sends it, threaded.
# Give your product an inbox that answers itself.
#
# Flow: MailKite POSTs the inbound `email.received` event → verify it → Claude composes a concise
# reply → send it back with `inReplyTo` so it threads to the sender.
#
# Run:  MAILKITE_API_KEY=mk_live_… MAILKITE_WEBHOOK_SECRET=whsec_… ANTHROPIC_API_KEY=sk-ant-… \
#       flask --app 03_agent_email_reply run --port 3000
# Deps: pip install mailkite-dev flask anthropic

import os, json
from flask import Flask, request
from mailkite import MailKite
import anthropic

mk = MailKite(os.environ["MAILKITE_API_KEY"])
claude = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
SECRET = os.environ["MAILKITE_WEBHOOK_SECRET"]

SYSTEM = (
    "You are the support agent for Acme. Read the customer's email and write a short, friendly "
    "reply that directly answers them. Plain text. If you can't help, say a human will follow up."
)

app = Flask(__name__)


@app.post("/hooks/mailkite")
def hook():
    raw = request.get_data(as_text=True)  # verify against the RAW body — re-serialized JSON breaks the HMAC
    if not mk.verifyWebhook(request.headers.get("x-mailkite-signature"), raw, SECRET):  # (signature, payload, secret)
        return "bad signature", 401

    event = json.loads(raw)
    if event.get("type") != "email.received":
        return {"status": "ok"}
    m = event.get("message", event)  # { from, to, subject, text, html, messageId, … }

    # 1. Claude drafts the reply.
    msg = claude.messages.create(
        model="claude-opus-4-8",  # swap to claude-sonnet-4-6 / claude-haiku-4-5 for lower cost
        max_tokens=1024,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"From: {m['from']}\nSubject: {m['subject']}\n\n{m.get('text') or m.get('html')}"}],
    )
    reply = next((b.text for b in msg.content if b.type == "text"), "Thanks — a human will follow up.")

    # 2. Send it back, threaded to the original.
    mk.send({
        "from": m["to"],  # reply from the address that received the mail
        "to": m["from"],
        "subject": m["subject"] if str(m["subject"]).startswith("Re:") else f"Re: {m['subject']}",
        "text": reply,
        "inReplyTo": m["messageId"],
    })
    print(f"🤖 replied to {m['from']}")
    return {"status": "ok"}
