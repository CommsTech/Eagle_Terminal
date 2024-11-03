"""Logger module for Eagle Terminal.

This module provides a setup function for creating and configuring
loggers used throughout the Eagle Terminal application.
"""

import logging
import os


def setup_logger():
    """Set up and configure the logger for the application.

    Returns:
        logging.Logger: The configured logger instance.
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)

    # Set up logging
    logger = logging.getLogger("eagle_terminal")
    logger.setLevel(logging.DEBUG)

    # Create file handler
    file_handler = logging.FileHandler(os.path.join(log_dir, "eagle_terminal.log"))
    file_handler.setLevel(logging.DEBUG)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Create and export the logger instance
logger = setup_logger()
