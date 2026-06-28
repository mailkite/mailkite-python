# Send an email over a verified domain — the 10-second "it works".
#
# Run:  MAILKITE_API_KEY=mk_live_… python 01_send_email.py
# Deps: pip install mailkite-dev

import os
from mailkite import MailKite

mk = MailKite(os.environ["MAILKITE_API_KEY"])

res = mk.send({
    "from": "hello@yourdomain.com",  # an address on a domain you've verified
    "to": "ada@example.com",
    "subject": "Your invoice #1042",
    "html": "<p>Thanks for your order — receipt attached.</p>",
    # text, cc, bcc, replyTo, attachments, templateId, templateData all supported
})

print("sent:", res)  # → { "id": "msg_…", "status": "queued" }
