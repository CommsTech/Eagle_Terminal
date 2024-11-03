from utils.logger import logger


class DeviceActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def add_device(self):
        self.main_window.device_management.add_new_device()

    def edit_device(self, device_id):
        self.main_window.device_management.edit_device(device_id)

    def delete_device(self, device_id):
        self.main_window.device_management.delete_device(device_id)

    def connect_to_device(self, device_id):
        device = self.main_window.device_management.get_device(device_id)
        if device:
            self.main_window.session_management.new_session(device)
        else:
            logger.error(f"Device with ID {device_id} not found")

    def refresh_device_status(self, device_id):
        self.main_window.device_status_management.refresh_device_status(device_id)

    def show_device_details(self, device_id):
        device = self.main_window.device_management.get_device(device_id)
        if device:
            # Implement a method to display device details in a dialog or panel
            self.main_window.show_device_details_dialog(device)
        else:
            logger.error(f"Device with ID {device_id} not found")
