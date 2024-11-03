import logging
import os

import pytest
from PyQt5 import QtCore, QtTest, QtWidgets
from ai.chief import Chief
from ui.tabs.ssh_tab import SSHTab
from utils.logger import logger

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Check if running in CI environment
IS_CI = os.environ.get("CI", "false").lower() == "true"


@pytest.fixture(scope="session")
def qapp():
    if IS_CI:
        # Use offscreen platform plugin in CI environment
        os.environ["QT_QPA_PLATFORM"] = "offscreen"
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()


@pytest.fixture
def ssh_tab(qapp, qtbot, monkeypatch):
    logger.debug("Creating Chief")
    config = {"model_name": "distilgpt2", "max_length": 512}
    chief = Chief(config=config)
    logger.debug("Chief created")

    session_data = {
        "hostname": "test.example.com",
        "username": "test_user",
        "password": "test_password",
        "port": 22
    }

    tab = SSHTab(None)
    tab.chief = chief
    tab.session_data = session_data

    monkeypatch.setattr(tab, 'connect', lambda: None)
    monkeypatch.setattr(tab, 'disconnect', lambda: None)

    return tab


def test_init(ssh_tab):
    logger.debug("Starting test_init")
    assert isinstance(ssh_tab.chief, Chief)
    assert ssh_tab.command_history == []
    assert ssh_tab.history_index == -1
    assert isinstance(ssh_tab.ssh_connection, SSHConnection)
    assert "Connected successfully" in ssh_tab.terminal.toPlainText()
    logger.debug("test_init completed successfully")


@pytest.mark.parametrize(
    "command,expected_output",
    [
        ("ls", "file1.txt file2.txt"),
        ("pwd", "/home/user"),
    ],
)
def test_send_command(ssh_tab, qtbot, command, expected_output):
    qtbot.keyClicks(ssh_tab.terminal, command)
    qtbot.keyClick(ssh_tab.terminal, QtCore.Qt.Key_Return)

    # Check if the command was executed and output displayed
    assert command in ssh_tab.terminal.toPlainText()
    assert expected_output in ssh_tab.terminal.toPlainText()


def test_show_previous_command(ssh_tab, qtbot):
    ssh_tab.command_history = ["ls", "pwd", "echo hello"]
    ssh_tab.history_index = -1

    # Press up arrow key
    qtbot.keyClick(ssh_tab.terminal, QtCore.Qt.Key_Up)

    # Check if the last command is displayed
    assert ssh_tab.terminal.toPlainText().strip().endswith("echo hello")


def test_show_next_command(ssh_tab, qtbot):
    ssh_tab.command_history = ["ls", "pwd", "echo hello"]
    ssh_tab.history_index = 1

    # Press down arrow key
    qtbot.keyClick(ssh_tab.terminal, QtCore.Qt.Key_Down)

    # Check if the next command is displayed
    assert ssh_tab.terminal.toPlainText().strip().endswith("echo hello")


# Remove the macro-related tests as they are no longer part of SSHTab

if __name__ == "__main__":
    pytest.main()
