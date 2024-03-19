#!python3.12
import argparse
import http.server
import sys
import threading
import time
from http import HTTPStatus

import requests

from lb.utils import set_headers, log_message

servers: dict[str, bool] | None = None
DEFAULT_HEALTHCHECK_INTERVAL: int = 10
DEFAULT_PORT = 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    _last_used_server = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log_message(self, fmt, *args):
        log_message(self, fmt, *args)

    @staticmethod
    def _get_next_server():
        servers_list = list(servers.keys())

        for i in range(Handler._last_used_server + 1, len(servers)):
            if servers[servers_list[i]]:
                Handler._last_used_server = i
                return servers_list[i]

        for i in range(Handler._last_used_server + 1):
            if servers[servers_list[i]]:
                Handler._last_used_server = i
                return servers_list[i]

        raise RuntimeError("No active backend")

    def do_GET(self):
        server = self._get_next_server()

        print(f"Forwarding request to {server}\n")
        response = requests.get(server)
        print(f"Response from server: {HTTPStatus(response.status_code)}: {response.text}\n")

        set_headers(self)
        self.wfile.write(response.content)


def do_healthcheck(server):
    try:
        response = requests.get(server)
        response.raise_for_status()
        servers[server] = True
    except Exception as exc:
        print(f"{server} failed healthcheck. Exception: {exc}")
        servers[server] = False


def do_healthchecks(healthcheck_interval):
    while True:
        print("Healthchecking...")
        [do_healthcheck(server) for server in servers.keys()]
        time.sleep(healthcheck_interval)


def run_healthcheck_thread(healthcheck_interval: int):
    assert healthcheck_interval > 0

    thread = threading.Thread(target=do_healthchecks, args=(healthcheck_interval,))
    thread.start()


def run_server(port: int):
    assert port > 0

    try:
        with http.server.ThreadingHTTPServer(("", port), Handler) as httpd:
            print(f"Load-balancer server listening on port {port}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--healthcheck-interval", "-T", type=int, default=DEFAULT_HEALTHCHECK_INTERVAL)
    parser.add_argument("servers", nargs="+", type=str)

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    servers = {server: True for server in args.servers}
    run_healthcheck_thread(args.healthcheck_interval)
    run_server(args.port)
