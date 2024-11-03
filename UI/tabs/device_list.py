from typing import Dict, List

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor  # Import QColor for color manipulation
from PyQt5.QtWidgets import QAction, QMenu, QTreeWidget, QTreeWidgetItem


class DeviceList(QTreeWidget):
    device_clicked = pyqtSignal(str)  # Signal emitted when a device is clicked
    device_double_clicked = pyqtSignal(
        str
    )  # Signal emitted when a device is double-clicked

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["Device", "Type", "Status"])
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.itemClicked.connect(self.on_item_clicked)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.devices = []  # List to store device data

    def populate_devices(self, devices: List[Dict]):
        """Populate the device list with the provided devices.

        Args:
            devices (List[Dict]): A list of dictionaries containing device information.
        """
        self.clear()
        self.devices = devices
        for device in devices:
            item = QTreeWidgetItem(self)
            item.setText(0, device.get("name", "Unknown"))
            item.setText(1, device.get("type", "Unknown"))
            item.setText(2, device.get("status", "Unknown"))
            item.setData(0, Qt.UserRole, device.get("id"))

    def add_device(self, device: Dict):
        """Add a single device to the list.

        Args:
            device (Dict): A dictionary containing device information.
        """
        item = QTreeWidgetItem(self)
        item.setText(0, device.get("name", "Unknown"))
        item.setText(1, device.get("type", "Unknown"))
        item.setText(2, device.get("status", "Unknown"))
        item.setData(0, Qt.UserRole, device.get("id"))
        self.devices.append(device)

    def remove_device(self, device_id: str):
        """Remove a device from the list.

        Args:
            device_id (str): The ID of the device to remove.
        """
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.data(0, Qt.UserRole) == device_id:
                self.takeTopLevelItem(i)
                self.devices = [d for d in self.devices if d.get("id") != device_id]
                break

    def update_device_status(self, device_id: str, status: str):
        """Update the status of a device in the list.

        Args:
            device_id (str): The ID of the device to update.
            status (str): The new status of the device.
        """
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            if item.data(0, Qt.UserRole) == device_id:
                item.setText(2, status)
                if status.lower() == "connected":
                    item.setForeground(2, QColor("green"))
                elif status.lower() == "disconnected":
                    item.setForeground(2, QColor("red"))
                else:
                    item.setForeground(2, QColor("black"))
                for device in self.devices:
                    if device.get("id") == device_id:
                        device["status"] = status
                        break
                break

    def show_context_menu(self, position):
        """Show a context menu when right-clicking on a device.

        Args:
            position: The position where the context menu should be shown.
        """
        item = self.itemAt(position)
        if item is not None:
            device_id = item.data(0, Qt.UserRole)
            context_menu = QMenu(self)

            connect_action = QAction("Connect", self)
            connect_action.triggered.connect(lambda: self.connect_to_device(device_id))
            context_menu.addAction(connect_action)

            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda: self.edit_device(device_id))
            context_menu.addAction(edit_action)

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_device(device_id))
            context_menu.addAction(delete_action)

            context_menu.exec_(self.mapToGlobal(position))

    def on_item_clicked(self, item, column):
        """Handle single-click events on devices.

        Args:
            item: The clicked item.
            column: The clicked column.
        """
        device_id = item.data(0, Qt.UserRole)
        self.device_clicked.emit(device_id)

    def on_item_double_clicked(self, item, column):
        """Handle double-click events on devices.

        Args:
            item: The double-clicked item.
            column: The double-clicked column.
        """
        device_id = item.data(0, Qt.UserRole)
        self.device_double_clicked.emit(device_id)

    def connect_to_device(self, device_id: str):
        """Connect to the selected device.

        Args:
            device_id (str): The ID of the device to connect to.
        """
        # This method should be implemented in the main window or a connection manager
        print(f"Connecting to device: {device_id}")

    def edit_device(self, device_id: str):
        """Edit the selected device.

        Args:
            device_id (str): The ID of the device to edit.
        """
        # This method should be implemented in the main window or a device manager
        print(f"Editing device: {device_id}")

    def delete_device(self, device_id: str):
        """Delete the selected device.

        Args:
            device_id (str): The ID of the device to delete.
        """
        # This method should be implemented in the main window or a device manager
        print(f"Deleting device: {device_id}")

    def get_device_by_id(self, device_id: str) -> Dict:
        """Get a device's information by its ID.

        Args:
            device_id (str): The ID of the device to retrieve.

        Returns:
            Dict: The device information, or None if not found.
        """
        for device in self.devices:
            if device.get("id") == device_id:
                return device
        return None
