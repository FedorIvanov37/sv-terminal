from PyQt5.QtNetwork import QTcpSocket


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
        QTcpSocket.ConnectedState: CONNECTED,
        QTcpSocket.UnconnectedState: DISCONNECTED,
        QTcpSocket.ConnectingState: IN_PROGRESS,
        QTcpSocket.HostLookupState: IN_PROGRESS,
        QTcpSocket.BoundState: IN_PROGRESS,
        QTcpSocket.ClosingState: IN_PROGRESS,
        QTcpSocket.ListeningState: UNKNOWN
    }

    COLOR_MAP = {
        QTcpSocket.ConnectedState: GREEN,
        QTcpSocket.UnconnectedState: RED,
        QTcpSocket.ConnectingState: YELLOW,
        QTcpSocket.HostLookupState: YELLOW,
        QTcpSocket.BoundState: YELLOW,
        QTcpSocket.ClosingState: YELLOW,
        QTcpSocket.ListeningState: GREEN
    }

    @staticmethod
    def get_state_description(state):
        return ConnectionStatus.STATE_MAP.get(state, ConnectionStatus.UNKNOWN)

    @staticmethod
    def get_state_color(state):
        return ConnectionStatus.COLOR_MAP.get(state, ConnectionStatus.GREY)
