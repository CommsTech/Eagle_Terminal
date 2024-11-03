from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QCheckBox,
        QComboBox,
        QFileDialog,
        QFormLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QPushButton,
        QVBoxLayout,
        QWizard,
        QWizardPage,
    )
else:
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import (
        QCheckBox,
        QComboBox,
        QFileDialog,
        QFormLayout,
        QHBoxLayout,
        QLabel,
        QLineEdit,
        QPushButton,
        QVBoxLayout,
        QWizard,
        QWizardPage,
    )


class NewSessionWizard(QWizard):
    def __init__(self, parent=None, quick_connect=False):
        super().__init__(parent)
        self.addPage(ConnectionDetailsPage(quick_connect))
        self.setWindowTitle("New Session" if not quick_connect else "Quick Connect")

    def get_session_data(self):
        return {
            "name": self.field("name"),
            "connection_type": self.field("connection_type"),
            "host": self.field("host"),
            "port": self.field("port"),
            "username": self.field("username"),
            "password": self.field("password"),
            "use_key": self.field("use_key"),
            "key_file": self.field("key_file"),
        }


class ConnectionDetailsPage(QWizardPage):
    def __init__(self, quick_connect=False, parent=None):
        super().__init__(parent)
        self.setTitle("Connection Details")
        self.setSubTitle("Enter the details for the new connection.")

        layout = QFormLayout()

        if not quick_connect:
            self.name_input = QLineEdit()
            layout.addRow("Name:", self.name_input)
            self.connection_type = QComboBox()
            self.connection_type.addItems(["SSH", "Telnet", "Serial"])
            layout.addRow("Connection Type:", self.connection_type)

        self.host_input = QLineEdit()
        self.port_input = QLineEdit("22")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Host:", self.host_input)
        layout.addRow("Port:", self.port_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)

        if not quick_connect:
            self.use_key_checkbox = QCheckBox("Use SSH Key")
            self.key_file_input = QLineEdit()
            self.key_file_button = QPushButton("Browse")

            layout.addRow("Use SSH Key:", self.use_key_checkbox)
            key_file_layout = QHBoxLayout()
            key_file_layout.addWidget(self.key_file_input)
            key_file_layout.addWidget(self.key_file_button)
            layout.addRow("Key File:", key_file_layout)

            self.use_key_checkbox.stateChanged.connect(self.toggle_key_file)
            self.key_file_button.clicked.connect(self.browse_key_file)

        self.setLayout(layout)

        if not quick_connect:
            self.registerField("name*", self.name_input)
            self.registerField("connection_type", self.connection_type, "currentText")
            self.registerField("use_key", self.use_key_checkbox)
            self.registerField("key_file", self.key_file_input)
        else:
            self.registerField("connection_type", "SSH")

        self.registerField("host*", self.host_input)
        self.registerField("port", self.port_input)
        self.registerField("username*", self.username_input)
        self.registerField("password", self.password_input)

        if not quick_connect:
            self.toggle_key_file(Qt.Unchecked)

    def toggle_key_file(self, state):
        use_key = state == Qt.Checked
        self.password_input.setEnabled(not use_key)
        self.key_file_input.setEnabled(use_key)
        self.key_file_button.setEnabled(use_key)

    def browse_key_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select SSH Key File")
        if file_name:
            self.key_file_input.setText(file_name)
