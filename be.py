#!python3.12
import argparse
import http.server
import sys

from lb.utils import log_message, set_headers


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log_message(self, fmt, *args)

    def do_GET(self):
        set_headers(self)
        self.wfile.write(b"Hello")
        print("Replied with 200: hello\n")


def run_server(args):
    port = args.port

    try:
        with http.server.HTTPServer(("", port), Handler) as httpd:
            print(f"Backend server listening on port {port}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")


def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--port", type=int, default=3000)

    return parser.parse_args(args)


if __name__ == "__main__":
    run_server(parse_args(sys.argv[1:]))
