import pytest
from PyQt5.QtWidgets import QApplication

from ui.main_window.main_window import MainWindow


@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])


@pytest.fixture
def main_window(app, qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def test_main_window_title(main_window):
    assert main_window.windowTitle() == "Eagle Terminal"


def test_main_window_size(main_window):
    assert main_window.width() > 0
    assert main_window.height() > 0
