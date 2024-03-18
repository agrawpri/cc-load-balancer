#!python3.12
import http.server
from http import HTTPStatus

import requests

from utils import set_headers, log_message

SERVERS = ["http://localhost:3000", "http://localhost:3001"]


class Handler(http.server.SimpleHTTPRequestHandler):
    _next_server = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_message(self, fmt, *args):
        log_message(self, fmt, *args)

    def do_GET(self):
        server = SERVERS[Handler._next_server]
        print(f"Forwarding request to {server}\n")

        response = requests.get(server)
        print(f"Response from server: {HTTPStatus(response.status_code)}: {response.text}\n")

        set_headers(self)
        self.wfile.write(response.content)
        Handler._next_server = (Handler._next_server + 1) % len(SERVERS)
        print(f"{Handler._next_server}")


def run_server(port, handler):
    try:
        with http.server.ThreadingHTTPServer(("", port), handler) as httpd:
            print(f"Load-balancer server listening on port {port}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")


if __name__ == "__main__":
    run_server(port=8000, handler=Handler)
