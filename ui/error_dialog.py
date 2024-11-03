from PyQt5.QtWidgets import QMessageBox

from utils.logger import logger


class ErrorDialog(QMessageBox):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setWindowTitle(title)


def show_error(parent, title, message):
    logger.error(f"Error dialog shown: {title} - {message}")
    ErrorDialog(parent, title, message).exec_()
