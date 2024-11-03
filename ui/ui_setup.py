from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QSplitter, QVBoxLayout, QWidget

from ui.tabs.ssh_tab import SSHTab
from utils.logger import logger


def setup_main_window(main_window):
    logger.debug("Setting up UI")

    # Set up the device list
    main_window.device_list.setHeaderLabel("Devices")
    main_window.device_list.setContextMenuPolicy(Qt.CustomContextMenu)
    main_window.device_list.customContextMenuRequested.connect(
        main_window.device_management.show_device_context_menu
    )

    # Set up the tab widget
    main_window.tab_widget.setTabsClosable(True)
    main_window.tab_widget.tabCloseRequested.connect(
        main_window.session_management.close_session
    )

    # Set splitter sizes
    main_window.splitter.setSizes(
        [int(main_window.width() * 0.2), int(main_window.width() * 0.8)]
    )

    logger.debug("UI setup complete")


def setup_ui(main_window, chief):
    # ... other UI setup code ...

    session_data = (
        main_window.session_manager.get_current_session()
    )  # Assuming you have a session manager
    ssh_tab = SSHTab(session_data, chief)
    main_window.addTab(ssh_tab, "SSH")

    # ... rest of the UI setup ...
