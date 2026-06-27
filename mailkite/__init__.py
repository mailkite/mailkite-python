"""MailKite SDK for Python.

Shape shared by every MailKite SDK: one low-level ``request()`` plus one thin
method per API endpoint. Zero dependencies — uses the standard library.

    from mailkite import MailKite
    mk = MailKite(os.environ["MAILKITE_API_KEY"])
    res = mk.send({"from": ..., "to": ..., "subject": ..., "text": ...})
"""

import base64
import hashlib
import hmac
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.mailkite.dev"
# Reject webhook events older than this (ms) to block replays. Pass 0 to disable.
DEFAULT_TOLERANCE_MS = 5 * 60 * 1000

# Best-effort extension -> MIME map for raw binary attachment uploads.
_CONTENT_TYPES = {
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
    "svg": "image/svg+xml",
    "csv": "text/csv",
    "txt": "text/plain",
    "html": "text/html",
    "json": "application/json",
    "zip": "application/zip",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ics": "text/calendar",
    "ical": "text/calendar",
}


def _guess_content_type(name):
    """Guess a MIME type from a filename's extension (default octet-stream)."""
    ext = ""
    if name and "." in name:
        ext = name.rsplit(".", 1)[1].lower()
    return _CONTENT_TYPES.get(ext, "application/octet-stream")

__all__ = ["MailKite", "MailKiteError", "verify_webhook", "reply_ok", "reply_spam", "reply_drop", "reply_block_sender", "encrypt", "decrypt"]


def verify_webhook(signature, payload, secret, toleranceMs=DEFAULT_TOLERANCE_MS):
    """Verify an ``x-mailkite-signature`` header on an inbound webhook delivery.

    Local HMAC-SHA256 check — no network call. Pass the raw, unparsed body
    (``str`` or ``bytes``); the signature is over the exact bytes received.
    Returns ``True`` only when the signature matches and the event is fresh.
    """
    if not isinstance(signature, str) or not signature:
        return False
    parts = {}
    for seg in signature.split(","):
        if "=" in seg:
            k, v = seg.split("=", 1)
            parts[k.strip()] = v.strip()
    t = parts.get("t")
    v1 = parts.get("v1")
    if not t or not v1 or not t.lstrip("-").isdigit():
        return False
    # The t in the header is milliseconds since the epoch.
    if toleranceMs and toleranceMs > 0:
        if abs(time.time() * 1000 - int(t)) > toleranceMs:
            return False
    body = payload.encode("utf-8") if isinstance(payload, str) else payload
    signed = (t + ".").encode("utf-8") + body
    expected = hmac.new(secret.encode("utf-8"), signed, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, v1)


def reply_ok():
    """Return the canonical ``200 OK`` webhook acknowledgement body.

    Inbound webhook handlers should reply with this exact string so MailKite
    marks the delivery as accepted. No network call."""
    return '{"status":"ok"}'


def reply_spam():
    """Control-mode reply telling MailKite to mark the message as spam.

    Returns the exact string ``{"status":"spam"}``. No network call."""
    return '{"status":"spam"}'


def reply_drop():
    """Control-mode reply telling MailKite to drop (discard) the message.

    Returns the exact string ``{"status":"drop"}``. No network call."""
    return '{"status":"drop"}'


def reply_block_sender():
    """Control-mode reply telling MailKite to block the sender.

    Returns the exact string ``{"status":"ok","actions":[{"type":"block-sender"}]}``.
    No network call."""
    return '{"status":"ok","actions":[{"type":"block-sender"}]}'


