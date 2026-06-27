# Receive inbound email as a webhook — and VERIFY the HMAC signature before trusting it.
#
# MailKite POSTs a signed `email.received` event to your URL. Always verify the
# `x-mailkite-signature` header against your webhook secret so inbound mail can't be forged.
#
# Run:  MAILKITE_WEBHOOK_SECRET=whsec_… flask --app 02_receive_webhook run --port 3000
# Deps: pip install mailkite-dev flask

import os, json
from flask import Flask, request
from mailkite import MailKite

mk = MailKite(os.environ.get("MAILKITE_API_KEY", "unused-for-verify"))
SECRET = os.environ["MAILKITE_WEBHOOK_SECRET"]

app = Flask(__name__)


@app.post("/hooks/mailkite")
def hook():
    raw = request.get_data(as_text=True)  # the RAW body — re-serialized JSON breaks the HMAC
    # verifyWebhook(signature, payload, secret, toleranceMs?) — positional.
    if not mk.verifyWebhook(request.headers.get("x-mailkite-signature"), raw, SECRET):
        return "bad signature", 401

    event = json.loads(raw)
    if event.get("type") == "email.received":
        m = event.get("message", event)
        print(f"📬 {m['from']} → {m['to']}: {m['subject']}")
        # …store it, notify a channel, kick off a workflow…

    return {"status": "ok"}  # 200 acknowledges; return a control body to mark spam / drop / block
