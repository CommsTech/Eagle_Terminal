import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox  # type: ignore

from ui.error_dialog import ErrorDialog
from utils.logger import logger


def global_exception_handler(exctype, value, traceback):
    """Global exception handler to log unhandled exceptions and show an error
    dialog."""
    logger.critical("Unhandled exception", exc_info=(exctype, value, traceback))
    error_dialog = ErrorDialog(None, "Unhandled Exception", str(value))
    error_dialog.exec_()


def setup_global_error_handling():
    """Set up the global exception handler."""
    sys.excepthook = global_exception_handler


class ErrorHandler:
    @staticmethod
    def show_error(title: str, message: str):
        """Displays an error message box with a given title and message.
        
        Args:
            title (str): The title of the error message box.
            message (str): The main text content of the error message box.
        
        Returns:
            None: This method doesn't return anything.
        """
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.exec_()
