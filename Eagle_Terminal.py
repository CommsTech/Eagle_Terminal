"""
Eagle Terminal - A powerful SSH client with AI assistance.

This module serves as the entry point for the Eagle Terminal application,
initializing the main window and setting up the AI assistant.
"""

import asyncio
import sys

from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop

from ai.chief import Chief
from ui.main_window.main_window import MainWindow
from utils.logger import logger
from utils.settings_manager import SettingsManager


async def main():
    """
    Initialize and run the Eagle Terminal application.

    This function sets up the QApplication, initializes the AI assistant,
    and creates the main window of the application.
    """
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    settings_manager = SettingsManager()

    # Create a config dictionary for Chief
    chief_config = {
        "model_name": settings_manager.settings.get("model_name", "gpt2"),
        "max_length": settings_manager.settings.get("max_length", 512),
        "learning_threshold": settings_manager.settings.get("learning_threshold", 100),
        "fine_tuning_epochs": settings_manager.settings.get("fine_tuning_epochs", 3),
        "batch_size": settings_manager.settings.get("batch_size", 8),
        "learning_rate": settings_manager.settings.get("learning_rate", 2e-5),
    }

    chief = None
    try:
        chief = Chief(chief_config)
        await chief.initialize()
        if not chief.is_functional():
            logger.warning(
                "Chief AI assistant is not fully functional. Some AI features may be unavailable."
            )
    except (ValueError, RuntimeError) as e:
        logger.error("Failed to initialize Chief: %s", str(e), exc_info=True)
        chief = None

    main_window = MainWindow(settings_manager, chief)
    main_window.show()

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error("Fatal error: %s", str(e), exc_info=True)
        sys.exit(1)
