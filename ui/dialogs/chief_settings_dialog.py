from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QDialog, QDoubleSpinBox, QFormLayout,
                             QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                             QPushButton, QSpinBox, QTabWidget, QVBoxLayout,
                             QWidget)

from utils.logger import logger


class ChiefSettingsDialog(QDialog):
    def __init__(self, chief, parent=None):
        super().__init__(parent)
        self.chief = chief
        self.setWindowTitle("Chief AI Settings")
        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        tabs.addTab(self.create_core_settings_tab(), "Core Settings")
        tabs.addTab(self.create_external_ai_tab(), "External AI")

        layout.addWidget(tabs)

        buttons = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(save_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

    def create_core_settings_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        self.model_name = QLineEdit(self.chief.config.get("model_name", ""))
        layout.addRow("Model Name:", self.model_name)

        self.max_length = QSpinBox()
        self.max_length.setRange(1, 2048)
        self.max_length.setValue(self.chief.config.get("max_length", 512))
        layout.addRow("Max Length:", self.max_length)

        self.learning_threshold = QSpinBox()
        self.learning_threshold.setRange(1, 1000)
        self.learning_threshold.setValue(
            self.chief.config.get("learning_threshold", 100)
        )
        layout.addRow("Learning Threshold:", self.learning_threshold)

        self.fine_tuning_epochs = QSpinBox()
        self.fine_tuning_epochs.setRange(1, 100)
        self.fine_tuning_epochs.setValue(self.chief.config.get("fine_tuning_epochs", 3))
        layout.addRow("Fine-tuning Epochs:", self.fine_tuning_epochs)

        self.batch_size = QSpinBox()
        self.batch_size.setRange(1, 128)
        self.batch_size.setValue(self.chief.config.get("batch_size", 8))
        layout.addRow("Batch Size:", self.batch_size)

        self.learning_rate = QDoubleSpinBox()
        self.learning_rate.setRange(0.00001, 0.1)
        self.learning_rate.setSingleStep(0.00001)
        self.learning_rate.setValue(self.chief.config.get("learning_rate", 2e-5))
        layout.addRow("Learning Rate:", self.learning_rate)

        return tab

    def create_external_ai_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        self.use_external_ai = QCheckBox()
        self.use_external_ai.setChecked(
            self.chief.settings.get("use_external_ai", False)
        )
        layout.addRow("Use External AI:", self.use_external_ai)

        self.external_ai_url = QLineEdit(self.chief.settings.get("external_ai_url", ""))
        layout.addRow("External AI URL:", self.external_ai_url)

        self.external_ai_key = QLineEdit(self.chief.settings.get("external_ai_key", ""))
        self.external_ai_key.setEchoMode(QLineEdit.Password)
        layout.addRow("External AI Key:", self.external_ai_key)

        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self.test_external_ai_connection)
        layout.addRow("", test_button)

        return tab

    def save_settings(self):
        # Update Chief's config
        self.chief.config["model_name"] = self.model_name.text()
        self.chief.config["max_length"] = self.max_length.value()
        self.chief.config["learning_threshold"] = self.learning_threshold.value()
        self.chief.config["fine_tuning_epochs"] = self.fine_tuning_epochs.value()
        self.chief.config["batch_size"] = self.batch_size.value()
        self.chief.config["learning_rate"] = self.learning_rate.value()

        # Update Chief's settings
        self.chief.settings["use_external_ai"] = self.use_external_ai.isChecked()
        self.chief.settings["external_ai_url"] = self.external_ai_url.text()
        self.chief.settings["external_ai_key"] = self.external_ai_key.text()

        # Apply changes
        self.chief.apply_settings()

        logger.info("Chief settings updated")
        self.accept()

    def test_external_ai_connection(self):
        url = self.external_ai_url.text()
        key = self.external_ai_key.text()

        # Implement the actual connection test here
        # For now, we'll just show a placeholder message
        QMessageBox.information(
            self, "Connection Test", f"Testing connection to {url}..."
        )
        logger.info(f"Testing external AI connection to {url}")
