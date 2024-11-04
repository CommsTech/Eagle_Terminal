import logging
import socket

from PyQt5.QtWidgets import (QListWidget, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)

logging.basicConfig(level=logging.ERROR)


class NetworkDiscovery(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.device_list = QListWidget()
        layout.addWidget(self.device_list)

        scan_button = QPushButton("Scan Network")
        scan_button.clicked.connect(self.scan_network)
        layout.addWidget(scan_button)

        self.setLayout(layout)

    def scan_network(self):
        ip_range = self.ip_range_input.text()
        try:
            devices = scan_network(ip_range)
            self.update_device_list(devices)
        except ValueError as e:
            logging.error(f"Invalid IP range: {str(e)}")
            QMessageBox.warning(self, "Invalid IP Range", str(e))
        except Exception as e:
            logging.error(f"Network scan failed: {str(e)}")
            QMessageBox.critical(
                self,
                "Scan Failed",
                f"An error occurred during the network scan: {str(e)}",
            )
