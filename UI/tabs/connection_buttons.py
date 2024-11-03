from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

from ui.main_window.device_management import DeviceManagement


class ConnectionButtons(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.device_management = DeviceManagement(main_window)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.parent.connect)
        layout.addWidget(connect_button)

        disconnect_button = QPushButton("Disconnect")
        disconnect_button.clicked.connect(self.parent.disconnect)
        layout.addWidget(disconnect_button)

        self.setLayout(layout)

    def on_connection_success(self, device_info):
        print(f"Connection successful. Device info: {device_info}")
        self.device_management.add_device(device_info)
