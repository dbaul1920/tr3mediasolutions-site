#!/usr/bin/env python3
"""
Marketing That Pays — Backend Proxy
Routes:
  POST /api/chat       — Claude API proxy for advisor chat
  POST /api/quiz       — Store quiz results + push to Mailchimp
  POST /api/subscribe  — Email-only subscribe (landing page) + Mailchimp

Keeps API keys server-side. Deploy on Opalstack.
"""

import hashlib
import json
import os
import sqlite3
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY", "")
MAILCHIMP_LIST_ID = os.environ.get("MAILCHIMP_LIST_ID", "")
MAILCHIMP_DC = os.environ.get("MAILCHIMP_DC", "us21")  # datacenter from API key suffix
PORT = int(os.environ.get("PORT", 8080))
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://tr3mediasolutions.com")
DB_PATH = os.environ.get("DB_PATH", "mtp_data.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            tier TEXT,
            score INTEGER,
            answers TEXT,
            frustration TEXT,
            source TEXT DEFAULT 'quiz',
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            source TEXT,
            tier TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def save_quiz_result(email, tier, score, answers, frustration):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO quiz_results (email, tier, score, answers, frustration) VALUES (?, ?, ?, ?, ?)",
        (email, tier, score, json.dumps(answers), frustration)
    )
    conn.commit()
    conn.close()


def save_subscriber(email, source, tier=""):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO subscribers (email, source, tier) VALUES (?, ?, ?)",
        (email, source, tier)
    )
    conn.commit()
    conn.close()


def mailchimp_subscribe(email, tier="", score=0, frustration="", source="quiz"):
    """Add/update subscriber in Mailchimp with MTP tags."""
    if not MAILCHIMP_API_KEY or not MAILCHIMP_LIST_ID:
        return

    email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
    url = f"https://{MAILCHIMP_DC}.api.mailchimp.com/3.0/lists/{MAILCHIMP_LIST_ID}/members/{email_hash}"

    tags = [source, f"mtp-{tier}"] if tier else [source]

    payload = {
        "email_address": email,
        "status_if_new": "subscribed",
        "merge_fields": {
            "MTP_TIER": tier.upper() if tier else "",
            "MTP_SCORE": str(score),
            "MTP_FRUST": frustration,
            "MTP_SRC": source,
        },
        "tags": tags,
    }

    import base64
    auth = base64.b64encode(f"anystring:{MAILCHIMP_API_KEY}".encode()).decode()

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth}",
        },
        method="PUT",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
    except urllib.error.HTTPError as e:
        print(f"Mailchimp error {e.code}: {e.read().decode()[:200]}")
    except urllib.error.URLError as e:
        print(f"Mailchimp connection error: {e.reason}")


class ProxyHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def _read_body(self, max_size=32_000):
        length = int(self.headers.get("Content-Length", 0))
        if length > max_size:
            return None
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return None

    def do_POST(self):
        if self.path == "/api/chat":
            self._handle_chat()
        elif self.path == "/api/quiz":
            self._handle_quiz()
        elif self.path == "/api/subscribe":
            self._handle_subscribe()
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_chat(self):
        if not API_KEY:
            self._error(500, "API key not configured")
            return

        body = self._read_body()
        if body is None:
            self._error(400, "Invalid or oversized request")
            return

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1000,
            "system": body.get("system", ""),
            "messages": body.get("messages", [])
        }

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors()
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self._error(e.code, e.read().decode())
        except urllib.error.URLError as e:
            self._error(502, str(e.reason))

    def _handle_quiz(self):
        body = self._read_body(8_000)
        if body is None:
            self._error(400, "Invalid request")
            return

        email = body.get("email", "").strip()
        tier = body.get("tier", "")
        score = body.get("score", 0)
        answers = body.get("answers", [])
        frustration = body.get("frustration", "")

        if email:
            save_quiz_result(email, tier, score, answers, frustration)
            mailchimp_subscribe(email, tier=tier, score=score, frustration=frustration, source="quiz")

        self._json_response({"ok": True, "tier": tier})

    def _handle_subscribe(self):
        body = self._read_body(4_000)
        if body is None:
            self._error(400, "Invalid request")
            return

        email = body.get("email", "").strip()
        source = body.get("source", "landing-page")
        tier = body.get("tier", "")

        if email:
            save_subscriber(email, source, tier)
            mailchimp_subscribe(email, tier=tier, source=source)

        self._json_response({"ok": True})

    def _json_response(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_cors()
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code, msg):
        self._json_response({"error": msg}, code)


if __name__ == "__main__":
    init_db()
    if not API_KEY:
        print("WARNING: ANTHROPIC_API_KEY not set")
    if not MAILCHIMP_API_KEY:
        print("WARNING: MAILCHIMP_API_KEY not set — email subscriptions will be stored locally only")
    server = HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    print(f"MTP backend running on port {PORT}")
    server.serve_forever()
