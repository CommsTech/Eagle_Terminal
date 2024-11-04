import json
import os

from utils.logger import logger


class SettingsManager:
    def __init__(self):
        """Initialize the class instance.
        
        This method initializes the class instance by setting up the settings file path
        and creating an empty dictionary to store the settings.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            settings_file (str): The path to the settings JSON file.
            settings (dict): An empty dictionary to store the loaded settings.
        """
        self.settings_file = "config/settings.json"
        self.settings = {}

    def load_settings(self):
        """Loads settings from a file or sets default settings if the file is not found or cannot be parsed.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: A dictionary containing the loaded settings.
        
        Raises:
            json.JSONDecodeError: If the settings file exists but cannot be parsed as JSON.
        """
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
        """Saves the current settings to a JSON file.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            JSONEncodeError: If there's an error encoding the settings to JSON.
            PermissionError: If the method doesn't have write permissions for the target directory.
        """
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_default_settings(self):
        """Returns the default settings for the application.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: A dictionary containing the default settings for the application.
                  Currently includes:
                  - 'dark_theme': A boolean indicating whether dark theme is enabled by default (False).
        """
        return {
            "dark_theme": False,
            # Add other default settings here
        }

    def get_setting(self, key, default=None):
        """Retrieves a setting value from the settings dictionary.
        
        Args:
            key (str): The key of the setting to retrieve.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.
        
        Returns:
            Any: The value associated with the given key in the settings dictionary, or the default value if the key is not found.
        """
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """Sets a setting value for a given key and saves the settings.
        
        Args:
            key (str): The key of the setting to be set.
            value (Any): The value to be associated with the key.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            KeyError: If the key is not a valid setting.
            TypeError: If the value is not of the expected type for the given key.
        """
        self.settings[key] = value
        self.save_settings()
