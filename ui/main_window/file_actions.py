import asyncio
import os
from typing import Any

import paramiko
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (
    QAction,
    QDialog,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QToolBar,
    QTreeView,
    QVBoxLayout,
)
from qasync import asyncSlot

from utils.logger import logger


class RemoteFileBrowserDialog(QDialog):
    def __init__(self, sftp, parent=None):
        super().__init__(parent)
        self.sftp = sftp
        self.setWindowTitle("Remote File Browser")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Toolbar
        toolbar = QToolBar()
        upload_action = QAction("Upload", self)
        upload_action.triggered.connect(self.upload_file)
        toolbar.addAction(upload_action)

        download_action = QAction("Download", self)
        download_action.triggered.connect(self.download_file)
        toolbar.addAction(download_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(self.delete_file)
        toolbar.addAction(delete_action)

        rename_action = QAction("Rename", self)
        rename_action.triggered.connect(self.rename_file)
        toolbar.addAction(rename_action)

        layout.addWidget(toolbar)

        # File tree
        self.file_tree = QTreeView()
        self.file_model = QStandardItemModel()
        self.file_tree.setModel(self.file_model)
        layout.addWidget(self.file_tree)

        self.populate_file_tree()

    def populate_file_tree(self, path="/"):
        self.file_model.clear()
        self.file_model.setHorizontalHeaderLabels(["Name", "Size", "Type"])

        try:
            for entry in self.sftp.listdir_attr(path):
                name = entry.filename
                size = str(entry.st_size)
                type_ = "Directory" if entry.longname.startswith("d") else "File"

                item = QStandardItem(name)
                item.setData(os.path.join(path, name), Qt.UserRole)
                self.file_model.appendRow(
                    [item, QStandardItem(size), QStandardItem(type_)]
                )

        except IOError as e:
            logger.error(f"Error listing directory {path}: {str(e)}")

    def upload_file(self):
        local_path, _ = QFileDialog.getOpenFileName(self, "Select File to Upload")
        if local_path:
            remote_path = self.file_tree.currentIndex().data(Qt.UserRole)
            if remote_path:
                try:
                    self.sftp.put(
                        local_path,
                        os.path.join(remote_path, os.path.basename(local_path)),
                    )
                    self.populate_file_tree(os.path.dirname(remote_path))
                    QMessageBox.information(
                        self, "Upload Successful", "File uploaded successfully."
                    )
                except IOError as e:
                    logger.error(f"Error uploading file: {str(e)}")
                    QMessageBox.critical(
                        self, "Upload Failed", f"Failed to upload file: {str(e)}"
                    )

    def download_file(self):
        remote_path = self.file_tree.currentIndex().data(Qt.UserRole)
        if remote_path:
            local_path, _ = QFileDialog.getSaveFileName(self, "Save File As")
            if local_path:
                try:
                    self.sftp.get(remote_path, local_path)
                    QMessageBox.information(
                        self, "Download Successful", "File downloaded successfully."
                    )
                except IOError as e:
                    logger.error(f"Error downloading file: {str(e)}")
                    QMessageBox.critical(
                        self, "Download Failed", f"Failed to download file: {str(e)}"
                    )

    def delete_file(self):
        remote_path = self.file_tree.currentIndex().data(Qt.UserRole)
        if remote_path:
            reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete {remote_path}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                try:
                    self.sftp.remove(remote_path)
                    self.populate_file_tree(os.path.dirname(remote_path))
                    QMessageBox.information(
                        self, "Deletion Successful", "File deleted successfully."
                    )
                except IOError as e:
                    logger.error(f"Error deleting file: {str(e)}")
                    QMessageBox.critical(
                        self, "Deletion Failed", f"Failed to delete file: {str(e)}"
                    )

    def rename_file(self):
        remote_path = self.file_tree.currentIndex().data(Qt.UserRole)
        if remote_path:
            new_name, ok = QInputDialog.getText(self, "Rename File", "Enter new name:")
            if ok and new_name:
                new_path = os.path.join(os.path.dirname(remote_path), new_name)
                try:
                    self.sftp.rename(remote_path, new_path)
                    self.populate_file_tree(os.path.dirname(remote_path))
                    QMessageBox.information(
                        self, "Rename Successful", "File renamed successfully."
                    )
                except IOError as e:
                    logger.error(f"Error renaming file: {str(e)}")
                    QMessageBox.critical(
                        self, "Rename Failed", f"Failed to rename file: {str(e)}"
                    )


class FileActions(QObject):
    new_session_requested = pyqtSignal()

    def __init__(self, main_window: Any):
        super().__init__()
        self.main_window = main_window
        self.setup_actions()

    def setup_actions(self):
        # ... (keep other action setups)

        self.new_session_action = QAction("New Session", self.main_window)
        self.new_session_action.setShortcut("Ctrl+N")
        self.new_session_action.triggered.connect(self.new_session_requested.emit)

    @asyncSlot()
    async def quick_connect(self) -> None:
        """Trigger quick connect action."""
        logger.info("Quick connect action triggered")
        await self.main_window.quick_connect()

    @asyncSlot()
    async def new_session(self):
        logger.info("New session action triggered")
        await self.main_window.session_management.new_session()

    def connect_in_tab(self) -> None:
        """Connect in a new tab."""
        logger.info("Connect in tab action triggered")
        self.main_window.connect_in_tab()

    def connect_in_shell(self) -> None:
        """Connect in a new shell."""
        logger.info("Connect in shell action triggered")
        self.main_window.connect_in_shell()

    def reconnect_current_session(self) -> None:
        """Reconnect the current session."""
        logger.info("Reconnect current session action triggered")
        self.main_window.reconnect_current_session()

    def reconnect_all_sessions(self) -> None:
        """Reconnect all sessions."""
        logger.info("Reconnect all sessions action triggered")
        self.main_window.reconnect_all_sessions()

    def disconnect_current_session(self) -> None:
        """Disconnect the current session."""
        logger.info("Disconnect current session action triggered")
        self.main_window.disconnect_current_session()

    def disconnect_all_sessions(self) -> None:
        """Disconnect all sessions."""
        logger.info("Disconnect all sessions action triggered")
        self.main_window.disconnect_all_sessions()

    def print_current_session(self) -> None:
        """Print the current session."""
        logger.info("Print current session action triggered")
        # Implement print functionality

    def print_setup(self) -> None:
        """Set up print options."""
        logger.info("Print setup action triggered")
        # Implement print setup functionality

    def exit(self) -> None:
        """Exit the application."""
        logger.info("Exit action triggered")
        self.main_window.close()

    def open_file_browser(self):
        logger.info("Opening file browser for current session")
        current_tab = self.main_window.tab_widget.currentWidget()
        if hasattr(current_tab, "ssh_client") and current_tab.ssh_client:
            try:
                sftp = current_tab.ssh_client.open_sftp()
                dialog = RemoteFileBrowserDialog(sftp, self.main_window)
                dialog.exec_()

                # Update Chief with the file structure
                file_structure = self.get_file_structure(sftp)
                self.main_window.chief.learn("File Structure", file_structure)

                sftp.close()
            except Exception as e:
                logger.error(f"Failed to open SFTP browser: {str(e)}")
                self.main_window.error_handler.show_error(
                    "SFTP Error", f"Failed to open SFTP browser: {str(e)}"
                )
        else:
            logger.warning("No active SSH session to open file browser")

    def get_file_structure(self, sftp):
        file_structure = {}
        for entry in sftp.listdir_attr("/"):
            name = entry.filename
            size = entry.st_size
            type_ = "Directory" if entry.longname.startswith("d") else "File"
            file_structure[name] = {"size": size, "type": type_}
        return file_structure

    def open_sftp_browser(self, sftp, remote_path, local_path):
        try:
            remote_files = sftp.listdir(remote_path)
            print(f"Remote files in {remote_path}:")
            for file in remote_files:
                print(file)

            # Example: Download a file
            file_to_download = QFileDialog.getOpenFileName(
                self.main_window, "Select File to Download", "", "All Files (*)"
            )[0]
            if file_to_download:
                remote_file = os.path.join(remote_path, file_to_download)
                local_file = os.path.join(local_path, file_to_download)
                sftp.get(remote_file, local_file)
                logger.info(f"Downloaded {file_to_download} to {local_file}")
                QMessageBox.information(
                    self.main_window,
                    "Download Complete",
                    f"File {file_to_download} has been downloaded successfully.",
                )
        except Exception as e:
            logger.error(f"SFTP operation failed: {str(e)}")
            self.main_window.error_handler.show_error(
                "SFTP Error", f"SFTP operation failed: {str(e)}"
            )
        finally:
            sftp.close()

    def new_file(self):
        logger.info("Creating new file")
        # Implement new file creation functionality
        QMessageBox.information(
            self.main_window,
            "New File",
            "New file creation functionality is not yet implemented.",
        )

    def open_file(self):
        logger.info("Opening file")
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Open File", "", "All Files (*)"
        )
        if file_path:
            # Implement file opening functionality
            logger.info(f"File selected: {file_path}")
            QMessageBox.information(
                self.main_window,
                "Open File",
                f"File opening functionality for {file_path} is not yet implemented.",
            )

    def save_file(self):
        logger.info("Saving file")
        # Implement file saving functionality
        QMessageBox.information(
            self.main_window,
            "Save File",
            "File saving functionality is not yet implemented.",
        )

    def save_file_as(self):
        logger.info("Saving file as")
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Save File As", "", "All Files (*)"
        )
        if file_path:
            # Implement file saving functionality
            logger.info(f"File to be saved as: {file_path}")
            QMessageBox.information(
                self.main_window,
                "Save File As",
                f"File saving functionality for {file_path} is not yet implemented.",
            )

    def run_script_dialog(self):
        logger.info("Opening run script dialog")
        self.main_window.script_actions.run()
