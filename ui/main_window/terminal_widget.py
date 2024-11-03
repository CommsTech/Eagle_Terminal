from PyQt5 import QtGui, QtWidgets


class TerminalWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.text_edit = QtWidgets.QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QtGui.QFont("Courier", 10))
        self.layout.addWidget(self.text_edit)

    def append_text(self, text):
        self.text_edit.append(text)

    def clear(self):
        self.text_edit.clear()

    def close_connections(self):
        # Implement cleanup for SSH connections
        if hasattr(self, "ssh_client") and self.ssh_client:
            try:
                self.ssh_client.close()
                self.ssh_client = None
            except Exception as e:
                print(f"Error closing SSH connection: {str(e)}")

        # Close any open channels
        if hasattr(self, "channel") and self.channel:
            try:
                self.channel.close()
                self.channel = None
            except Exception as e:
                print(f"Error closing SSH channel: {str(e)}")

        # Clear the terminal display
        self.clear()
