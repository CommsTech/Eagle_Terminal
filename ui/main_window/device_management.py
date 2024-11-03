import asyncio
import json
import os

from cryptography.fernet import Fernet
from PyQt5.QtCore import Q_ARG, QMetaObject, QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QInputDialog, QMenu, QMessageBox, QTreeWidgetItem

from ui.widgets.device_list import DeviceListWidget
from ui.widgets.device_status_widget import DeviceStatusWidget
from utils.logger import logger


class DeviceManagement(QObject):
    device_clicked = pyqtSignal(str)  # Signal for device clicks
    device_added = pyqtSignal(dict)  # Signal for new device added

    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.devices = []
        self.key_file = "device_key.key"
        self.devices_file = "devices.enc"
        self.load_or_create_key()
        self.load_devices()
        self.main_window.device_list.itemClicked.connect(self.on_device_clicked)

    def load_or_create_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        self.fernet = Fernet(key)

    def load_devices(self):
        if os.path.exists(self.devices_file):
            with open(self.devices_file, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.devices = json.loads(decrypted_data)
        else:
            self.devices = []
        self.update_device_list()

    def save_devices(self):
        encrypted_data = self.fernet.encrypt(json.dumps(self.devices).encode())
        with open(self.devices_file, "wb") as file:
            file.write(encrypted_data)
        logger.info("Devices saved and encrypted successfully")

    def update_device_list(self):
        self.main_window.device_list.clear()
        for device in self.devices:
            self.main_window.device_list.add_device(device)

    async def add_device(self, device_data):
        device_id = self.generate_device_id()
        new_device = {
            "id": device_id,
            "name": device_data.get("name")
            or device_data.get("hostname")
            or f"Device_{device_id}",
            "hostname": device_data.get("hostname", ""),
            "username": device_data.get("username", ""),
            "password": device_data.get("password", ""),
            "port": device_data.get("port", 22),
            "connection_type": device_data.get("connection_type", "SSH"),
            "os_type": device_data.get("os_type", "unknown"),
        }
        self.devices.append(new_device)
        await self.save_devices()
        self.device_added.emit(new_device)
        self.main_window.update_status(f"New device '{new_device['name']}' added")
        logger.info(f"New device added: {new_device['name']}")

        # Update the UI in the main thread
        QMetaObject.invokeMethod(
            self.main_window,
            "update_device_list",
            Qt.QueuedConnection,
            Q_ARG(dict, new_device),
        )

        # Update the sidebar
        if hasattr(self.main_window, "sidebar"):
            self.main_window.sidebar.update_saved_connections(self.devices)

    def edit_device(self, device_id):
        device = self.get_device(device_id)
        if device:
            name, ok = QInputDialog.getText(
                self.main_window, "Edit Device", "Enter new name:", text=device["name"]
            )
            if ok and name:
                device["name"] = name
                hostname, ok = QInputDialog.getText(
                    self.main_window,
                    "Edit Device",
                    "Enter new hostname or IP:",
                    text=device["hostname"],
                )
                if ok and hostname:
                    device["hostname"] = hostname
                    self.save_devices()
                    self.update_device_list()
                    self.main_window.update_status(f"Device '{name}' updated")

    def delete_device(self, device_id):
        device = self.get_device(device_id)
        if device:
            reply = QMessageBox.question(
                self.main_window,
                "Delete Device",
                f"Are you sure you want to delete {device['name']}?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.devices = [d for d in self.devices if d["id"] != device_id]
                self.save_devices()
                self.update_device_list()
                self.main_window.update_status(f"Device '{device['name']}' deleted")

    def get_device(self, device_id):
        for device in self.devices:
            if device["id"] == device_id:
                return device
        return None

    def get_devices(self):
        """Get all devices.

        Returns:
            list: A list of all devices.
        """
        return self.devices

    def generate_device_id(self):
        return str(max([int(d["id"]) for d in self.devices] + [0]) + 1)

    def show_device_context_menu(self, position):
        item = self.main_window.device_list.itemAt(position)
        if item is None:
            return

        device_id = item.data(0, Qt.UserRole)
        device = self.get_device(device_id)

        context_menu = QMenu()
        edit_action = context_menu.addAction("Edit")
        delete_action = context_menu.addAction("Delete")
        connect_action = context_menu.addAction("Connect")

        action = context_menu.exec_(self.main_window.device_list.mapToGlobal(position))

        if action == edit_action:
            self.edit_device(device_id)
        elif action == delete_action:
            self.delete_device(device_id)
        elif action == connect_action:
            # Use QTimer to schedule the async operation
            QTimer.singleShot(0, lambda: self.connect_to_device(device_id))

    def add_device(self, device_data):
        print(f"Adding device to list: {device_data}")
        new_device = {
            "id": self.generate_device_id(),
            "name": device_data.get("name", device_data["hostname"]),
            "hostname": device_data["hostname"],
            "username": device_data["username"],
            "password": device_data.get("password", ""),
            "port": device_data.get("port", 22),
            "connection_type": device_data.get("connection_type", "SSH"),
        }
        self.devices.append(new_device)
        self.save_devices()

        # Update the UI
        self.main_window.device_list.add_device(new_device)

        self.main_window.update_status(f"New device '{new_device['name']}' added")
        logger.info(f"New device added: {new_device['name']}")
        return new_device

    def on_device_clicked(self, item, column):
        device_id = item.data(0, Qt.UserRole)
        self.device_clicked.emit(device_id)

    def reconnect_device(self, device_id):
        device = self.get_device(device_id)
        if device:
            try:
                self.main_window.session_management.reconnect_session(device)
                logger.info(f"Reconnected to device: {device['name']}")
            except Exception as e:
                logger.error(
                    f"Failed to reconnect to device {device['name']}: {str(e)}"
                )
                self.main_window.error_handler.show_error(
                    "Reconnection Error",
                    f"Failed to reconnect to {device['name']}: {str(e)}",
                )
        else:
            logger.error(f"Device with ID {device_id} not found")

    def get_current_device(self):
        current_item = self.main_window.device_list.currentItem()
        if current_item:
            device_id = current_item.data(0, Qt.UserRole)
            return self.get_device(device_id)
        return None

    def update_device_status(self, device_id, status):
        for i in range(self.main_window.device_list.topLevelItemCount()):
            item = self.main_window.device_list.topLevelItem(i)
            if item.data(0, Qt.UserRole) == device_id:
                status_widget = self.main_window.device_list.itemWidget(item, 1)
                if status_widget:
                    status_widget.update_status(status)
                break

    def get_device_widget(self, device_id):
        """Get the device widget for a specific device.

        Args:
            device_id (str): The ID of the device.

        Returns:
            DeviceStatusWidget: The widget for the specified device, or None if not found.
        """
        for i in range(self.main_window.device_list.topLevelItemCount()):
            item = self.main_window.device_list.topLevelItem(i)
            if item.data(0, Qt.UserRole) == device_id:
                return self.main_window.device_list.itemWidget(item, 1)
        return None

    async def add_new_device(self):
        """Open a dialog to add a new device and add it to the list."""
        from ui.dialogs.quick_connect_dialog import QuickConnectDialog

        dialog = QuickConnectDialog(self.main_window)
        if dialog.exec_():
            device_data = dialog.get_session_data()
            new_device = self.add_device(device_data)  # Use the synchronous version
            logger.info(f"New device added: {new_device['name']}")
        else:
            logger.info("New device addition cancelled")

    def connect_to_device(self, device_id):
        # This method will be called in the main event loop
        asyncio.ensure_future(self.async_connect_to_device(device_id))

    async def async_connect_to_device(self, device_id):
        # Use force_new=False when connecting to an existing device
        await self.main_window.session_management.new_session(force_new=False)
