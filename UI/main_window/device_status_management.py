import asyncio

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from utils.device_status import get_device_info, get_device_status
from utils.logger import logger


class DeviceStatusManagement(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.check_interval = 60  # Check every 60 seconds
        self.status_check_task = None
        self.is_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_devices_status)

    def check_devices_status(self):
        try:
            logger.debug("Checking devices status")
            for device in self.main_window.device_management.get_devices():
                try:
                    # Implement your device status check logic here
                    # For example:
                    # status = self.check_device_status(device)
                    # self.update_device_status(device, status)
                    pass
                except Exception as e:
                    logger.error(
                        f"Error checking status for device {device['name']}: {str(e)}"
                    )
        except Exception as e:
            logger.error(f"Unexpected error in device status check: {str(e)}")

    def check_device_status(self, device):
        # This is a placeholder implementation. Replace with actual device checking logic.
        device_info = get_device_info(device["ip"])
        status = get_device_status(device_info)
        return status

    def update_device_status(self, device, status):
        # Find the device in the device list and update its status
        for i in range(self.main_window.device_list.topLevelItemCount()):
            item = self.main_window.device_list.topLevelItem(i)
            if item.text(0) == device["name"]:
                item.setText(1, status)
                break

    def start_status_check(self):
        if not self.timer.isActive():
            self.timer.start(
                self.check_interval * 1000
            )  # Convert seconds to milliseconds

    def stop_status_check(self):
        if self.timer.isActive():
            self.timer.stop()
