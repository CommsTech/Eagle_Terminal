import json
import os

from utils.logger import logger


class SettingsManager:
    def __init__(self):
        self.settings_file = "config/settings.json"
        self.settings = {}

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    self.settings = json.load(f)
            except json.JSONDecodeError:
                logger.error("Failed to parse settings file. Using default settings.")
        else:
            logger.info("Settings file not found. Using default settings.")
            self.settings = self.get_default_settings()
        return self.settings

    def save_settings(self):
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_default_settings(self):
        return {
            "dark_theme": False,
            # Add other default settings here
        }

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()
