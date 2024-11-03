from utils.logger import logger


class PluginActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def register_hook(self, hook_name, callback):
        self.main_window.plugin_manager.register_hook(hook_name, callback)

    # Add other plugin-related methods here
