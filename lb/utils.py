import http.server


def set_headers(server: http.server.BaseHTTPRequestHandler):
    server.send_response(200)
    server.send_header("Content-type", "text/plain")
    server.end_headers()


def log_message(server: http.server.BaseHTTPRequestHandler, fmt, *args):
    msg = (f"Client: {server.client_address[0]}; Method: {server.command}; "
           f"Protocol: {server.protocol_version};\n{server.headers}")
    print(msg)
