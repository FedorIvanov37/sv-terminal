from PyQt5.QtCore import QObject, pyqtSignal
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer, HTTPServer
from common.app.decorators.singleton import singleton


json = '''{
  "config": {
    "generate_fields": [
      "4",
      "7",
      "11",
      "12",
      "37"
    ],
    "max_amount": 100
  },
  "transaction": {
    "id": "default_transaction_id",
    "message_type_indicator": "0200",
    "fields": {
      "2": "5486736712458564",
      "3": "000000",
      "4": "000000007612",
      "7": "0712142218",
      "11": "181352",
      "12": "191210155656",
      "14": "2504",
      "18": "8999",
      "22": "810",
      "37": "687812337229",
      "41": "70000014",
      "42": "FACIL01        ",
      "43": "PSP*merch.com               >Limassol>CY",
      "47": {
        "038": {
          "01": "00000239626",
          "03": "000000010000396",
          "04": "Limassol",
          "05": "3107",
          "06": "196",
          "07": "merch.com",
          "08": "PSP"
        },
        "033": "5",
        "027": "30303030433032445531325350334c48474b564c",
        "028": "00000308254236854496634394423610b892eb6a",
        "030": "2"
      },
      "48": {
        "51": "SOME ONE",
        "96": "415481%8164",
        "54": "HOW ARE YOU",
        "76": "10000001",
        "42": "01",
        "92": "000"
      },
      "49": "978"
    }
  }
}'''


class TerminalApi(BaseHTTPRequestHandler):
    def do_POST(self):
        if not self.path.endswith('/api/send-transaction'):
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            return

        content_length = int(self.headers['Content-Length'])
        raw_message = self.rfile.read(content_length)
        api = Api()
        api.emit_message(raw_message)
        
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json, "utf-8"))


@singleton
class Api(QObject):
    _api_has_message: pyqtSignal = pyqtSignal(bytes)

    @property
    def api_has_message(self):
        return self._api_has_message

    def __init__(self):
        QObject.__init__(self)

        self.setup()

    def setup(self):
        ...

    def emit_message(self, message):
        self.api_has_message.emit(message)
