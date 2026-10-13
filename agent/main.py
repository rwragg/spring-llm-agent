"""HTTP service exposing the LLM agent — stdlib only (no FastAPI).

Why stdlib: Python 3.14 has no prebuilt wheel for pydantic-core (a FastAPI
dependency), so FastAPI won't install cleanly on this machine. A tiny
http.server handler gives the same REST surface with zero build risk.

Spring Boot's backend calls POST /agent/ask with a JSON body:
    {"prompt": "Explain dependency injection"}
and receives:
    {"prompt": "...", "model": "...", "answer": "...", "error": null}
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agent import ask

HOST = "0.0.0.0"
PORT = 8000


class AgentHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 - http.server API
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802 - http.server API
        if self.path != "/agent/ask":
            self._send_json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            body = json.loads(raw) if raw else {}
            prompt = body.get("prompt", "")
            model = body.get("model", "llama3.2")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "invalid JSON body"})
            return

        result = ask(prompt, model)
        self._send_json(200, result)

    def log_message(self, *args) -> None:  # quiet the default request logging
        pass


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), AgentHandler)
    print(f"Agent service listening on http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()