from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class RDP_Tab(QWidget):
    def __init__(self, session_data):
        super().__init__()
        self.session_data = session_data
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        label = QLabel("RDP functionality not implemented yet")
        layout.addWidget(label)
