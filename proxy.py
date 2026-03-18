#!/usr/bin/env python3
"""
Marketing That Pays — Claude API Proxy
Sits between advisor.html and the Anthropic API.
Keeps your API key server-side. Deploy on Opalstack.
"""

import json
import os
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
PORT = int(os.environ.get("PORT", 8080))
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://tr3mediasolutions.com")


class ProxyHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # silence default access logs

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", ALLOWED_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_response(404)
            self.end_headers()
            return

        if not API_KEY:
            self._error(500, "API key not configured")
            return

        length = int(self.headers.get("Content-Length", 0))
        if length > 32_000:
            self._error(400, "Request too large")
            return

        try:
            body = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self._error(400, "Invalid JSON")
            return

        # Only pass through what we need — nothing else
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

    def _error(self, code, msg):
        body = json.dumps({"error": msg}).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_cors()
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    if not API_KEY:
        print("WARNING: ANTHROPIC_API_KEY not set")
    server = HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    print(f"Proxy running on port {PORT}")
    server.serve_forever()
