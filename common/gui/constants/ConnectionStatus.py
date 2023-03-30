from PyQt6.QtNetwork import QTcpSocket


class ConnectionStatus(object):
    CONNECTED: str = "SVFE Connected"
    DISCONNECTED: str = "SVFE Disconnected"
    IN_PROGRESS: str = "SVFE Connection In Progress"
    UNKNOWN: str = "Unknown"

    # RGB
    GREY = (195, 195, 195)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    STATE_MAP = {
        QTcpSocket.SocketState.ConnectedState: CONNECTED,
        QTcpSocket.SocketState.UnconnectedState: DISCONNECTED,
        QTcpSocket.SocketState.ConnectingState: IN_PROGRESS,
        QTcpSocket.SocketState.HostLookupState: IN_PROGRESS,
        QTcpSocket.SocketState.BoundState: IN_PROGRESS,
        QTcpSocket.SocketState.ClosingState: IN_PROGRESS,
        QTcpSocket.SocketState.ListeningState: UNKNOWN
    }

    COLOR_MAP = {
        QTcpSocket.SocketState.ConnectedState: GREEN,
        QTcpSocket.SocketState.UnconnectedState: RED,
        QTcpSocket.SocketState.ConnectingState: YELLOW,
        QTcpSocket.SocketState.HostLookupState: YELLOW,
        QTcpSocket.SocketState.BoundState: YELLOW,
        QTcpSocket.SocketState.ClosingState: YELLOW,
        QTcpSocket.SocketState.ListeningState: GREEN
    }

    @staticmethod
    def get_state_description(state):
        return ConnectionStatus.STATE_MAP.get(state, ConnectionStatus.UNKNOWN)

    @staticmethod
    def get_state_color(state):
        return ConnectionStatus.COLOR_MAP.get(state, ConnectionStatus.GREY)
