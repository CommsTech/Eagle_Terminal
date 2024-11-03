import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QToolBar

from utils.logger import logger


def create_toolbar(parent):
    toolbar = QToolBar()
    toolbar.setMovable(False)
    toolbar.setFloatable(False)
    toolbar.setIconSize(QSize(24, 24))  # Use QSize instead of Qt.QSize

    icon_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons"
    )

    actions = [
        ("new_session.png", "New Session", "Create a new session", parent.new_session),
        (
            "quick_connect.png",
            "Quick Connect",
            "Quickly connect to a host",
            parent.quick_connect,
        ),
        (None, None, None, None),  # Separator
        (
            "disconnect.png",
            "Disconnect",
            "Disconnect from the current session",
            parent.disconnect_current_session,
        ),
        (
            "reconnect.png",
            "Reconnect",
            "Reconnect to the current session",
            parent.reconnect_current_session,
        ),
        (None, None, None, None),  # Separator
        (
            "file_browser.png",
            "File Browser",
            "Open the file browser for the current session",
            parent.open_file_browser,
        ),
        (
            "run_script.png",
            "Run Script",
            "Run a script on the current session",
            parent.run_script_dialog,
        ),
        (None, None, None, None),  # Separator
        (
            "ai_assistant.png",
            "Local AI",
            "Open the Local AI dialog",
            parent.open_local_ai_dialog,
        ),
        (
            "meshtastic_chat.png",
            "Meshtastic Chat",
            "Toggle Meshtastic Chat",
            parent.toggle_meshtastic_chat,
        ),
        (
            "network_discovery.png",
            "Network Discovery",
            "Run network discovery",
            parent.run_network_discovery,
        ),
        ("add_device.png", "Add New Device", "Add a new device", parent.add_new_device),
        (
            "notes.png",
            "Device Notes",
            "Open device notes",
            parent.open_device_notes,
        ),
    ]

    # Add Meshtastic Chat action only if the library is available
    try:
        from meshtastic import SerialInterface

        actions.insert(
            -2,
            (
                "meshtastic_chat.png",
                "Meshtastic Chat",
                "Toggle Meshtastic Chat",
                parent.toggle_meshtastic_chat,
            ),
        )
    except ImportError:
        logger.warning(
            "Meshtastic library not found. Meshtastic Chat feature will not be available."
        )

    for icon_file, text, status_tip, callback in actions:
        if icon_file is None:
            toolbar.addSeparator()
        else:
            action = QAction(QIcon(os.path.join(icon_path, icon_file)), text, parent)
            action.setStatusTip(status_tip)
            action.triggered.connect(callback)
            if text == "Meshtastic Chat":
                action.setCheckable(True)
                action.toggled.connect(callback)
            toolbar.addAction(action)

    return toolbar
