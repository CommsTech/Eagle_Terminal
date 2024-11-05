from unittest.mock import MagicMock

import pytest
from PyQt5.QtWidgets import QApplication

from ai.chief import Chief
from ui.main_window.main_window import MainWindow
from utils.settings_manager import SettingsManager


@pytest.fixture
def app(qtbot):
    """Create QApplication instance."""
    return QApplication.instance() or QApplication([])


@pytest.fixture
async def chief():
    """Create Chief instance for testing."""
    config = {"model_name": "distilgpt2", "max_length": 512}
    chief_instance = Chief(config=config)
    await chief_instance.initialize()
    return chief_instance


@pytest.fixture
def settings_manager():
    """Create SettingsManager instance for testing."""
    return SettingsManager()


@pytest.fixture
def main_window(app, qtbot, settings_manager, chief):
    """Create MainWindow instance with required dependencies."""
    window = MainWindow(settings_manager=settings_manager, chief=chief)
    qtbot.addWidget(window)
    return window


@pytest.mark.asyncio
async def test_main_window_title(main_window):
    """Test window title."""
    assert main_window.windowTitle() == "Eagle Terminal"


@pytest.mark.asyncio
async def test_main_window_size(main_window):
    """Test window dimensions."""
    assert main_window.width() > 0
    assert main_window.height() > 0
