# Give your agent its own email address — MailKite's built-in inbox agent answers mail for you,
# no webhook server required.
#
# Point a route's action at the hosted `agent`: every email to the matched address is handed to an
# inbox agent that reads it and acts on your instructions — reply, file, or escalate.
#
# Run:  MAILKITE_API_KEY=mk_live_… python 04_give_your_agent_an_inbox.py
# Deps: pip install mailkite-dev

import os
from mailkite import MailKite

mk = MailKite(os.environ["MAILKITE_API_KEY"])

# The domain must already be verified (mk.createDomain + DNS + mk.verifyDomain — see the docs).
route = mk.createRoute({
    "match": "support@yourdomain.com",   # or "*@agent.yourdomain.com" for a whole subdomain
    "action": "agent",
    "agentPrompt": (
        "You are Acme's email support agent. Answer billing and account questions from our docs, "
        "keep replies short and friendly, and escalate anything you're unsure about by forwarding "
        "to team@yourdomain.com. Never share account secrets."
    ),
})
print("inbox agent live:", route)

# Test it without sending real mail — hand the agent a message directly and read its reply:
reply = mk.agent({"to": "support@yourdomain.com", "text": "Hi, how do I reset my password?"})
print("agent says:", reply)
