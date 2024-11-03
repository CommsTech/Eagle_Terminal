from PyQt5.QtCore import QObject, pyqtSignal


class ConnectionHandler(QObject):
    output_received = pyqtSignal(str)
    connection_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.connected = False

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def send_command(self, command):
        raise NotImplementedError
