"""Macro Manager module for Eagle Terminal.

This module provides functionality to record, save, and playback command
macros.
"""

import json
import os
from typing import Dict, List

from utils.logger import logger


class MacroManager:
    def __init__(self, macro_file: str = "macros.json"):
        """Initialize the MacroManager.
        
        This method initializes a MacroManager object, setting up the necessary attributes
        and loading existing macros from a file.
        
        Args:
            macro_file (str, optional): The path to the JSON file containing saved macros.
                                        Defaults to "macros.json".
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the specified macro file does not exist.
            json.JSONDecodeError: If the macro file contains invalid JSON.
        """
        self.macro_file = macro_file
        self.macros: Dict[str, List[str]] = {}
        self.current_macro: List[str] = []
        self.is_recording = False
        self.load_macros()

    def start_recording(self, macro_name: str):
        """Start recording a new macro."""
        self.is_recording = True
        self.current_macro = []
        logger.info(f"Started recording macro: {macro_name}")

    def stop_recording(self, macro_name: str):
        """Stop recording the current macro and save it."""
        self.is_recording = False
        self.macros[macro_name] = self.current_macro
        self.current_macro = []
        self.save_macros()
        logger.info(f"Stopped recording macro: {macro_name}")

    def add_command(self, command: str):
        """Add a command to the current macro if recording."""
        if self.is_recording:
            self.current_macro.append(command)

    def play_macro(self, macro_name: str) -> List[str]:
        """Play back a recorded macro."""
        if macro_name in self.macros:
            logger.info(f"Playing macro: {macro_name}")
            return self.macros[macro_name]
        else:
            logger.warning(f"Macro not found: {macro_name}")
            return []

    def save_macros(self):
        """Save all macros to a file."""
        try:
            with open(self.macro_file, "w") as f:
                json.dump(self.macros, f)
            logger.info("Macros saved successfully")
        except Exception as e:
            logger.error(f"Error saving macros: {str(e)}")

    def load_macros(self):
        """Load macros from a file."""
        if os.path.exists(self.macro_file):
            try:
                with open(self.macro_file, "r") as f:
                    self.macros = json.load(f)
                logger.info("Macros loaded successfully")
            except Exception as e:
                logger.error(f"Error loading macros: {str(e)}")
        else:
            logger.info("No macro file found. Starting with empty macros.")

    def get_macro_list(self) -> List[str]:
        """Return a list of all available macro names."""
        return list(self.macros.keys())
