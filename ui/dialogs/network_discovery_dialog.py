from PyQt5.QtWidgets import (QButtonGroup, QDialog, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QRadioButton, QVBoxLayout)


class NetworkDiscoveryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Network Discovery")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Network input
        self.network_input = QLineEdit()
        layout.addWidget(QLabel("Enter IP, IP Range, or CIDR:"))
        layout.addWidget(self.network_input)

        # Scan type selection
        scan_type_layout = QHBoxLayout()
        self.ip_radio = QRadioButton("Single IP")
        self.range_radio = QRadioButton("IP Range")
        self.cidr_radio = QRadioButton("CIDR")
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.ip_radio)
        self.button_group.addButton(self.range_radio)
        self.button_group.addButton(self.cidr_radio)
        scan_type_layout.addWidget(self.ip_radio)
        scan_type_layout.addWidget(self.range_radio)
        scan_type_layout.addWidget(self.cidr_radio)
        layout.addLayout(scan_type_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.scan_button = QPushButton("Scan")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.scan_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect signals
        self.scan_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_network_input(self):
        return self.network_input.text()

    def get_scan_type(self):
        if self.ip_radio.isChecked():
            return "IP"
        elif self.range_radio.isChecked():
            return "Range"
        elif self.cidr_radio.isChecked():
            return "CIDR"
        else:
            return None
