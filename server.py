#!/usr/bin/env python3
import http.server
import json
import urllib.parse
import os

class UserAgentHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/health":
            self.send_json({"status": "healthy", "service": "UserAgentPulse API", "version": "1.0.0"})
        elif parsed.path == "/v1/parse":
            params = urllib.parse.parse_qs(parsed.query)
            ua = params.get("ua", [self.headers.get("User-Agent", "Mozilla/5.0")])[0]
            is_bot = any(b in ua.lower() for b in ["bot", "crawl", "spider", "slurp"])
            is_mobile = any(m in ua.lower() for m in ["mobile", "android", "iphone"])
            self.send_json({
                "raw_user_agent": ua,
                "is_bot": is_bot,
                "device_type": "mobile" if is_mobile else "desktop",
                "os": "Android" if "Android" in ua else ("iOS" if "iPhone" in ua else ("Windows" if "Windows" in ua else "Linux/MacOS")),
                "browser": "Chrome" if "Chrome" in ua else ("Safari" if "Safari" in ua else "Firefox")
            })
        else:
            self.send_json({"error": "Endpoint not found"}, status=404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), UserAgentHandler)
    server.serve_forever()
