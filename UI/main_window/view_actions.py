"""View Actions module for Eagle Terminal.

This module contains the ViewActions class, which handles all view-
related actions in the main window of Eagle Terminal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QMenu
else:
    from PyQt5.QtWidgets import QAction, QMenu

from utils.logger import logger

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QToolBar
else:
    from PyQt5.QtWidgets import QToolBar

from PyQt5.QtCore import Qt


class ViewActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_menu(self, menu: QMenu) -> None:
        """Set up the View menu."""
        menu.addAction(self.create_action("Zoom In", self.zoom_in))
        menu.addAction(self.create_action("Zoom Out", self.zoom_out))
        menu.addAction(self.create_action("Reset Zoom", self.reset_zoom))
        # Add more view actions here as needed

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def toggle_toolbar(self) -> None:
        """Toggle the visibility of the toolbar."""
        logger.info("Toggle toolbar action triggered")
        toolbar = self.main_window.findChild(QToolBar)
        if toolbar:
            toolbar.setVisible(not toolbar.isVisible())
        else:
            logger.warning("Toolbar not found")

    def toggle_status_bar(self) -> None:
        """Toggle the visibility of the status bar."""
        logger.info("Toggle status bar action triggered")
        self.main_window.statusBar().setVisible(
            not self.main_window.statusBar().isVisible()
        )

    def toggle_device_list(self) -> None:
        """Toggle the visibility of the device list."""
        logger.info("Toggle device list action triggered")
        if hasattr(self.main_window, "device_list"):
            self.main_window.device_list.setVisible(
                not self.main_window.device_list.isVisible()
            )
        else:
            logger.warning("Device list not found")

    def toggle_full_screen(self) -> None:
        """Toggle full screen mode."""
        logger.info("Toggle full screen action triggered")
        if self.main_window.isFullScreen():
            self.main_window.showNormal()
        else:
            self.main_window.showFullScreen()

    def zoom_in(self) -> None:
        """Zoom in the current terminal view."""
        logger.info("Zoom in action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "zoom_in"):
            current_tab.zoom_in()
        else:
            logger.warning("Current tab does not support zoom in")

    def zoom_out(self) -> None:
        """Zoom out the current terminal view."""
        logger.info("Zoom out action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "zoom_out"):
            current_tab.zoom_out()
        else:
            logger.warning("Current tab does not support zoom out")

    def reset_zoom(self) -> None:
        """Reset zoom level of the current terminal view."""
        logger.info("Reset zoom action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "reset_zoom"):
            current_tab.reset_zoom()
        else:
            logger.warning("Current tab does not support reset zoom")

    def toggle_word_wrap(self) -> None:
        """Toggle word wrap in the current terminal view."""
        logger.info("Toggle word wrap action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "toggle_word_wrap"):
            current_tab.toggle_word_wrap()
        else:
            logger.warning("Current tab does not support word wrap")

    def toggle_always_on_top(self) -> None:
        """Toggle always on top mode for the main window."""
        logger.info("Toggle always on top action triggered")
        flags = self.main_window.windowFlags()
        if flags & Qt.WindowStaysOnTopHint:
            flags &= ~Qt.WindowStaysOnTopHint
        else:
            flags |= Qt.WindowStaysOnTopHint
        self.main_window.setWindowFlags(flags)
        self.main_window.show()
