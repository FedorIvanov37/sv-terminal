from dataclasses import dataclass
from PyQt6.QtNetwork import QTcpSocket


@dataclass(frozen=True)
class ConnectionDefinitions:

    @dataclass(frozen=True)
    class ConnectionStatuses:
        CONNECTED: str = "SVFE Connected"
        DISCONNECTED: str = "SVFE Disconnected"
        IN_PROGRESS: str = "SVFE Connection In Progress"
        UNKNOWN: str = "Unknown"

        # RGB
        GREY = (128, 128, 128)
        YELLOW = (255, 165, 0)
        RED = (224, 64, 6)
        GREEN = (166, 215, 133)

    @staticmethod
    def get_state_description(state):
        return ConnectionDefinitions.ConnectionStatusMap.get(state, ConnectionDefinitions.ConnectionStatuses.UNKNOWN)

    @staticmethod
    def get_state_color(state):
        return ConnectionDefinitions.ConnectionColorMap.get(state, ConnectionDefinitions.ConnectionStatuses.GREY)

    ConnectionStatusMap = {
        QTcpSocket.SocketState.ConnectedState: ConnectionStatuses.CONNECTED,
        QTcpSocket.SocketState.UnconnectedState: ConnectionStatuses.DISCONNECTED,
        QTcpSocket.SocketState.ConnectingState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.HostLookupState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.BoundState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.ClosingState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.ListeningState: ConnectionStatuses.UNKNOWN,
    }

    ConnectionColorMap = {
        QTcpSocket.SocketState.ConnectedState: ConnectionStatuses.GREEN,
        QTcpSocket.SocketState.UnconnectedState: ConnectionStatuses.RED,
        QTcpSocket.SocketState.ConnectingState: ConnectionStatuses.YELLOW,
        QTcpSocket.SocketState.HostLookupState: ConnectionStatuses.YELLOW,
        QTcpSocket.SocketState.BoundState: ConnectionStatuses.YELLOW,
        QTcpSocket.SocketState.ClosingState: ConnectionStatuses.YELLOW,
        QTcpSocket.SocketState.ListeningState: ConnectionStatuses.GREEN,
    }
