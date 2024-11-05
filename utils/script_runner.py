"""Script Runner module for Eagle Terminal.

This module provides functionality to run automation scripts within
Eagle Terminal.
"""

import importlib.util
import os

from utils import logger


class ScriptRunner:
    def __init__(self):
        """Initialize a new instance of the class.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            scripts (dict): A dictionary to store scripts.
        """
        self.scripts = {}

    def load_scripts(self):
        """Loads Python scripts from a specified directory and adds them to the scripts dictionary.
        
        This method scans the '../scripts' directory relative to the current file's location,
        imports all '.py' files as modules, and stores them in the self.scripts dictionary
        with the script name (without extension) as the key and the imported module as the value.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None: This method doesn't return anything, but it populates the self.scripts dictionary.
        
        Raises:
            ImportError: If there's an issue importing any of the script files.
            FileNotFoundError: If the scripts directory doesn't exist.
        """
        script_dir = os.path.join(os.path.dirname(__file__), "..", "scripts")
        for filename in os.listdir(script_dir):
            if filename.endswith(".py"):
                script_name = filename[:-3]
                script_path = os.path.join(script_dir, filename)
                spec = importlib.util.spec_from_file_location(script_name, script_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                self.scripts[script_name] = module
                logger.info(f"Loaded script: {script_name}")

    def run_script(self, script_name, *args, **kwargs):
        """Executes a script with the given name and arguments.
        
        Args:
            script_name (str): The name of the script to run.
            *args: Variable length argument list to pass to the script.
            **kwargs: Arbitrary keyword arguments to pass to the script.
        
        Returns:
            Any: The result of the script execution, or None if the script is not found.
        
        Raises:
            None: The method doesn't raise exceptions, but logs an error if the script is not found.
        """
        if script_name in self.scripts:
            return self.scripts[script_name].run(*args, **kwargs)
        else:
            logger.error(f"Script not found: {script_name}")
            return None
