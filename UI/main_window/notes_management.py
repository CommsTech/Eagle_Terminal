import json
import os

from cryptography.fernet import Fernet
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QDialog, QPushButton, QTextEdit, QVBoxLayout

from utils.logger import logger


class NotesDialog(QDialog):
    def __init__(self, parent, device_id, notes, on_save):
        super().__init__(parent)
        self.device_id = device_id
        self.notes = notes
        self.on_save = on_save
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        self.notes_edit = QTextEdit(self.notes)
        layout.addWidget(self.notes_edit)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_notes)
        layout.addWidget(save_button)

    def save_notes(self):
        new_notes = self.notes_edit.toPlainText()
        self.on_save(self.device_id, new_notes)
        self.accept()


class NotesManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.notes_file = "device_notes.enc"
        self.key_file = "notes_key.key"
        self.load_or_create_key()
        self.notes = self.load_notes()

    def load_or_create_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        self.fernet = Fernet(key)

    def load_notes(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        return {}

    def save_notes(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.notes).encode())
        with open(self.notes_file, "wb") as file:
            file.write(encrypted_data)

    def open_notes(self, device_id):
        device = self.main_window.device_management.get_device(device_id)
        if device:
            notes = self.notes.get(device_id, "")
            dialog = NotesDialog(self.main_window, device_id, notes, self.update_notes)
            dialog.exec_()
        else:
            logger.warning(f"Device with ID {device_id} not found")

    def update_notes(self, device_id, new_notes):
        self.notes[device_id] = new_notes
        self.save_notes()
        self.main_window.chief.learn_device_notes(device_id, new_notes)

    def get_notes(self, device_id):
        return self.notes.get(device_id, "")
