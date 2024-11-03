import json
import os

from utils.logger import logger


class SettingsManager:
    def __init__(self):
        """Initialize the settings for the class.
        
        This method initializes the class instance by setting up the path to the settings file
        and creating an empty dictionary to store the settings.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            settings_file (str): The path to the configuration file.
            settings (dict): An empty dictionary to store the settings.
        """
        self.settings_file = "config/settings.json"
        self.settings = {}

    def load_settings(self):
        """Loads settings from a file or uses default settings if the file is not found or cannot be parsed.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: The loaded settings as a dictionary.
        
        Raises:
            json.JSONDecodeError: If the settings file exists but cannot be parsed as JSON.
        
        Notes:
            - If the settings file exists and can be parsed, it loads the settings from the file.
            - If the file exists but cannot be parsed, it logs an error and uses default settings.
            - If the file does not exist, it logs an info message and uses default settings.
            - The method always returns a settings dictionary, either loaded or default.
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
            self: The instance of the class containing the settings and file path.
        
        Returns:
            None
        
        Raises:
            IOError: If there's an error writing to the file.
            JSONDecodeError: If there's an error encoding the settings to JSON.
        """
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        with open(self.settings_file, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get_default_settings(self):
        """Get the default settings for the application.
        
        Returns:
            dict: A dictionary containing the default settings for the application.
                Currently includes:
                - 'dark_theme' (bool): Whether the dark theme is enabled by default.
        """
        return {
            "dark_theme": False,
            # Add other default settings here
        }

    def get_setting(self, key, default=None):
        """Retrieve a setting value from the settings dictionary.
        
        Args:
            key (str): The key of the setting to retrieve.
            default (Any, optional): The default value to return if the key is not found. Defaults to None.
        
        Returns:
            Any: The value associated with the key if found, otherwise the default value.
        """
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """Sets a setting value for a given key and saves the settings.
        
        Args:
            key (str): The key of the setting to be set.
            value (Any): The value to be associated with the key.
        
        Returns:
            None
        """
        self.settings[key] = value
        self.save_settings()
