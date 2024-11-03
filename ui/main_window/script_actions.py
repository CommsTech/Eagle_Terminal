"""Script Actions module for Eagle Terminal.

This module contains the ScriptActions class, which handles all script-
related actions in the main window of Eagle Terminal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QMenu
else:
    from PyQt5.QtWidgets import QAction, QMenu

from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from utils.logger import logger


class ScriptActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_menu(self, menu: QMenu) -> None:
        """Set up the Script menu."""
        actions = [
            ("Run", self.run_script),
            ("Cancel", self.cancel_script),
            ("Start Recording Script", self.start_recording_script),
            ("Stop Recording Script", self.stop_recording_script),
            ("Cancel Recording Script", self.cancel_recording_script),
        ]

        for name, callback in actions:
            menu.addAction(self.create_action(name, callback))

        recent_scripts_menu = QMenu("Recent Scripts", self.main_window)
        menu.addMenu(recent_scripts_menu)
        # Populate recent_scripts_menu dynamically
        self.populate_recent_scripts(recent_scripts_menu)

        menu.addAction(self.create_action("Configure Scripts", self.configure_scripts))

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def run_script(self):
        logger.info("Run script action triggered")
        # Implement run script functionality here

    def cancel_script(self):
        logger.info("Cancel script action triggered")
        # Implement cancel script functionality here

    def start_recording_script(self):
        logger.info("Start recording script action triggered")
        # Implement start recording script functionality here

    def stop_recording_script(self):
        logger.info("Stop recording script action triggered")
        # Implement stop recording script functionality here

    def cancel_recording_script(self):
        logger.info("Cancel recording script action triggered")
        # Implement cancel recording script functionality here

    def configure_scripts(self):
        logger.info("Configure scripts action triggered")
        # Implement configure scripts functionality here

    def populate_recent_scripts(self, menu: QMenu):
        # Implement populating recent scripts menu
        # This method should be called whenever the list of recent scripts changes
        pass

    # Add more script-related methods here as needed
