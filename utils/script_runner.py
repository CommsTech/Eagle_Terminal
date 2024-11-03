"""Script Runner module for Eagle Terminal.

This module provides functionality to run automation scripts within
Eagle Terminal.
"""

import importlib.util
import os

from utils import logger


class ScriptRunner:
    def __init__(self):
        self.scripts = {}

    def load_scripts(self):
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
        if script_name in self.scripts:
            return self.scripts[script_name].run(*args, **kwargs)
        else:
            logger.error(f"Script not found: {script_name}")
            return None
