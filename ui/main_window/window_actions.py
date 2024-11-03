from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
else:
    from PyQt5.QtWidgets import QAction, QMenu, QMessageBox

from utils.logger import logger


class WindowActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_menu(self, menu: QMenu) -> None:
        """Set up the Window menu."""
        menu.addAction(self.create_action("New Window", self.new_window))
        menu.addAction(self.create_action("Close Window", self.close_window))
        menu.addSeparator()
        menu.addAction(self.create_action("New Tab", self.new_tab))
        menu.addAction(self.create_action("Close Tab", self.close_tab))
        menu.addSeparator()
        menu.addAction(self.create_action("Next Tab", self.next_tab))
        menu.addAction(self.create_action("Previous Tab", self.previous_tab))
        menu.addSeparator()
        menu.addAction(self.create_action("Minimize", self.main_window.showMinimized))
        menu.addAction(self.create_action("Maximize", self.main_window.showMaximized))
        menu.addAction(self.create_action("Restore", self.main_window.showNormal))
        menu.addSeparator()
        menu.addAction(self.create_action("Show Tabs", self.show_tabs))
        menu.addAction(self.create_action("Tile Vertically", self.tile_vertically))
        menu.addAction(self.create_action("Tile Horizontally", self.tile_horizontally))
        menu.addAction(self.create_action("Cascade", self.cascade_windows))

        # Add open sessions dynamically
        menu.addSeparator()
        open_sessions = self.main_window.get_open_sessions()
        if open_sessions:
            for session in open_sessions:
                menu.addAction(
                    self.create_action(
                        session["name"], lambda s=session: self.focus_session(s)
                    )
                )
        else:
            no_sessions_action = self.create_action("No Open Sessions", lambda: None)
            no_sessions_action.setEnabled(False)
            menu.addAction(no_sessions_action)

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def new_window(self) -> None:
        """Open a new main window."""
        logger.info("New window action triggered")
        # Implement new window creation logic here

    def close_window(self) -> None:
        """Close the current window."""
        logger.info("Close window action triggered")
        self.main_window.close()

    def new_tab(self) -> None:
        """Open a new tab."""
        logger.info("New tab action triggered")
        self.main_window.new_session()

    def close_tab(self) -> None:
        """Close the current tab."""
        logger.info("Close tab action triggered")
        current_index = self.main_window.tab_widget.currentIndex()
        if current_index != -1:
            self.main_window.tab_widget.removeTab(current_index)

    def next_tab(self) -> None:
        """Switch to the next tab."""
        logger.info("Next tab action triggered")
        current_index = self.main_window.tab_widget.currentIndex()
        next_index = (current_index + 1) % self.main_window.tab_widget.count()
        self.main_window.tab_widget.setCurrentIndex(next_index)

    def previous_tab(self) -> None:
        """Switch to the previous tab."""
        logger.info("Previous tab action triggered")
        current_index = self.main_window.tab_widget.currentIndex()
        previous_index = (current_index - 1) % self.main_window.tab_widget.count()
        self.main_window.tab_widget.setCurrentIndex(previous_index)

    def show_tabs(self):
        logger.info("Show Tabs action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Show Tabs not implemented yet"
        )

    def tile_vertically(self):
        logger.info("Tile Vertically action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Tile Vertically not implemented yet"
        )

    def tile_horizontally(self):
        logger.info("Tile Horizontally action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Tile Horizontally not implemented yet"
        )

    def cascade_windows(self):
        logger.info("Cascade Windows action triggered")
        QMessageBox.information(
            self.main_window, "Info", "Cascade Windows not implemented yet"
        )

    def focus_session(self, session):
        logger.info(f"Focus on session {session['name']} action triggered")
        QMessageBox.information(
            self.main_window,
            "Info",
            f"Focus on session {session['name']} not implemented yet",
        )