def encrypt(plaintext, public_key):
    """Encrypt a UTF-8 string to a MailKite at-rest envelope (JSON string).

    Hybrid encryption matching MailKite's at-rest scheme: a fresh AES-256-GCM
    content key encrypts the plaintext, then that key is wrapped with the
    customer's RSA-OAEP (SHA-256) ``public_key`` (SPKI/PEM). Only the holder of
    the matching private key can :func:`decrypt`. No network call. Requires the
    ``cryptography`` package."""
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    pem = public_key.encode("utf-8") if isinstance(public_key, str) else public_key
    pub = serialization.load_pem_public_key(pem)
    spki_der = pub.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    fp = hashlib.sha256(spki_der).hexdigest()

    content_key = AESGCM.generate_key(bit_length=256)
    iv = os.urandom(12)
    # AESGCM.encrypt returns ciphertext || 16-byte tag (matches WebCrypto).
    ciphertext = AESGCM(content_key).encrypt(iv, plaintext.encode("utf-8"), None)
    wrapped = pub.encrypt(
        content_key,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    def b64(b):
        return base64.b64encode(b).decode("ascii")

    return json.dumps({
        "v": 1,
        "keyAlg": "RSA-OAEP-256",
        "fp": fp,
        "enc": "A256GCM",
        "iv": b64(iv),
        "wrappedKey": b64(wrapped),
        "ciphertext": b64(ciphertext),
    })


def decrypt(envelope, private_key):
    """Decrypt a MailKite at-rest ``envelope`` (JSON string) back to plaintext.

    Inverse of :func:`encrypt`: unwraps the AES-256-GCM content key with the
    RSA-OAEP (SHA-256) ``private_key`` (PKCS8/PEM), then decrypts the ciphertext
    (which carries its 16-byte GCM tag) and returns the UTF-8 string. No network
    call. Requires the ``cryptography`` package."""
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    env = json.loads(envelope)
    pem = private_key.encode("utf-8") if isinstance(private_key, str) else private_key
    priv = serialization.load_pem_private_key(pem, password=None)
    content_key = priv.decrypt(
        base64.b64decode(env["wrappedKey"]),
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )
    plaintext = AESGCM(content_key).decrypt(
        base64.b64decode(env["iv"]), base64.b64decode(env["ciphertext"]), None
    )
    return plaintext.decode("utf-8")


class MailKiteError(Exception):
    def __init__(self, status, message, body=None):
        super().__init__(message)
        self.status = status
        self.message = message
        self.body = body


class MailKite:
    def __init__(self, apiKey, baseUrl=DEFAULT_BASE_URL):
        self.apiKey = apiKey
        self.baseUrl = baseUrl.rstrip("/")

    # Low-level request. Every method below is a one-liner on top of this.
    def request(self, method, path, body=None):
        headers = {"Authorization": "Bearer " + self.apiKey}
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.baseUrl + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text else None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8")
            parsed = json.loads(text) if text else None
            message = parsed.get("error") if isinstance(parsed, dict) else None
            raise MailKiteError(e.code, message or e.reason or "HTTP %d" % e.code, parsed)

    # Raw-binary variant of request(): the body is the file bytes themselves
    # (not JSON, not multipart) and filename/retentionDays ride in the query.
    def requestBinary(self, method, path, data, filename, contentType=None, retentionDays=None):
        query = {"filename": filename}
        if retentionDays is not None:
            query["retentionDays"] = retentionDays
        url = self.baseUrl + path + "?" + urllib.parse.urlencode(query)
        headers = {
            "Authorization": "Bearer " + self.apiKey,
            "Content-Type": contentType or "application/octet-stream",
        }
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode("utf-8")
                return json.loads(text) if text else None
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8")
            parsed = json.loads(text) if text else None
            message = parsed.get("error") if isinstance(parsed, dict) else None
            raise MailKiteError(e.code, message or e.reason or "HTTP %d" % e.code, parsed)

    # --- Sending ----------------------------------------------------------
    def send(self, message):
        """Send an email. ``message`` is a dict with ``from``, ``to`` and a
        body (``text`` and/or ``html``). ``subject`` is optional — it may come
        from a template. Pass ``templateId`` (str) to render a stored template
        and ``templateData`` (dict) to supply its variables."""
        return self.request("POST", "/v1/send", message)

    def uploadAttachment(self, file):
        """Upload a file and get back a secure, time-limited URL to reference as
        a send() attachment (``{ filename, url }``) or link inline — instead of
        base64-inlining large files on every send. ``file`` is a dict that
        provides the file ONE of four ways (checked in this order):

        - ``url`` (str): MailKite fetches and re-hosts the remote file.
        - ``bytes`` (raw ``bytes``): uploaded directly as a raw binary body.
        - ``path`` (str): a local file read off disk, then uploaded as raw bytes;
          ``filename`` and ``contentType`` are derived from the path if omitted.
        - ``content`` (str): a base64-encoded body (the original JSON form).

        Optional in every mode: ``filename``, ``contentType`` and
        ``retentionDays`` (7 | 30 | 90 | 365, default 7). Returns
        ``{id, url, filename, contentType, size, expiresAt}``."""
        file = file or {}
        filename = file.get("filename")
        content = file.get("content")
        url = file.get("url")
        path = file.get("path")
        data = file.get("bytes")
        contentType = file.get("contentType")
        retentionDays = file.get("retentionDays")
        if url is not None:
            body = {"url": url}
            if filename is not None:
                body["filename"] = filename
            if contentType is not None:
                body["contentType"] = contentType
            if retentionDays is not None:
                body["retentionDays"] = retentionDays
            return self.request("POST", "/v1/attachments", body)
        if data is not None or path is not None:
            name = filename
            ctype = contentType
            if data is None:
                with open(path, "rb") as f:
                    data = f.read()
                if not name:
                    name = os.path.basename(path)
                if not ctype:
                    ctype = _guess_content_type(name)
            return self.requestBinary("POST", "/v1/attachments", data, name, ctype, retentionDays)
        if content is not None:
            body = {"content": content}
            if filename is not None:
                body["filename"] = filename
            if contentType is not None:
                body["contentType"] = contentType
            if retentionDays is not None:
                body["retentionDays"] = retentionDays
            return self.request("POST", "/v1/attachments", body)
        raise MailKiteError(0, "uploadAttachment needs one of: path, bytes, url, or base64 content")

    def agent(self, message):
        """Send a message to an AI agent inbox. ``message`` is a dict with
        ``text`` (required) and optional ``subject``, ``from``, ``html``,
        ``routeId``, ``address`` and ``model``."""
        return self.request("POST", "/v1/agent", message)

    def route(self, message):
        """Route a message. ``message`` is a dict with ``from`` (required) and
        optional ``routeId``, ``address``, ``subject``, ``text`` and ``html``."""
        return self.request("POST", "/v1/route", message)

    # --- Templates --------------------------------------------------------
    def listTemplates(self):
        return self.request("GET", "/api/templates")

    def listBaseTemplates(self):
        return self.request("GET", "/api/templates/base")

    def getTemplate(self, id):
        return self.request("GET", "/api/templates/%s" % id)

    def createTemplate(self, body):
        return self.request("POST", "/api/templates", body)

    # --- Domains ----------------------------------------------------------
    def listDomains(self):
        return self.request("GET", "/api/domains")

    def createDomain(self, body):
        return self.request("POST", "/api/domains", body)

    def getDomain(self, id):
        return self.request("GET", "/api/domains/%s" % id)

    def deleteDomain(self, id):
        return self.request("DELETE", "/api/domains/%s" % id)

    def verifyDomain(self, id):
        return self.request("POST", "/api/domains/%s/verify" % id)

    def setWebhook(self, id, body):
        return self.request("PUT", "/api/domains/%s/webhook" % id, body)

    def deleteWebhook(self, id):
        return self.request("DELETE", "/api/domains/%s/webhook" % id)

    def testWebhook(self, id):
        return self.request("POST", "/api/domains/%s/webhook/test" % id)

    def checkDomainAvailability(self, domain):
        return self.request("GET", "/api/domains/register/check?domain=%s" % urllib.parse.quote(domain))

    def registerDomain(self, body):
        return self.request("POST", "/api/domains/register", body)

    # --- Routes -----------------------------------------------------------
    def listRoutes(self):
        return self.request("GET", "/api/routes")

    def createRoute(self, body):
        return self.request("POST", "/api/routes", body)

    # --- Messages & deliveries -------------------------------------------
    def listMessages(self):
        return self.request("GET", "/api/messages")

    def getMessage(self, id):
        return self.request("GET", "/api/messages/%s" % id)

    def retryDelivery(self, id):
        return self.request("POST", "/api/deliveries/%s/retry" % id)

    # --- Lists ------------------------------------------------------------
    def listLists(self):
        return self.request("GET", "/api/lists")

    def createList(self, body):
        return self.request("POST", "/api/lists", body)

    def getList(self, id):
        return self.request("GET", "/api/lists/%s" % id)

    def updateList(self, id, body):
        return self.request("PATCH", "/api/lists/%s" % id, body)

    def deleteList(self, id):
        return self.request("DELETE", "/api/lists/%s" % id)

    def listListContacts(self, id):
        return self.request("GET", "/api/lists/%s/contacts" % id)

    def addListContacts(self, id, body):
        return self.request("POST", "/api/lists/%s/contacts" % id, body)

    def removeListContact(self, id, contactId):
        return self.request("DELETE", "/api/lists/%s/contacts/%s" % (id, contactId))

    # --- Broadcasts -------------------------------------------------------
    def listBroadcasts(self):
        return self.request("GET", "/api/broadcasts")

    def createBroadcast(self, body):
        return self.request("POST", "/api/broadcasts", body)

    def getBroadcast(self, id):
        return self.request("GET", "/api/broadcasts/%s" % id)

    def updateBroadcast(self, id, body):
        return self.request("PATCH", "/api/broadcasts/%s" % id, body)

    def deleteBroadcast(self, id):
        return self.request("DELETE", "/api/broadcasts/%s" % id)

    def sendBroadcast(self, id, body=None):
        return self.request("POST", "/api/broadcasts/%s/send" % id, body)

    # --- Webhooks ---------------------------------------------------------
    def verifyWebhook(self, signature, payload, secret, toleranceMs=DEFAULT_TOLERANCE_MS):
        """Verify an ``x-mailkite-signature`` header. See module-level
        :func:`verify_webhook` — this is a thin instance wrapper, so you can
        call it on an existing client without re-importing."""
        return verify_webhook(signature, payload, secret, toleranceMs)

    def reply_ok(self):
        """Canonical webhook acknowledgement body. See module-level
        :func:`reply_ok`."""
        return reply_ok()

    def reply_spam(self):
        """Control-mode reply marking the message as spam. See module-level
        :func:`reply_spam`."""
        return reply_spam()

    def reply_drop(self):
        """Control-mode reply dropping the message. See module-level
        :func:`reply_drop`."""
        return reply_drop()

    def reply_block_sender(self):
        """Control-mode reply blocking the sender. See module-level
        :func:`reply_block_sender`."""
        return reply_block_sender()

    def encrypt(self, plaintext, public_key):
        """Encrypt to a MailKite at-rest envelope. See module-level
        :func:`encrypt`."""
        return encrypt(plaintext, public_key)

    def decrypt(self, envelope, private_key):
        """Decrypt a MailKite at-rest envelope. See module-level
        :func:`decrypt`."""
        return decrypt(envelope, private_key)
