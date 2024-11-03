"""Error Handling module for Eagle Terminal.

This module contains the ErrorHandler class, which manages error
handling and display in the main window of Eagle Terminal.
"""

from PyQt5.QtWidgets import QMessageBox

from utils.logger import logger


class ErrorHandler:
    @staticmethod
    def show_error(parent, title: str, message: str):
        """Display an error message box.

        Args:
            parent: The parent widget for the message box.
            title (str): The title of the error message box.
            message (str): The error message to display.
        """
        logger.error(f"{title}: {message}")
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_warning(parent, title: str, message: str):
        """Display a warning message box.

        Args:
            parent: The parent widget for the message box.
            title (str): The title of the warning message box.
            message (str): The warning message to display.
        """
        logger.warning(f"{title}: {message}")
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_info(parent, title: str, message: str):
        """Display an information message box.

        Args:
            parent: The parent widget for the message box.
            title (str): The title of the information message box.
            message (str): The information message to display.
        """
        logger.info(f"{title}: {message}")
        QMessageBox.information(parent, title, message)

    @staticmethod
    def log_error(title: str, message: str):
        """Log an error message without displaying a message box.

        Args:
            title (str): The title or category of the error.
            message (str): The error message to log.
        """
        logger.error(f"{title}: {message}")

    @staticmethod
    def log_warning(title: str, message: str):
        """Log a warning message without displaying a message box.

        Args:
            title (str): The title or category of the warning.
            message (str): The warning message to log.
        """
        logger.warning(f"{title}: {message}")

    @staticmethod
    def log_info(title: str, message: str):
        """Log an information message without displaying a message box.

        Args:
            title (str): The title or category of the information.
            message (str): The information message to log.
        """
        logger.info(f"{title}: {message}")
