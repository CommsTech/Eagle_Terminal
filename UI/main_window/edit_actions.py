"""Edit Actions module for Eagle Terminal.

This module contains the EditActions class, which handles all edit-
related actions in the main window of Eagle Terminal.
"""

from PyQt5.QtWidgets import QAction, QInputDialog, QMessageBox

from utils.logger import logger


class EditActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def copy(self) -> None:
        """Copy selected text to clipboard."""
        logger.info("Copy action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "copy_selection"):
            current_tab.copy_selection()
        else:
            logger.warning("Current tab does not support copy action")

    def paste(self) -> None:
        """Paste text from clipboard."""
        logger.info("Paste action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "paste_clipboard"):
            current_tab.paste_clipboard()
        else:
            logger.warning("Current tab does not support paste action")

    def copy_and_paste(self) -> None:
        """Copy selected text and immediately paste it."""
        logger.info("Copy and paste action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "copy_and_paste"):
            current_tab.copy_and_paste()
        else:
            logger.warning("Current tab does not support copy and paste action")

    def select_all(self) -> None:
        """Select all text in the current tab."""
        logger.info("Select all action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "select_all"):
            current_tab.select_all()
        else:
            logger.warning("Current tab does not support select all action")

    def find(self) -> None:
        """Open find dialog."""
        logger.info("Find action triggered")
        text, ok = QInputDialog.getText(self.main_window, "Find", "Enter text to find:")
        if ok and text:
            current_tab = self.main_window.tab_widget.currentWidget()
            if hasattr(current_tab, "find_text"):
                found = current_tab.find_text(text)
                if not found:
                    QMessageBox.information(
                        self.main_window, "Find", f'Text "{text}" not found.'
                    )
            else:
                logger.warning("Current tab does not support find action")

    def go_to_session(self) -> None:
        """Go to a specific session."""
        logger.info("Go to session action triggered")
        sessions = self.main_window.get_open_sessions()
        session_names = [f"{s['hostname']} ({s['username']})" for s in sessions]
        session, ok = QInputDialog.getItem(
            self.main_window,
            "Go to Session",
            "Select a session:",
            session_names,
            0,
            False,
        )
        if ok and session:
            index = session_names.index(session)
            self.main_window.tab_widget.setCurrentIndex(index)

    def clear_scrollback(self) -> None:
        """Clear scrollback buffer of the current terminal."""
        logger.info("Clear scrollback action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "clear_scrollback"):
            current_tab.clear_scrollback()
        else:
            logger.warning("Current tab does not support clear scrollback action")

    def clear_screen(self) -> None:
        """Clear the screen of the current terminal."""
        logger.info("Clear screen action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "clear_screen"):
            current_tab.clear_screen()
        else:
            logger.warning("Current tab does not support clear screen action")

    def send_break(self) -> None:
        """Send break signal to the current terminal."""
        logger.info("Send break action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "send_break"):
            current_tab.send_break()
        else:
            logger.warning("Current tab does not support send break action")

    def reset(self) -> None:
        """Reset the current terminal."""
        logger.info("Reset action triggered")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "reset_terminal"):
            current_tab.reset_terminal()
        else:
            logger.warning("Current tab does not support reset action")


def setup_menu(menu, parent):
    # Add edit actions to the menu
    copy_action = QAction("Copy", parent)
    copy_action.triggered.connect(parent.copy)
    menu.addAction(copy_action)

    paste_action = QAction("Paste", parent)
    paste_action.triggered.connect(parent.paste)
    menu.addAction(paste_action)

    # Add more edit actions as needed
