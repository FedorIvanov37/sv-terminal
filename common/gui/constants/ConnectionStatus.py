from dataclasses import dataclass
from PyQt6.QtNetwork import QTcpSocket
from common.gui.constants.TermFilesPath import TermFilesPath


@dataclass(frozen=True)
class ConnectionDefinitions:

    @dataclass(frozen=True)
    class ConnectionStatuses:
        CONNECTED: str = "SVFE Connected"
        DISCONNECTED: str = "SVFE Disconnected"
        IN_PROGRESS: str = "SVFE Connection In Progress"
        UNKNOWN: str = "Unknown"

        GREY = TermFilesPath.GREY_CIRCLE
        GREEN = TermFilesPath.GREEN_CIRCLE
        YELLOW = TermFilesPath.YELLOW_CIRCLE
        RED = TermFilesPath.RED_CIRCLE

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
        QTcpSocket.SocketState.ConnectedState: TermFilesPath.GREEN_CIRCLE,
        QTcpSocket.SocketState.UnconnectedState: TermFilesPath.RED_CIRCLE,
        QTcpSocket.SocketState.ConnectingState: TermFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.HostLookupState: TermFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.BoundState: TermFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.ClosingState: TermFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.ListeningState: TermFilesPath.GREY_CIRCLE,
    }
