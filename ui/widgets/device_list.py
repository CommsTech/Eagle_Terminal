from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QTreeWidget,
                             QTreeWidgetItem)

from .device_status_widget import DeviceStatusWidget


class DeviceList(QListWidget):
    device_selected = pyqtSignal(str)  # Signal to emit the selected device ID

    def __init__(self, parent=None):
        super().__init__(parent)
        self.itemClicked.connect(self.on_item_clicked)

    def add_device(self, device_id, device_info):
        item = QListWidgetItem(self)
        device_widget = DeviceStatusWidget(device_id)
        device_widget.update_status(device_info)
        item.setSizeHint(device_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, device_widget)

    def update_device_status(self, device_id, status):
        for index in range(self.count()):
            item = self.item(index)
            widget = self.itemWidget(item)
            if isinstance(widget, DeviceStatusWidget) and widget.device_id == device_id:
                widget.update_status(status)
                break

    def on_item_clicked(self, item):
        widget = self.itemWidget(item)
        if isinstance(widget, DeviceStatusWidget):
            self.device_selected.emit(widget.device_id)

    def clear_devices(self):
        self.clear()


class DeviceListWidget(QTreeWidget):
    device_selected = pyqtSignal(str)  # Signal to emit the selected device ID

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setHeaderLabels(["Device", "Status"])
        self.itemClicked.connect(self.on_item_clicked)

    def add_device(self, device_info):
        print(f"Adding device to UI list: {device_info}")
        item = QTreeWidgetItem(self)
        item.setText(0, device_info["name"])
        item.setText(1, device_info.get("connection_type", "Unknown"))
        item.setData(0, Qt.UserRole, device_info["id"])
        print(f"Current item count: {self.topLevelItemCount()}")

    def clear(self):
        super().clear()
        print("Cleared device list")

    def on_item_clicked(self, item, column):
        device_id = item.data(0, Qt.UserRole)
        self.device_selected.emit(device_id)
