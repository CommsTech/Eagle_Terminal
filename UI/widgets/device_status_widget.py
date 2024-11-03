"""This module contains widgets for displaying device status information.

It includes a ColorDot widget for visual status indication and a
DeviceStatusWidget for showing detailed device information.
"""

# pylint: disable=no-name-in-module,invalid-name
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class ColorDot(QWidget):
    """A widget that displays a colored dot."""

    def __init__(self, color, size=10, parent=None):
        """Initialize the ColorDot widget.

        Args:
            color (str): The color of the dot.
            size (int): The size of the dot in pixels.
            parent (QWidget): The parent widget.
        """
        super().__init__(parent)
        self.color = color
        self.size = size
        self.setFixedSize(size, size)

    def paintEvent(self, _):
        """Paint the colored dot."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, self.size, self.size)


class DeviceStatusWidget(QWidget):
    """A widget that displays the status of a device."""

    clicked = pyqtSignal()

    def __init__(self, device_id):
        """Initialize the DeviceStatusWidget.

        Args:
            device_id (str): The unique identifier for the device.
        """
        super().__init__()
        self.device_id = device_id
        self.layout = QVBoxLayout(self)
        self.name_label = QLabel()
        self.status_label = QLabel()
        self.error_label = QLabel()
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.error_label)

    def set_status(self, status):
        """Set the status of the device and update the display.

        Args:
            status (str): The current status of the device (e.g., "connected", "disconnected").
        """
        self.status_label.setText(status)
        if status.lower() == "connected":
            self.status_label.setStyleSheet("color: green;")
        elif status.lower() == "disconnected":
            self.status_label.setStyleSheet("color: red;")
        else:
            self.status_label.setStyleSheet("color: black;")

    def set_error(self, error):
        """Set the error message for the device.

        Args:
            error (str): The error message to display.
        """
        self.error_label.setText(error)

    def update_status(self, status):
        """Update the status and error message of the device.

        Args:
            status (dict or str): The status information for the device.
        """
        if isinstance(status, dict):
            self.set_status(status.get("status", "Unknown"))
            if "error" in status:
                self.set_error(status["error"])
        else:
            self.set_status(str(status))

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def set_name(self, name):
        """Set the name of the device and update the display.

        Args:
            name (str): The name of the device to be displayed.
        """
        self.name_label.setText(name)

    def update_device_info(self, device_info):
        """Update the device information displayed in the widget.

        Args:
            device_info (dict): A dictionary containing the device information.
                                Expected keys: 'name', 'status'.
        """
        self.set_name(device_info.get("name", "Unknown Device"))
        self.set_status(device_info.get("status", "Unknown"))

    def get_device_id(self):
        """Get the device ID associated with this widget.

        Returns:
            str: The unique identifier of the device.
        """
        return self.device_id
