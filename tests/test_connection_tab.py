import asyncio
import logging
import os
from unittest.mock import AsyncMock, MagicMock

import pytest
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from ai.chief import Chief
from ui.tabs.ssh_tab import SSHTab
from utils.logger import logger

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="function")
def event_loop():
    """Create an event loop for testing."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    # Clean up pending tasks
    pending = asyncio.all_tasks(loop)
    for task in pending:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    loop.close()


@pytest.fixture
def qapp():
    """Create a QApplication instance for testing."""
    if os.environ.get("CI"):
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    yield app
    app.quit()


@pytest.fixture
async def chief():
    """Create a Chief instance for testing."""
    config = {"model_name": "distilgpt2", "max_length": 512}
    chief_instance = Chief(config=config)
    await chief_instance.initialize()
    yield chief_instance
    # Cleanup
    if hasattr(chief_instance, "cleanup"):
        await chief_instance.cleanup()


@pytest.fixture
def ssh_tab(qapp, qtbot, chief):
    """Create an SSHTab instance for testing."""
    session_data = {
        "hostname": "test.example.com",
        "username": "test_user",
        "password": "test_password",
        "port": 22,
        "os_type": "linux",
    }

    # Create SSHTab with session_data and chief
    tab = SSHTab(session_data=session_data, chief=chief)

    # Initialize terminal for testing
    tab.terminal = QtWidgets.QTextEdit()
    qtbot.addWidget(tab.terminal)

    # Mock methods
    tab.connect = AsyncMock()
    tab.disconnect = AsyncMock()
    tab.ssh_connection = MagicMock()
    tab.command_history = []
    tab.history_index = -1

    return tab


@pytest.mark.asyncio
async def test_init(ssh_tab):
    """Test SSHTab initialization."""
    assert isinstance(ssh_tab, SSHTab)
    assert ssh_tab.command_history == []
    assert ssh_tab.history_index == -1
    assert ssh_tab.os_type == "linux"
    assert ssh_tab.session_data["hostname"] == "test.example.com"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "command,expected_output", [("ls", "file1.txt file2.txt"), ("pwd", "/home/user")]
)
async def test_send_command(ssh_tab, qtbot, command, expected_output):
    """Test sending commands to the terminal."""
    # Set up terminal content
    ssh_tab.terminal.setText("")

    # Send command
    qtbot.keyClicks(ssh_tab.terminal, command)
    qtbot.keyClick(ssh_tab.terminal, Qt.Key_Return)

    # Add expected output to terminal
    ssh_tab.terminal.append(expected_output)

    # Check if the command was executed and output displayed
    assert command in ssh_tab.terminal.toPlainText()
    assert expected_output in ssh_tab.terminal.toPlainText()


@pytest.mark.asyncio
async def test_show_previous_command(ssh_tab, qtbot):
    """Test showing previous command with up arrow key."""
    ssh_tab.command_history = ["ls", "pwd", "echo hello"]
    ssh_tab.history_index = -1

    # Press up arrow key
    qtbot.keyClick(ssh_tab.terminal, Qt.Key_Up)

    # Check if the last command is displayed
    assert ssh_tab.terminal.toPlainText().strip().endswith("echo hello")


@pytest.mark.asyncio
async def test_show_next_command(ssh_tab, qtbot):
    """Test showing next command with down arrow key."""
    ssh_tab.command_history = ["ls", "pwd", "echo hello"]
    ssh_tab.history_index = 1

    # Press down arrow key
    qtbot.keyClick(ssh_tab.terminal, Qt.Key_Down)

    # Check if the next command is displayed
    assert ssh_tab.terminal.toPlainText().strip().endswith("echo hello")
