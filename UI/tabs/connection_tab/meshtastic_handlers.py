from utils.logger import logger


def toggle_meshtastic_chat(self, state):
    if hasattr(self.main_window, "meshtastic_chat_management"):
        self.main_window.meshtastic_chat_management.toggle_meshtastic_chat(state)
    else:
        logger.warning("Meshtastic chat management not available")
