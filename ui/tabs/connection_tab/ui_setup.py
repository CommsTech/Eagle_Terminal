from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTextEdit, QVBoxLayout)


def setup_ui(self):
    layout = QVBoxLayout()

    # Connection settings
    conn_layout = QHBoxLayout()
    conn_layout.addWidget(QLabel("Connection Type:"))
    self.connection_type_combo = QComboBox()
    self.connection_type_combo.addItems(["SSH", "Serial"])
    conn_layout.addWidget(self.connection_type_combo)
    layout.addLayout(conn_layout)

    # Host/Port inputs
    host_layout = QHBoxLayout()
    host_layout.addWidget(QLabel("Host:"))
    self.host_input = QLineEdit()
    host_layout.addWidget(self.host_input)
    host_layout.addWidget(QLabel("Port:"))
    self.port_input = QLineEdit()
    host_layout.addWidget(self.port_input)
    layout.addLayout(host_layout)

    # Username/Password inputs
    cred_layout = QHBoxLayout()
    cred_layout.addWidget(QLabel("Username:"))
    self.username_input = QLineEdit()
    cred_layout.addWidget(self.username_input)
    cred_layout.addWidget(QLabel("Password:"))
    self.password_input = QLineEdit()
    self.password_input.setEchoMode(QLineEdit.Password)
    cred_layout.addWidget(self.password_input)
    layout.addLayout(cred_layout)

    # Connect button
    self.connect_button = QPushButton("Connect")
    layout.addWidget(self.connect_button)

    # Terminal
    self.terminal = QTextEdit()
    self.terminal.setReadOnly(True)
    layout.addWidget(self.terminal)

    # Command input
    self.command_input = QLineEdit()
    layout.addWidget(self.command_input)

    self.setLayout(layout)
