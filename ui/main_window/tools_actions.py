from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
else:
    from PyQt5.QtWidgets import QMessageBox, QAction, QMenu

from utils.logger import logger


class ToolsActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def keymap_editor(self):
        logger.info("Keymap Editor action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Keymap Editor not implemented yet"
        )

    def create_public_key(self):
        logger.info("Create Public Key action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Create Public Key not implemented yet"
        )

    def convert_private_key(self):
        logger.info("Convert Private Key action triggered")
        QMessageBox.information(
            self.main_window,
            "Info",
            "Convert Private Key to OpenSSH Format not implemented yet",
        )

    def export_public_key(self):
        logger.info("Export Public Key action triggered")
        QMessageBox.information(
            self.main_window,
            "Info",
            "Export Public Key from Certificate not implemented yet",
        )

    def public_key_assistant(self):
        logger.info("Public Key Assistant action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Public Key Assistant not implemented yet"
        )

    def manage_agent_keys(self):
        logger.info("Manage Agent Keys action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Manage Agent Keys not implemented yet"
        )

    def change_config_properties(self):
        logger.info("Change Configuration Properties action triggered")
        QMessageBox.information(
            self.main_window,
            "Info",
            "Change Configuration Properties not implemented yet",
        )

    def export_settings(self):
        logger.info("Export Settings action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Export Settings not implemented yet"
        )

    def import_settings(self):
        logger.info("Import Settings action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Import Settings not implemented yet"
        )

    def setup_menu(self, menu: QMenu):
        actions = [
            ("Keymap Editor", self.keymap_editor),
            ("Create Public Key", self.create_public_key),
            ("Convert Private Key to OpenSSH Format", self.convert_private_key),
            ("Export Public Key from Certificate", self.export_public_key),
            ("Public Key Assistant", self.public_key_assistant),
            ("Manage Agent Keys", self.manage_agent_keys),
            ("Change Configuration Properties", self.change_config_properties),
            ("Export Settings", self.export_settings),
            ("Import Settings", self.import_settings),
        ]

        for name, callback in actions:
            action = QAction(name, self.main_window)
            action.triggered.connect(callback)
            menu.addAction(action)

        # Add other actions here if needed
        # Example:
        # menu.addAction(self.create_action("Some Action", self.some_function, "Ctrl+S"))

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action
