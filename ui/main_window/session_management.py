import asyncio
import json
import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from ui.dialogs.new_connection_wizard import NewConnectionWizard
from ui.dialogs.quick_connect_dialog import QuickConnectDialog
from ui.tabs.ssh_tab import SSHTab
from ui.tabs.shell_tab import ShellTab
from utils.logger import logger


class SessionManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.sessions_file = "sessions.json"
        self.load_saved_sessions()

    def load_saved_sessions(self):
        if os.path.exists(self.sessions_file):
            with open(self.sessions_file, "r") as f:
                self.saved_sessions = json.load(f)
        else:
            self.saved_sessions = []

    def save_sessions(self):
        with open(self.sessions_file, "w") as f:
            json.dump(self.saved_sessions, f)

    async def new_session(self, force_new=False):
        """Create a new session."""
        logger.info("Creating new session")
        try:
            if not force_new:
                # Check if there's a selected device
                current_device = self.main_window.device_management.get_current_device()
                if current_device:
                    # Use the current device's information
                    session_data = current_device
                else:
                    force_new = True  # No device selected, so force new connection

            if force_new:
                # Always open the NewConnectionWizard for new connections
                dialog = NewConnectionWizard(self.main_window)
                if dialog.exec_():
                    session_data = dialog.get_session_data()
                else:
                    return  # User cancelled the dialog

            ssh_tab = await self.main_window.create_ssh_tab(session_data)
            if ssh_tab:
                # Add the device to the device list if it's not already there
                if force_new:
                    self.main_window.device_management.add_device(session_data)
        except Exception as e:
            logger.error(f"Error creating new session: {str(e)}")
            self.main_window.error_handler.show_error(
                self.main_window,
                "Session Error",
                f"Failed to create new session: {str(e)}",
            )

    async def open_session(self, session_data):
        new_tab = self.main_window.create_ssh_tab(session_data)
        self.main_window.add_open_session(session_data)

        # Wait for the connection to be established
        await new_tab.connection_established.wait()

        if new_tab.is_connected:
            session_data["os_type"] = new_tab.os_type
            new_tab.display_session_info()
        else:
            logger.error(f"Failed to connect to {session_data['hostname']}")
            self.main_window.tab_widget.removeTab(
                self.main_window.tab_widget.indexOf(new_tab)
            )

    def close_session(self, index):
        if 0 <= index < self.main_window.tab_widget.count():
            tab = self.main_window.tab_widget.widget(index)
            if isinstance(tab, SSHTab):
                tab.ssh_connection.close()
            self.main_window.tab_widget.removeTab(index)
            if index < len(self.main_window.open_sessions):
                self.main_window.open_sessions.pop(index)
        else:
            logger.warning(f"Attempted to close invalid session index: {index}")

    def reconnect_session(self, session_data):
        for i in range(self.main_window.tab_widget.count()):
            tab = self.main_window.tab_widget.widget(i)
            if isinstance(tab, SSHTab) and tab.session_data == session_data:
                tab.reconnect()
                break

    def connect_in_tab(self):
        logger.info("Connecting in a new tab")
        self.new_session()

    def connect_in_shell(self):
        logger.info("Connecting in shell")
        # Implement shell connection logic
        wizard = NewConnectionWizard(self.main_window)
        if wizard.exec_():
            session_data = wizard.get_connection_data()
            shell = ShellTab(self.main_window, session_data)
            self.main_window.tab_widget.addTab(
                shell, f"Shell: {session_data['hostname']}"
            )
            self.main_window.add_open_session(session_data)
            asyncio.create_task(shell.connect())
        QMessageBox.information(
            self.main_window,
            "Not Implemented",
            "Connect in shell functionality is not yet implemented.",
        )

    def disconnect_current_session(self):
        current_index = self.main_window.tab_widget.currentIndex()
        if current_index != -1:
            self.close_session(current_index)

    def reconnect_current_session(self):
        current_tab = self.main_window.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab):
            current_tab.reconnect()

    def reconnect_all_sessions(self):
        for i in range(self.main_window.tab_widget.count()):
            tab = self.main_window.tab_widget.widget(i)
            if isinstance(tab, SSHTab):
                tab.reconnect()

    def disconnect_all_sessions(self):
        for i in range(self.main_window.tab_widget.count() - 1, -1, -1):
            self.close_session(i)

    def get_current_session(self):
        current_tab = self.main_window.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab):
            return current_tab.session_data
        return None

    def get_session_by_name(self, name):
        for session in self.main_window.open_sessions:
            if session.get("name") == name:
                return session
        return None

    def rename_session(self, old_name, new_name):
        session = self.get_session_by_name(old_name)
        if session:
            session["name"] = new_name
            for i in range(self.main_window.tab_widget.count()):
                tab = self.main_window.tab_widget.widget(i)
                if isinstance(tab, SSHTab) and tab.session_data == session:
                    self.main_window.tab_widget.setTabText(i, f"SSH: {new_name}")
                    break
            self.save_sessions()

    def duplicate_session(self, session_data):
        new_session_data = session_data.copy()
        new_session_data["name"] = f"{session_data['name']} (copy)"
        self.open_session(new_session_data)

    def save_session(self, session_data):
        if session_data not in self.saved_sessions:
            self.saved_sessions.append(session_data)
            self.save_sessions()
            logger.info(f"Session saved: {session_data['name']}")

    def delete_saved_session(self, session_name):
        self.saved_sessions = [
            s for s in self.saved_sessions if s["name"] != session_name
        ]
        self.save_sessions()
        logger.info(f"Saved session deleted: {session_name}")

    def load_saved_session(self, session_name):
        session = next(
            (s for s in self.saved_sessions if s["name"] == session_name), None
        )
        if session:
            self.open_session(session)
        else:
            logger.warning(f"Saved session not found: {session_name}")

    def export_session_config(self, session_data, file_path):
        with open(file_path, "w") as f:
            json.dump(session_data, f)
        logger.info(f"Session config exported to {file_path}")

    def import_session_config(self, file_path):
        with open(file_path, "r") as f:
            session_data = json.load(f)
        self.open_session(session_data)
        logger.info(f"Session config imported from {file_path}")

    def create_session_group(self, name, sessions):
        group = {"name": name, "sessions": sessions}
        self.saved_sessions.append(group)
        self.save_sessions()
        logger.info(f"Session group created: {name}")

    def open_session_group(self, group_name):
        group = next(
            (
                g
                for g in self.saved_sessions
                if g["name"] == group_name and "sessions" in g
            ),
            None,
        )
        if group:
            for session in group["sessions"]:
                self.open_session(session)
            logger.info(f"Session group opened: {group_name}")
        else:
            logger.warning(f"Session group not found: {group_name}")

    def get_saved_sessions(self):
        return self.saved_sessions
