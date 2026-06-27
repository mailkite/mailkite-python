"""Unit tests for the MailKite Python SDK. Covers every public function:

  - request() (auth, content-type, JSON body, errors, base-url trim, empty body)
  - one thin method per endpoint (correct verb + path + body)
  - verify_webhook / verifyWebhook (valid / tampered / wrong-secret / malformed /
    replay window)

Run with:  python3 -m unittest discover -s tests
"""

import hashlib
import hmac
import json
import os
import sys
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mailkite import MailKite, MailKiteError, verify_webhook  # noqa: E402

# ---- in-process mock server -------------------------------------------------
STATE = {"status": 200, "body": {"ok": True}, "last": None}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):  # silence
        pass

    def _handle(self):
        length = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(length).decode("utf-8") if length else ""
        STATE["last"] = {
            "method": self.command,
            "path": self.path,
            "headers": {k.lower(): v for k, v in self.headers.items()},
            "raw": raw,
        }
        body = STATE["body"]
        payload = b"" if body is None else json.dumps(body).encode("utf-8")
        self.send_response(STATE["status"])
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PUT = do_DELETE = _handle


def reply(status, body):
    STATE["status"], STATE["body"] = status, body


SECRET = "whsec_mailkite_test"
PAYLOAD = '{"type":"email.received","id":"evt_123","message":"It works."}'
V1 = "3d790f831e170ddba4d001f27532bf2c1fc68ebed52eef72fe453dfa1196b03c"
HEADER = "t=1750000000000,v1=" + V1


def fresh_header(secret, body):
    t = int(time.time() * 1000)
    sig = hmac.new(secret.encode(), f"{t}.{body}".encode(), hashlib.sha256).hexdigest()
    return f"t={t},v1={sig}"


class SDKTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        port = cls.server.server_address[1]
        cls.base = f"http://127.0.0.1:{port}"
        cls.key = "mk_live_test"
        cls.mk = MailKite(cls.key, cls.base)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    # ---- constructor --------------------------------------------------------
    def test_base_url_trim(self):
        self.assertEqual(MailKite("k", "https://api.x.dev///").baseUrl, "https://api.x.dev")
        self.assertEqual(MailKite("k").baseUrl, "https://api.mailkite.dev")

    # ---- request() ----------------------------------------------------------
    def test_request_auth_and_json(self):
        reply(200, {"id": "x", "status": "queued"})
        out = self.mk.request("POST", "/v1/send", {"a": 1})
        last = STATE["last"]
        self.assertEqual(last["headers"]["authorization"], "Bearer " + self.key)
        self.assertIn("application/json", last["headers"]["content-type"])
        self.assertEqual(json.loads(last["raw"]), {"a": 1})
        self.assertEqual(out, {"id": "x", "status": "queued"})

    def test_request_no_body(self):
        reply(200, [])
        self.mk.request("GET", "/api/domains")
        self.assertEqual(STATE["last"]["raw"], "")
        self.assertNotIn("content-type", {k: v for k, v in STATE["last"]["headers"].items() if k == "content-type"})

    def test_request_empty_body_returns_none(self):
        reply(204, None)
        self.assertIsNone(self.mk.request("DELETE", "/api/x"))

    def test_request_error_maps_to_exception(self):
        reply(404, {"error": "not found"})
        with self.assertRaises(MailKiteError) as ctx:
            self.mk.request("GET", "/api/messages/nope")
        self.assertEqual(ctx.exception.status, 404)
        self.assertEqual(ctx.exception.message, "not found")
        self.assertEqual(ctx.exception.body, {"error": "not found"})

    def test_request_error_without_error_field(self):
        reply(500, {"nope": True})
        with self.assertRaises(MailKiteError) as ctx:
            self.mk.request("GET", "/x")
        self.assertEqual(ctx.exception.status, 500)

    # ---- endpoint methods ---------------------------------------------------
    def test_endpoint_methods(self):
        mk = self.mk
        cases = [
            (lambda: mk.send({"from": "a", "to": "b", "subject": "s", "text": "t"}), "POST", "/v1/send", {"from": "a", "to": "b", "subject": "s", "text": "t"}),
            (lambda: mk.listDomains(), "GET", "/api/domains", None),
            (lambda: mk.createDomain({"domain": "x.dev"}), "POST", "/api/domains", {"domain": "x.dev"}),
            (lambda: mk.getDomain("dom_1"), "GET", "/api/domains/dom_1", None),
            (lambda: mk.deleteDomain("dom_1"), "DELETE", "/api/domains/dom_1", None),
            (lambda: mk.verifyDomain("dom_1"), "POST", "/api/domains/dom_1/verify", None),
            (lambda: mk.setWebhook("dom_1", {"url": "https://h.dev"}), "PUT", "/api/domains/dom_1/webhook", {"url": "https://h.dev"}),
            (lambda: mk.deleteWebhook("dom_1"), "DELETE", "/api/domains/dom_1/webhook", None),
            (lambda: mk.testWebhook("dom_1"), "POST", "/api/domains/dom_1/webhook/test", None),
            (lambda: mk.listRoutes(), "GET", "/api/routes", None),
            (lambda: mk.createRoute({"match": "*@x", "action": "webhook", "destination": "u"}), "POST", "/api/routes", {"match": "*@x", "action": "webhook", "destination": "u"}),
            (lambda: mk.listMessages(), "GET", "/api/messages", None),
            (lambda: mk.getMessage("msg_1"), "GET", "/api/messages/msg_1", None),
            (lambda: mk.retryDelivery("dlv_1"), "POST", "/api/deliveries/dlv_1/retry", None),
        ]
        for call, method, path, body in cases:
            reply(200, {"ok": True})
            call()
            last = STATE["last"]
            self.assertEqual(last["method"], method, path)
            self.assertEqual(last["path"], path)
            if body is None:
                self.assertEqual(last["raw"], "")
            else:
                self.assertEqual(json.loads(last["raw"]), body)

    # ---- verify_webhook -----------------------------------------------------
    def test_verify_valid(self):
        self.assertTrue(verify_webhook(HEADER, PAYLOAD, SECRET, 0))
        self.assertTrue(self.mk.verifyWebhook(HEADER, PAYLOAD, SECRET, 0))

    def test_verify_bytes_payload(self):
        self.assertTrue(verify_webhook(HEADER, PAYLOAD.encode("utf-8"), SECRET, 0))

    def test_verify_tampered_body(self):
        self.assertFalse(verify_webhook(HEADER, PAYLOAD + " ", SECRET, 0))

    def test_verify_wrong_secret(self):
        self.assertFalse(verify_webhook(HEADER, PAYLOAD, "whsec_wrong", 0))

    def test_verify_malformed(self):
        for h in ["", "garbage", "t=1750000000000", "v1=" + V1, "t=nan,v1=" + V1, None]:
            self.assertFalse(verify_webhook(h, PAYLOAD, SECRET, 0))

    def test_verify_replay_window(self):
        # Fixed vector is far in the past → default 5-min window rejects it.
        self.assertFalse(verify_webhook(HEADER, PAYLOAD, SECRET))
        # Freshly signed event → passes the default window.
        self.assertTrue(verify_webhook(fresh_header(SECRET, PAYLOAD), PAYLOAD, SECRET))


if __name__ == "__main__":
    unittest.main()
