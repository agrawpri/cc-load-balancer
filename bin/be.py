#!python3.12
import http.server
import sys

from utils import log_message, set_headers


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        log_message(self, fmt, *args)

    def do_GET(self):
        set_headers(self)
        self.wfile.write(b"Hello")
        print("Replied with 200: hello\n")


def run_server(port, handler):
    try:
        with http.server.HTTPServer(("", port), handler) as httpd:
            print(f"Backend server listening on port {port}...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")


if __name__ == "__main__":
    run_server(port=int(sys.argv[1]), handler=Handler)
