from pydantic import FilePath
from PyQt6.QtNetwork import QTcpSocket
from common.gui.constants.GuiFilesPath import GuiFilesPath


class ConnectionDefinitions:

    class ConnectionStatuses:
        CONNECTED: str = "Connected"
        DISCONNECTED: str = "Disconnected"
        IN_PROGRESS: str = "Connection In Progress"
        UNKNOWN: str = "Unknown"

        GREY: FilePath = GuiFilesPath.GREY_CIRCLE
        GREEN: FilePath = GuiFilesPath.GREEN_CIRCLE
        YELLOW: FilePath = GuiFilesPath.YELLOW_CIRCLE
        RED: FilePath = GuiFilesPath.RED_CIRCLE

    @staticmethod
    def get_state_description(state):
        return ConnectionDefinitions.ConnectionStatusMap.get(state, ConnectionDefinitions.ConnectionStatuses.UNKNOWN)

    @staticmethod
    def get_state_icon_path(state):
        return ConnectionDefinitions.ConnectionIconMap.get(state, ConnectionDefinitions.ConnectionStatuses.GREY)

    ConnectionStatusMap = {
        QTcpSocket.SocketState.ConnectedState: ConnectionStatuses.CONNECTED,
        QTcpSocket.SocketState.UnconnectedState: ConnectionStatuses.DISCONNECTED,
        QTcpSocket.SocketState.ConnectingState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.HostLookupState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.BoundState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.ClosingState: ConnectionStatuses.IN_PROGRESS,
        QTcpSocket.SocketState.ListeningState: ConnectionStatuses.UNKNOWN,
    }

    ConnectionIconMap = {
        QTcpSocket.SocketState.ConnectedState: GuiFilesPath.GREEN_CIRCLE,
        QTcpSocket.SocketState.UnconnectedState: GuiFilesPath.RED_CIRCLE,
        QTcpSocket.SocketState.ConnectingState: GuiFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.HostLookupState: GuiFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.BoundState: GuiFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.ClosingState: GuiFilesPath.YELLOW_CIRCLE,
        QTcpSocket.SocketState.ListeningState: GuiFilesPath.GREY_CIRCLE,
    }
