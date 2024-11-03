import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QProgressBar, QVBoxLayout, QWidget


class DetailedDeviceStatusWidget(QWidget):
    """A widget that displays detailed status information for a device.

    This widget shows the device name, OS, uptime, CPU usage, memory
    usage, and the time since the last update.
    """

    def __init__(self, parent=None):
        """Initialize the DetailedDeviceStatusWidget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.init_ui()
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_time)
        self.update_timer.start(1000)  # Update every second

    def init_ui(self):
        """Initialize the user interface components of the widget."""
        layout = QVBoxLayout(self)

        self.name_label = QLabel()
        self.os_label = QLabel()
        self.uptime_label = QLabel()
        self.cpu_bar = QProgressBar()
        self.memory_bar = QProgressBar()
        self.last_update_label = QLabel()

        layout.addWidget(self.name_label)
        layout.addWidget(self.os_label)
        layout.addWidget(self.uptime_label)
        layout.addWidget(self.cpu_bar)
        layout.addWidget(self.memory_bar)
        layout.addWidget(self.last_update_label)

    def update_status(self, status):
        """Update the widget with new status information.

        Args:
            status (dict): A dictionary containing the device status information.
                           Expected keys: 'name', 'os', 'uptime', 'cpu_usage', 'memory_usage'.
        """
        self.name_label.setText(f"Name: {status.get('name', 'Unknown')}")
        self.os_label.setText(f"OS: {status.get('os', 'Unknown')}")
        self.uptime_label.setText(f"Uptime: {status.get('uptime', 'Unknown')}")

        cpu_usage = status.get("cpu_usage", "Unknown")
        if cpu_usage != "Unknown":
            cpu_value = int(cpu_usage.rstrip("%"))
            self.cpu_bar.setValue(cpu_value)
            self.cpu_bar.setFormat(f"CPU: {cpu_usage}")
        else:
            self.cpu_bar.setValue(0)
            self.cpu_bar.setFormat("CPU: Unknown")

        memory_usage = status.get("memory_usage", "Unknown")
        if memory_usage != "Unknown":
            memory_value = int(memory_usage.rstrip("%"))
            self.memory_bar.setValue(memory_value)
            self.memory_bar.setFormat(f"Memory: {memory_usage}")
        else:
            self.memory_bar.setValue(0)
            self.memory_bar.setFormat("Memory: Unknown")

        self.last_update_time = datetime.datetime.now()
        self.update_time()

    def update_time(self):
        """Update the 'last update' time display."""
        if hasattr(self, "last_update_time"):
            time_diff = datetime.datetime.now() - self.last_update_time
            self.last_update_label.setText(f"Last update: {time_diff.seconds}s ago")

    def clear(self):
        """Clear all status information from the widget."""
        self.name_label.clear()
        self.os_label.clear()
        self.uptime_label.clear()
        self.cpu_bar.setValue(0)
        self.cpu_bar.setFormat("CPU: N/A")
        self.memory_bar.setValue(0)
        self.memory_bar.setFormat("Memory: N/A")
        self.last_update_label.clear()
