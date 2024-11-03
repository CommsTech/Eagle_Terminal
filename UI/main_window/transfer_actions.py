"""Transfer Actions module for Eagle Terminal.

This module contains the TransferActions class, which handles all file
transfer related actions in the main window of Eagle Terminal.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtWidgets import QAction, QFileDialog, QMenu, QMessageBox
else:
    from PyQt5.QtWidgets import QAction, QMenu, QFileDialog, QMessageBox

from utils.logger import logger


class TransferActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_menu(self, menu: QMenu) -> None:
        """Set up the Transfer menu."""
        actions = [
            ("Send ASCII", self.send_ascii),
            ("Receive ASCII", self.receive_ascii),
            ("Send Binary", self.send_binary),
            ("Send Kermit", self.send_kermit),
            ("Receive Kermit", self.receive_kermit),
            ("Send Xmodem", self.send_xmodem),
            ("Receive Xmodem", self.receive_xmodem),
            ("Send Ymodem", self.send_ymodem),
            ("Receive Ymodem", self.receive_ymodem),
            ("Zmodem Upload List", self.zmodem_upload_list),
            ("Start Zmodem Upload", self.start_zmodem_upload),
            ("Start TFTP Server", self.start_tftp_server),
        ]

        for name, callback in actions:
            menu.addAction(self.create_action(name, callback))

    def create_action(self, text, slot, shortcut=None):
        action = QAction(text, self.main_window)
        action.triggered.connect(slot)
        if shortcut:
            action.setShortcut(shortcut)
        return action

    def send_ascii(self) -> None:
        """Send an ASCII file."""
        logger.info("Send ASCII action triggered")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Select ASCII file to send"
        )
        if file_path:
            # Implement ASCII file sending logic here
            QMessageBox.information(
                self.main_window, "Send ASCII", f"Sending ASCII file: {file_path}"
            )

    def receive_ascii(self) -> None:
        """Receive an ASCII file."""
        logger.info("Receive ASCII action triggered")
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save received ASCII file"
        )
        if file_path:
            # Implement ASCII file receiving logic here
            QMessageBox.information(
                self.main_window,
                "Receive ASCII",
                f"Receiving ASCII file to: {file_path}",
            )

    def send_binary(self) -> None:
        """Send a binary file."""
        logger.info("Send binary action triggered")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Select binary file to send"
        )
        if file_path:
            # Implement binary file sending logic here
            QMessageBox.information(
                self.main_window, "Send Binary", f"Sending binary file: {file_path}"
            )

    def send_kermit(self) -> None:
        """Send a file using Kermit protocol."""
        logger.info("Send Kermit action triggered")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Select file to send via Kermit"
        )
        if file_path:
            # Implement Kermit file sending logic here
            QMessageBox.information(
                self.main_window, "Send Kermit", f"Sending file via Kermit: {file_path}"
            )

    def receive_kermit(self) -> None:
        """Receive a file using Kermit protocol."""
        logger.info("Receive Kermit action triggered")
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save file received via Kermit"
        )
        if file_path:
            # Implement Kermit file receiving logic here
            QMessageBox.information(
                self.main_window,
                "Receive Kermit",
                f"Receiving file via Kermit to: {file_path}",
            )

    def send_xmodem(self) -> None:
        """Send a file using XMODEM protocol."""
        logger.info("Send XMODEM action triggered")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Select file to send via XMODEM"
        )
        if file_path:
            # Implement XMODEM file sending logic here
            QMessageBox.information(
                self.main_window, "Send XMODEM", f"Sending file via XMODEM: {file_path}"
            )

    def receive_xmodem(self) -> None:
        """Receive a file using XMODEM protocol."""
        logger.info("Receive XMODEM action triggered")
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save file received via XMODEM"
        )
        if file_path:
            # Implement XMODEM file receiving logic here
            QMessageBox.information(
                self.main_window,
                "Receive XMODEM",
                f"Receiving file via XMODEM to: {file_path}",
            )

    def send_ymodem(self) -> None:
        """Send a file using YMODEM protocol."""
        logger.info("Send YMODEM action triggered")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Select file to send via YMODEM"
        )
        if file_path:
            # Implement YMODEM file sending logic here
            QMessageBox.information(
                self.main_window, "Send YMODEM", f"Sending file via YMODEM: {file_path}"
            )

    def receive_ymodem(self) -> None:
        """Receive a file using YMODEM protocol."""
        logger.info("Receive YMODEM action triggered")
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save file received via YMODEM"
        )
        if file_path:
            # Implement YMODEM file receiving logic here
            QMessageBox.information(
                self.main_window,
                "Receive YMODEM",
                f"Receiving file via YMODEM to: {file_path}",
            )

    def zmodem_upload_list(self) -> None:
        """Show ZMODEM upload list."""
        logger.info("ZMODEM upload list action triggered")
        # Implement ZMODEM upload list logic here
        QMessageBox.information(
            self.main_window,
            "ZMODEM Upload List",
            "ZMODEM upload list not yet implemented",
        )

    def start_zmodem_upload(self) -> None:
        """Start ZMODEM upload."""
        logger.info("Start ZMODEM upload action triggered")
        # Implement ZMODEM upload logic here
        QMessageBox.information(
            self.main_window, "Start ZMODEM Upload", "ZMODEM upload not yet implemented"
        )

    def start_tftp_server(self) -> None:
        """Start TFTP server."""
        logger.info("Start TFTP server action triggered")
        # Implement TFTP server logic here
        QMessageBox.information(
            self.main_window, "Start TFTP Server", "TFTP server not yet implemented"
        )
