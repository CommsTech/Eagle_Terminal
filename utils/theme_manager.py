"""This module manages the application's theme settings.

It provides functionality to switch between light and dark themes, and
to set specific themes for terminal and chief output.
"""

# pylint: disable=no-name-in-module
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QApplication, QTextEdit


class ThemeManager:
    """A class to manage the application's theme settings."""

    @staticmethod
    def set_theme(app: QApplication, settings):
        """Set the application theme based on the settings.

        Args:
            app (QApplication): The application instance.
            settings (dict): The application settings.
        """
        if settings.get("dark_theme", False):
            ThemeManager.set_dark_theme(app)
        else:
            ThemeManager.set_light_theme(app)

    @staticmethod
    def set_dark_theme(app: QApplication):
        """Set the dark theme for the application.

        Args:
            app (QApplication): The application instance.
        """
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        app.setStyleSheet(
            """
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QTextEdit, QLineEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4c4c4c;
            }
        """
        )

    @staticmethod
    def set_light_theme(app: QApplication):
        """Set the light theme for the application.

        Args:
            app (QApplication): The application instance.
        """
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("")

    @staticmethod
    def set_terminal_theme(terminal: QTextEdit):
        """Set the theme for the terminal widget.

        Args:
            terminal (QTextEdit): The terminal widget instance.
        """
        terminal.setStyleSheet(
            """
            QTextEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                font-family: 'Consolas', monospace;
                font-size: 10pt;
            }
        """
        )

    @staticmethod
    def set_chief_output_theme(chief_output):
        """Set the theme for the chief output widget.

        Args:
            chief_output (QTextEdit): The chief output widget instance.
        """
        chief_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #2d2d2d;
                color: #87CEFA;
                border: none;
                padding: 5px;
            }
        """
        )
