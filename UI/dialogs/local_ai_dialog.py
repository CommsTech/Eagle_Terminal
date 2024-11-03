from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QTextEdit, QVBoxLayout


class LocalAIDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Local AI")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Local AI Configuration", self)
        layout.addWidget(label)

        self.config_text = QTextEdit(self)
        layout.addWidget(self.config_text)

        save_button = QPushButton("Save Configuration", self)
        save_button.clicked.connect(self.save_configuration)
        layout.addWidget(save_button)

    def save_configuration(self):
        # Implement saving the configuration
        config = self.config_text.toPlainText()
        # Save the config to a file or process it as needed
        print(f"Saving configuration: {config}")
        self.accept()
