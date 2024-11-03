"""Error Handler module for Eagle Terminal's AI system.

This module provides functionality to handle and log errors that occur
during the execution of AI-related tasks in the Eagle Terminal.
"""

import logging
from functools import wraps
from typing import Callable


class AIErrorHandler:
    """A class for handling and logging errors in AI-related tasks.

    This class sets up a logger to record errors and provides a
    decorator to wrap functions for error handling.
    """

    def __init__(self):
        """Initialize the AIErrorHandler with a configured logger."""
        self.logger = logging.getLogger("ai_error_handler")
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("ai_errors.log")
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def handle_error(self, func: Callable):
        """Decorator to handle errors in the wrapped function.

        This decorator catches any exceptions raised in the wrapped function,
        logs the error, and re-raises the exception.

        Args:
            func (Callable): The function to be wrapped for error handling.

        Returns:
            Callable: The wrapped function with error handling.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.logger.error(
                    "Error in %s: %s", func.__name__, str(e), exc_info=True
                )
                raise

        return wrapper


error_handler = AIErrorHandler()
