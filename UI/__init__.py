"""User Interface module for Eagle Terminal.

This module contains all the UI components used in Eagle Terminal,
including the main window, tabs, dialogs, and other UI elements.
"""

from . import dialogs, elements, tabs
from .error_dialog import ErrorDialog
from .main_window.main_window import MainWindow

__all__ = ["MainWindow", "ErrorDialog", "tabs", "elements", "dialogs"]
