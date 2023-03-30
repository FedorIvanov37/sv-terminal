from typing import Optional
from socket import socket
from time import sleep
from pydantic import BaseModel


class Config(BaseModel):
    address: str = str()
    port: int = 16677
    is_server: bool = True
    separator: str = ">>>>"


class TerminalSocket(object):
    _config: Config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    def __init__(self, config: Optional[Config] = None):
        if config is None:
            config = Config()

        self.config = config

    def run_server(self) -> None:
        if not self.config.is_server:
            raise TypeError("The socket was run not in server mode")

        sock = socket()
        sock.bind((self.config.address, self.config.port))
        sock.listen(1)
        conn, addr = sock.accept()

        while True:
            data = conn.recv(1024)

            if not data:
                sleep(1)
                conn, addr = sock.accept()

            print(self.config.separator)
            print("\n%s\n" % data)

    # TODO
    def run_client(self):
        pass


config = Config()
terminal_socket = TerminalSocket(config)
terminal_socket.run_server()
