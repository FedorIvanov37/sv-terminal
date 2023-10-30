from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from common.lib.constants import TermFilesPath


SERVER_ADDRESS = 'localhost'
PORT = 4242
PATH = '/specification'


class HttpSpec(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != PATH:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
            return

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        with open(TermFilesPath.SPECIFICATION) as json_file:
            self.wfile.write(json_file.read().encode())


server = HTTPServer((SERVER_ADDRESS, PORT), HttpSpec)

try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
