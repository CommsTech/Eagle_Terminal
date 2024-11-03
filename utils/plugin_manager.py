"""Plugin Manager module for Eagle Terminal.

This module provides functionality to load and manage plugins for Eagle
Terminal.
"""

import importlib
import os
from typing import Any, Dict

from utils.logger import logger


class PluginManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.plugin_dir = "plugins"
        self.plugins: Dict[str, Any] = {}
        self.hooks = {
            "on_connect": [],
            "on_disconnect": [],
            "on_command": [],
            "on_output": [],
            "on_main_window_created": [],
        }

    def load_plugins(self):
        """Load all plugins from the plugin directory."""
        if not os.path.exists(self.plugin_dir):
            logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                plugin_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{self.plugin_dir}.{plugin_name}")
                    if hasattr(module, "setup"):
                        self.plugins[plugin_name] = module
                        module.setup(self)
                        logger.info(f"Loaded plugin: {plugin_name}")
                    else:
                        logger.warning(f"Plugin {plugin_name} has no setup function")
                except Exception as e:
                    logger.error(f"Error loading plugin {plugin_name}: {str(e)}")

    def register_hook(self, hook_name, callback):
        """Register a callback function for a specific hook."""
        if hook_name in self.hooks:
            self.hooks[hook_name].append(callback)
        else:
            logger.warning(f"Unknown hook: {hook_name}")

    def trigger_hook(self, hook_name, *args, **kwargs):
        """Trigger a hook with the given arguments."""
        if hook_name in self.hooks:
            for callback in self.hooks[hook_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in plugin hook {hook_name}: {str(e)}")
        else:
            logger.warning(f"Unknown hook: {hook_name}")

    def get_plugin_list(self):
        """Return a list of all loaded plugin names."""
        return list(self.plugins.keys())

    def setup_plugins(self):
        for name, plugin in self.plugins.items():
            try:
                plugin.setup(self.main_window)
                logger.info(f"Set up plugin: {name}")
            except Exception as e:
                logger.error(f"Error setting up plugin {name}: {e}")
