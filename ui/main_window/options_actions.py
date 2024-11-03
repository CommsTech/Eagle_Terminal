from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
else:
    from PyQt5.QtWidgets import QAction, QMenu, QMessageBox

from utils.logger import logger


class OptionsActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_menu(self, menu: QMenu) -> None:
        """Set up the Options menu."""
        actions = [
            ("Global Options", self.global_options),
            ("Session Options", self.session_options),
            ("Default Session", self.default_session),
            ("Keyword Sets", self.keyword_sets),
            ("Logging", self.logging),
            ("Keyboard", self.keyboard),
            ("Appearance", self.appearance),
            ("Proxy Settings", self.proxy_settings),
            ("Meshtastic Settings", self.meshtastic_settings),
        ]

        for name, callback in actions:
            menu.addAction(self.create_action(name, callback))

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def global_options(self):
        logger.info("Global Options action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Global Options not implemented yet"
        )

    def session_options(self):
        logger.info("Session Options action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Session Options not implemented yet"
        )

    def default_session(self):
        logger.info("Default Session action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Default Session not implemented yet"
        )

    def keyword_sets(self):
        logger.info("Keyword Sets action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Keyword Sets not implemented yet"
        )

    def logging(self):
        logger.info("Logging action triggered")
        QMessageBox.information(self.main_window, "Info", "Logging not implemented yet")

    def keyboard(self):
        logger.info("Keyboard action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Keyboard not implemented yet"
        )

    def appearance(self):
        logger.info("Appearance action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Appearance not implemented yet"
        )

    def proxy_settings(self):
        logger.info("Proxy Settings action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Proxy Settings not implemented yet"
        )

    def meshtastic_settings(self):
        logger.info("Meshtastic Settings action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Meshtastic Settings not implemented yet"
        )
