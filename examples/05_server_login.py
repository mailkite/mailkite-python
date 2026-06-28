# Server-side login + register.
#
#   A) Your OWN account: call signup (register) or login with email + password, keep the token.
#   B) YOUR USERS' accounts (multi-tenant): the OAuth 2.1 + PKCE flow — send the user to MailKite's
#      hosted page where they LOG IN OR REGISTER, then exchange the returned `code` for a token that
#      *is* that user. Register-or-login is handled on the hosted page; a new user just signs up
#      there and lands back logged in.
#
# Run:  MAILKITE_BASE_URL=https://api.mailkite.dev flask --app 05_server_login run --port 3000
#       then open http://localhost:3000/login
# Deps: pip install mailkite-dev flask requests

import os, base64, hashlib, secrets
import requests
from flask import Flask, request, redirect, jsonify
from mailkite import MailKite

ISSUER = os.environ.get("MAILKITE_BASE_URL", "https://api.mailkite.dev")
REDIRECT_URI = "http://localhost:3000/callback"


def b64url(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


# ── A) Server acting as your OWN single account (no redirect) ───────────────────────────────────
def own_account():
    r = requests.post(f"{ISSUER}/api/auth/signup", json={"email": "you@example.com", "password": os.environ["MK_PASSWORD"]})
    if r.status_code == 409:  # already registered → log in instead
        r = requests.post(f"{ISSUER}/api/auth/login", json={"email": "you@example.com", "password": os.environ["MK_PASSWORD"]})
    token = r.json()["token"]
    mk = MailKite(token)  # the session token works like an API key
    print("logged in as own account; domains:", mk.listDomains())


# ── B) OAuth login/register for YOUR USERS ───────────────────────────────────────────────────────
app = Flask(__name__)
sessions = {}  # demo store: state → {verifier, client_id}. Use a real session store in prod.


@app.get("/login")
def login():
    reg = requests.post(f"{ISSUER}/oauth/register", json={
        "client_name": "My App", "redirect_uris": [REDIRECT_URI],
        "grant_types": ["authorization_code", "refresh_token"], "response_types": ["code"],
    }).json()
    verifier = b64url(secrets.token_bytes(32))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    state = b64url(secrets.token_bytes(16))
    sessions[state] = {"verifier": verifier, "client_id": reg["client_id"]}
    params = {
        "response_type": "code", "client_id": reg["client_id"], "redirect_uri": REDIRECT_URI,
        "scope": "mcp", "state": state, "code_challenge": challenge, "code_challenge_method": "S256",
    }
    return redirect(f"{ISSUER}/oauth/authorize?" + requests.compat.urlencode(params))


@app.get("/callback")
def callback():
    sess = sessions.pop(request.args.get("state", ""), None)
    if not sess:
        return "unknown state", 400
    tok = requests.post(f"{ISSUER}/oauth/token", data={
        "grant_type": "authorization_code", "code": request.args["code"], "redirect_uri": REDIRECT_URI,
        "client_id": sess["client_id"], "code_verifier": sess["verifier"],
    }).json()
    mk = MailKite(tok["access_token"])  # now act as that user (store refresh_token to renew later)
    return jsonify({"ok": True, "message": "Logged in as the MailKite user.", "domains": mk.listDomains()})
