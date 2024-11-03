import asyncio

from PyQt5.QtWidgets import QListWidget, QPushButton, QVBoxLayout, QWidget


class Sidebar(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        new_connection_btn = QPushButton("New Connection")
        new_connection_btn.clicked.connect(
            lambda: asyncio.create_task(self.main_window.new_connection())
        )
        layout.addWidget(new_connection_btn)

        self.saved_connections = QListWidget()
        self.saved_connections.itemDoubleClicked.connect(self.connect_to_saved)
        layout.addWidget(self.saved_connections)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.main_window.open_settings)
        layout.addWidget(settings_btn)

    def connect_to_saved(self, item):
        # Implement connection to saved session
        connection_name = item.text()
        self.main_window.session_management.load_saved_session(connection_name)

    def update_saved_connections(self, connections):
        self.saved_connections.clear()
        for conn in connections:
            self.saved_connections.addItem(conn["name"])
