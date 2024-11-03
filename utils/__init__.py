"""Utility modules for Eagle Terminal.

This package contains various utility functions and classes used
throughout the Eagle Terminal application, including logging, error
handling, and more.
"""

from .logger import logger
from .script_runner import ScriptRunner

__all__ = ["logger", "ScriptRunner"]
