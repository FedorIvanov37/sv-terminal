from dataclasses import dataclass
from socket import socket
from time import sleep


@dataclass
class Config:
    SERVER = True
    PORT = 16677
    ADDRESS = ''


def get_connector():
    sock = socket()
    sock.bind((Config.ADDRESS, Config.PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    return conn


connection = get_connector()


while True:
    data = connection.recv(1024)

    if not data:
        print(connection)
        connection = get_connector()

    print(data)
