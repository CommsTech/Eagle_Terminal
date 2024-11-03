import importlib
import os

from utils.logger import logger


class PluginManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.plugins = {}

    def load_plugins(self, plugin_dir):
        logger.info(f"Loading plugins from {plugin_dir}")
        for filename in os.listdir(plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                plugin_path = os.path.join(plugin_dir, filename)
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "Plugin"):
                    self.plugins[plugin_name] = module.Plugin(self.main_window)
                    logger.info(f"Loaded plugin: {plugin_name}")

    def initialize_plugins(self):
        for plugin_name, plugin in self.plugins.items():
            try:
                plugin.initialize()
                logger.info(f"Initialized plugin: {plugin_name}")
            except Exception as e:
                logger.error(f"Error initializing plugin {plugin_name}: {str(e)}")

    def register_hook(self, hook_name, callback):
        for plugin in self.plugins.values():
            if hasattr(plugin, hook_name):
                getattr(plugin, hook_name)(callback)

    # Implement other necessary methods
