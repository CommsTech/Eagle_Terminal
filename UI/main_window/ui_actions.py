from utils.logger import logger


class UIActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def update_status(self, message):
        self.main_window.status_bar.showMessage(
            message, 5000
        )  # Show message for 5 seconds

    # Add other UI-related methods here
