from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWizard,
    QWizardPage,
)


class NewConnectionWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Connection")
        self.addPage(ConnectionDetailsPage())
        self.addPage(AuthenticationPage())

    def get_connection_data(self):
        return {
            "name": self.field("name"),
            "hostname": self.field("hostname"),
            "port": self.field("port"),
            "username": self.field("username"),
            "password": self.field("password"),
            "key_file": self.field("key_file"),
            "connection_type": self.field("connection_type"),
            "os_type": self.field("os_type"),
        }

    def get_session_data(self):
        return {
            "name": self.field("name"),
            "hostname": self.field("hostname"),
            "username": self.field("username"),
            "password": self.field("password"),
            "port": self.field("port"),
            "connection_type": "SSH",  # Assuming SSH for now, adjust if needed
        }


class ConnectionDetailsPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Connection Details")
        self.setSubTitle("Please enter the details for the new connection.")

        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        self.registerField("name*", self.name_edit)
        layout.addWidget(QLabel("Connection Name:"))
        layout.addWidget(self.name_edit)

        self.hostname_edit = QLineEdit()
        self.registerField("hostname*", self.hostname_edit)
        layout.addWidget(QLabel("Hostname or IP:"))
        layout.addWidget(self.hostname_edit)

        self.port_edit = QLineEdit()
        self.port_edit.setText("22")  # Default SSH port
        self.registerField("port*", self.port_edit)
        layout.addWidget(QLabel("Port:"))
        layout.addWidget(self.port_edit)

        self.connection_type = QComboBox()
        self.connection_type.addItems(["SSH", "Telnet", "Serial"])
        self.registerField("connection_type*", self.connection_type, "currentText")
        layout.addWidget(QLabel("Connection Type:"))
        layout.addWidget(self.connection_type)

        self.os_type = QComboBox()
        self.os_type.addItems(["Linux", "Windows", "macOS", "Cisco IOS", "Other"])
        self.registerField("os_type*", self.os_type, "currentText")
        layout.addWidget(QLabel("OS Type:"))
        layout.addWidget(self.os_type)

        self.setLayout(layout)

        # Connect signals to update completeness
        self.name_edit.textChanged.connect(self.completeChanged)
        self.hostname_edit.textChanged.connect(self.completeChanged)
        self.port_edit.textChanged.connect(self.completeChanged)
        self.connection_type.currentTextChanged.connect(self.completeChanged)
        self.os_type.currentTextChanged.connect(self.completeChanged)

    def isComplete(self):
        return bool(
            self.name_edit.text()
            and self.hostname_edit.text()
            and self.port_edit.text()
            and self.connection_type.currentText()
            and self.os_type.currentText()
        )


class AuthenticationPage(QWizardPage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Authentication")
        self.setSubTitle("Please enter your authentication details.")

        layout = QVBoxLayout()

        self.username_edit = QLineEdit()
        self.registerField("username*", self.username_edit)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.registerField("password", self.password_edit)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_edit)

        self.key_file_edit = QLineEdit()
        self.registerField("key_file", self.key_file_edit)
        layout.addWidget(QLabel("Key File (optional):"))
        layout.addWidget(self.key_file_edit)

        self.setLayout(layout)

        # Connect signal to update completeness
        self.username_edit.textChanged.connect(self.completeChanged)

    def isComplete(self):
        return bool(self.username_edit.text())
