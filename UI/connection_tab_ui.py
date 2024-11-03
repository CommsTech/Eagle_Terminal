from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ConnectionTabUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Connection type
        self.connection_type = QComboBox()
        self.connection_type.addItems(["SSH", "Telnet", "Serial"])
        layout.addWidget(self.connection_type)

        # Connection details
        self.connection_details = QFormLayout()
        self.host_input = QLineEdit()
        self.port_input = QLineEdit("22")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.connection_details.addRow("Host:", self.host_input)
        self.connection_details.addRow("Port:", self.port_input)
        self.connection_details.addRow("Username:", self.username_input)
        self.connection_details.addRow("Password:", self.password_input)

        layout.addLayout(self.connection_details)

        # Connect button
        self.connect_button = QPushButton("Connect")
        layout.addWidget(self.connect_button)

        # Terminal output
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        layout.addWidget(self.terminal)

        # Command input
        self.command_input = QLineEdit()
        layout.addWidget(self.command_input)

        # Macro buttons
        macro_layout = QHBoxLayout()
        self.record_macro_button = QPushButton("Record Macro")
        self.play_macro_button = QPushButton("Play Macro")
        macro_layout.addWidget(self.record_macro_button)
        macro_layout.addWidget(self.play_macro_button)
        layout.addLayout(macro_layout)
