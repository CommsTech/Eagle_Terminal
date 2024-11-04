from PyQt5.QtWidgets import (QLineEdit, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget)


class Chat_Tab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

    def send_message(self):
        message = self.input_field.text()
        if message:
            self.chat_display.append(f"You: {message}")
            self.input_field.clear()
            # Here you would typically send the message to a server or process it
