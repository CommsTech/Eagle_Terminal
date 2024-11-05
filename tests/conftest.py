from utils.settings_manager import SettingsManager
from ai.chief import Chief
import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

import pytest
from PyQt5 import QtWidgets

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def qapp():
    """Create QApplication instance."""
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    yield app
    app.quit()


@pytest.fixture
async def chief():
    """Create Chief instance with mocked components."""
    config = {"model_name": "distilgpt2", "max_length": 512}
    chief_instance = Chief(config=config)

    # Mock the components to avoid actual model loading
    chief_instance.model_manager = MagicMock()
    chief_instance.command_analyzer = MagicMock()
    chief_instance.command_learner = MagicMock()
    chief_instance.response_generator = MagicMock()

    # Mock async methods
    chief_instance.analyze_command_output = AsyncMock(
        return_value="Command executed successfully"
    )
    chief_instance.suggest_next_command = AsyncMock(return_value="Suggested command")

    yield chief_instance
    if hasattr(chief_instance, "cleanup"):
        await chief_instance.cleanup()


@pytest.fixture
def settings_manager():
    """Create SettingsManager instance."""
    return SettingsManager()
