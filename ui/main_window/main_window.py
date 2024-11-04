import asyncio
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSlot  # type: ignore
from PyQt5.QtGui import QIcon  # type: ignore
from PyQt5.QtWidgets import QDialog  # type: ignore
from PyQt5.QtWidgets import (QAction, QApplication, QMainWindow, QMessageBox,
                             QSplitter, QTabWidget, QVBoxLayout, QWidget)
from qasync import QEventLoop, asyncSlot

from ai.chief import Chief
from plugins.meshtastic_chat import MeshtasticChat
from scripts.chief_learning import start_learning_session
from ui.dialogs.local_ai_dialog import \
    LocalAIDialog  # You'll need to create this dialog
from ui.dialogs.new_connection_wizard import NewConnectionWizard
from ui.dialogs.quick_connect_dialog import QuickConnectDialog
from ui.dialogs.remote_file_browser_dialog import RemoteFileBrowserDialog
from ui.elements.menu_bar import create_menu_bar
from ui.elements.toolbar import create_toolbar
from ui.tabs.device_list import DeviceList
from ui.tabs.ssh_tab import SSHTab
from ui.ui_setup import setup_main_window
from ui.widgets.device_list import DeviceListWidget
from utils.logger import logger
from utils.script_runner import ScriptRunner
from utils.settings_manager import SettingsManager
from utils.theme_manager import ThemeManager

from .device_management import DeviceManagement
from .device_status_management import DeviceStatusManagement
from .edit_actions import EditActions
from .error_handling import ErrorHandler
from .file_actions import FileActions
from .help_actions import HelpActions
from .meshtastic_chat_management import MeshtasticChatManagement
from .network_discovery_management import NetworkDiscoveryManagement
from .notes_management import NotesManagement
from .options_actions import OptionsActions
from .plugin_management import PluginManager
from .script_actions import ScriptActions
from .session_management import SessionManagement
from .settings_actions import SettingsActions
from .tools_actions import ToolsActions
from .transfer_actions import TransferActions
from .view_actions import ViewActions
from .window_actions import WindowActions


class MainWindow(QMainWindow):
    def __init__(self, settings_manager: SettingsManager, chief: Chief):
        super().__init__()
        self.settings_manager = settings_manager
        self.chief = chief

        if self.chief is None:
            logger.warning(
                "Chief AI assistant is not available. Some features will be disabled."
            )

        # Create a config dictionary for Chief
        chief_config = {
            "model_name": settings_manager.settings.get("model_name", "distilgpt2"),
            "max_length": settings_manager.settings.get("max_length", 1024),
            "learning_threshold": settings_manager.settings.get(
                "learning_threshold", 100
            ),
            "fine_tuning_epochs": settings_manager.settings.get(
                "fine_tuning_epochs", 3
            ),
            "batch_size": settings_manager.settings.get("batch_size", 8),
            "learning_rate": settings_manager.settings.get("learning_rate", 2e-5),
            # Add any other necessary configuration parameters
        }

        try:
            self.chief = Chief(chief_config)
            if not self.chief.is_functional():
                logger.warning(
                    "Chief AI assistant is not fully functional. Some AI features may be unavailable."
                )
        except Exception as e:
            logger.error(f"Failed to initialize Chief: {str(e)}")
            self.chief = None

        # Set up asyncio event loop
        self.loop = asyncio.get_event_loop()
        if not self.loop.is_running():
            self.async_start()

        self.setup_ui()
        ThemeManager.set_theme(QApplication.instance(), self.settings_manager.settings)

        self.open_sessions = []
        self.devices = []
        self.meshtastic_chat = None
        self.meshtastic_chat_management = None

        self.error_handler = ErrorHandler()

        self.init_ui_components()
        self.setup_actions()
        self.setup_components()

        # Set up event loop for asyncio
        self.tasks = []

    def setup_ui(self):
        self.setWindowTitle("Eagle Terminal")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(self.splitter)

        self.device_list = DeviceListWidget(self)
        self.splitter.addWidget(self.device_list)

        self.tab_widget = QtWidgets.QTabWidget()
        self.splitter.addWidget(self.tab_widget)

        self.splitter.setSizes(
            [200, 1000]
        )  # Set initial sizes for device list and main area

        self.status_bar = self.statusBar()

    def init_ui_components(self):
        # This method is now empty, but we'll keep it for potential future use
        pass

    def setup_actions(self):
        self.file_actions = FileActions(self)
        self.file_actions.new_session_requested.connect(self.new_session)
        self.edit_actions = EditActions(self)
        self.view_actions = ViewActions(self)
        self.options_actions = OptionsActions(self)
        self.transfer_actions = TransferActions(self)
        self.script_actions = ScriptActions(self)
        self.tools_actions = ToolsActions(self)
        self.window_actions = WindowActions(self)
        self.help_actions = HelpActions(self)
        self.settings_actions = SettingsActions(self)

        # Create AI menu if it doesn't exist
        self.ai_menu = self.menuBar().addMenu("AI")

        self.local_ai_action = QAction("Local AI", self)
        self.local_ai_action.triggered.connect(self.open_local_ai_dialog)

        # Add this action to the AI menu
        self.ai_menu.addAction(self.local_ai_action)

        self.setup_help_menu()

    def setup_components(self):
        try:
            logger.debug("Setting up MainWindow components")
            self.plugin_manager = PluginManager(self)
            self.script_runner = ScriptRunner()

            self.session_management = SessionManagement(self)
            self.network_discovery = NetworkDiscoveryManagement(self)
            self.device_status = DeviceStatusManagement(self)
            self.device_management = DeviceManagement(self)

            self.notes_management = NotesManagement(self)

            self.setup_menu_bar()
            self.setup_toolbar()
            setup_main_window(self)

            plugin_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "plugins"
            )
            self.plugin_manager.load_plugins(plugin_dir)
            self.script_runner.load_scripts()
            self.plugin_manager.initialize_plugins()

            self.device_management.update_device_list()

            self.device_status.start_status_check()
        except Exception as e:
            logger.error(f"Error setting up MainWindow: {str(e)}")
            self.error_handler.show_error(self, "Error setting up MainWindow", str(e))

    def setup_menu_bar(self):
        menu_bar = create_menu_bar(self)
        self.setMenuBar(menu_bar)
        logger.debug("Menu bar set up")

    def setup_toolbar(self):
        toolbar = create_toolbar(self)
        self.addToolBar(toolbar)
        logger.debug("Toolbar set up")

    def update_status(self, message):
        self.status_bar.showMessage(message, 5000)

    def get_open_sessions(self):
        return self.open_sessions

    def add_open_session(self, session_data):
        self.open_sessions.append(session_data)

    def remove_open_session(self, session_data):
        self.open_sessions.remove(session_data)

    def register_hook(self, hook_name, callback):
        self.plugin_manager.register_hook(hook_name, callback)

    @pyqtSlot()
    def new_connection(self):
        """Handle new connection request."""
        logger.info("New connection requested")
        asyncio.create_task(self.session_management.new_session())

    @asyncSlot()
    async def quick_connect(self):
        """Handle quick connect request."""
        logger.info("Quick connect requested")
        try:
            dialog = QuickConnectDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                session_data = dialog.get_connection_data()
                await self.create_ssh_tab(session_data)
        except AttributeError as e:
            logger.error(f"Error in quick_connect: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in quick_connect: {str(e)}")
            QMessageBox.critical(
                self, "Error", f"An unexpected error occurred: {str(e)}"
            )

    async def create_ssh_tab(self, session_data):
        try:
            ssh_tab = SSHTab(session_data, self.chief)
            index = self.tab_widget.addTab(ssh_tab, f"SSH: {session_data['hostname']}")
            self.tab_widget.setCurrentIndex(index)
            ThemeManager.set_terminal_theme(ssh_tab.terminal)
            ThemeManager.set_chief_output_theme(ssh_tab.chief_output)

            try:
                connected = await ssh_tab.connect_async()
                if connected:
                    self.tasks.append(ssh_tab)
                else:
                    self.tab_widget.removeTab(index)
                    QMessageBox.critical(
                        self,
                        "Connection Error",
                        "Failed to connect. Please check your credentials and try again.",
                    )
            except Exception as e:
                logger.error(f"Failed to connect: {str(e)}")
                self.tab_widget.removeTab(index)
                QMessageBox.critical(
                    self, "Connection Error", f"Failed to connect: {str(e)}"
                )

            return ssh_tab
        except Exception as e:
            logger.error(f"Error creating SSH tab: {str(e)}")
            QMessageBox.critical(
                self, "Error", f"An error occurred while creating the SSH tab: {str(e)}"
            )
            return None

    def toggle_insights(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab):
            current_tab.toggle_insights()

    def start_learning_session(self):
        start_learning_session(self.chief)

    def toggle_meshtastic_chat(self, checked):
        if checked:
            if self.meshtastic_chat_management is None:
                self.meshtastic_chat_management = MeshtasticChatManagement(self)
            self.meshtastic_chat_management.open_meshtastic_chat()
        else:
            if self.meshtastic_chat_management:
                self.meshtastic_chat_management.close_meshtastic_chat()

    def update_meshtastic_chat(self, message):
        self.meshtastic_chat_management.update_meshtastic_chat(message)

    def run_network_discovery(self):
        logger.info("Running network discovery")
        self.network_discovery.discover_devices()

    async def add_new_device(self):
        logger.info("Adding new device")
        await self.device_management.add_new_device()

    def open_device_notes(self):
        current_device = self.device_management.get_current_device()
        if current_device:
            self.notes_management.open_notes(current_device["id"])
        else:
            logger.warning("No device selected")
            self.error_handler.show_error(self, "Notes Error", "No device selected")

    def on_device_clicked(self, item, column):
        device_id = item.data(0, Qt.UserRole)
        self.device_management.reconnect_device(device_id)

    def open_settings(self):
        """Open the settings dialog."""
        logger.info("Opening settings dialog")
        self.settings_actions.open_settings_dialog()

    def closeEvent(self, event):
        """Handle the window close event."""
        logger.info("Closing application")
        asyncio.create_task(self.shutdown())
        event.accept()

    async def shutdown(self):
        """Perform asynchronous shutdown operations."""
        for task in self.tasks:
            if isinstance(task, asyncio.Task) and not task.done():
                try:
                    await asyncio.wait_for(task, timeout=5.0)
                except asyncio.TimeoutError:
                    task.cancel()
            elif asyncio.iscoroutine(task):
                await task
            elif callable(task):
                task()
            elif isinstance(task, SSHTab):
                await task.close()
            else:
                logger.warning(f"Unexpected task type during shutdown: {type(task)}")

    @pyqtSlot(dict)
    def update_device_list(self, new_device):
        self.device_management.update_device_list()

    def run_task(self, coro):
        if asyncio.iscoroutine(coro):
            task = asyncio.create_task(coro)
            self.tasks.append(task)
            task.add_done_callback(self.tasks.remove)
        elif callable(coro):
            self.tasks.append(coro)
        elif isinstance(coro, SSHTab):
            self.tasks.append(coro)
        else:
            logger.warning(f"Attempted to run non-coroutine task: {coro}")

    @asyncSlot()
    async def new_session(self):
        """Handle new session request."""
        logger.info("New session requested")
        await self.session_management.new_session(force_new=True)

    def disconnect_current_session(self):
        """Disconnect the current session."""
        logger.info("Disconnecting current session")
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab):
            current_tab.close()
            self.tab_widget.removeTab(self.tab_widget.currentIndex())
        else:
            logger.warning("No active SSH session to disconnect")

    def disconnect_all_sessions(self):
        """Disconnect all sessions."""
        logger.info("Disconnecting all sessions")
        for i in range(self.tab_widget.count() - 1, -1, -1):
            tab = self.tab_widget.widget(i)
            if isinstance(tab, SSHTab):
                tab.close()
                self.tab_widget.removeTab(i)

    def reconnect_current_session(self):
        """Reconnect the current session."""
        logger.info("Reconnecting current session")
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab):
            current_tab.reconnect()
        else:
            logger.warning("No active SSH session to reconnect")

    def reconnect_all_sessions(self):
        """Reconnect all sessions."""
        logger.info("Reconnecting all sessions")
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if isinstance(tab, SSHTab):
                tab.reconnect()

    def connect_in_tab(self):
        """Connect in a new tab."""
        logger.info("Connecting in a new tab")
        asyncio.create_task(self.new_session())

    def connect_in_shell(self):
        """Connect in a new shell."""
        logger.info("Connecting in shell")
        # TODO: Implement shell connection logic
        QMessageBox.information(
            self,
            "Not Implemented",
            "Connect in shell functionality is not yet implemented.",
        )

    def open_file_browser(self):
        """Open the file browser for the current session."""
        logger.info("Opening file browser for current session")
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, SSHTab) and current_tab.ssh_connection:
            try:
                sftp = current_tab.ssh_connection.open_sftp()
                dialog = RemoteFileBrowserDialog(sftp, self)
                dialog.exec_()

                # Update Chief with the file structure
                file_structure = self.get_file_structure(sftp)
                self.chief.learn("File Structure", file_structure)

                sftp.close()
            except Exception as e:
                logger.error(f"Failed to open SFTP browser: {str(e)}")
                self.error_handler.show_error(
                    "SFTP Error", f"Failed to open SFTP browser: {str(e)}"
                )
        else:
            logger.warning("No active SSH session to open file browser")

    def get_file_structure(self, sftp):
        """Get the file structure from the SFTP connection."""
        file_structure = {}
        try:
            for entry in sftp.listdir_attr("/"):
                name = entry.filename
                size = entry.st_size
                type_ = "Directory" if entry.longname.startswith("d") else "File"
                file_structure[name] = {"size": size, "type": type_}
        except Exception as e:
            logger.error(f"Error getting file structure: {str(e)}")
        return file_structure

    def run_script_dialog(self):
        """Open the run script dialog."""
        logger.info("Opening run script dialog")
        try:
            self.script_actions.run()
        except AttributeError:
            logger.error("ScriptActions not initialized or missing 'run' method")
            QMessageBox.warning(
                self,
                "Not Implemented",
                "Run script functionality is not yet fully implemented.",
            )

    def open_local_ai_dialog(self):
        """Open the Local AI dialog."""
        logger.info("Opening Local AI dialog")
        try:
            dialog = LocalAIDialog(self)
            dialog.exec_()
        except Exception as e:
            logger.error(f"Error opening Local AI dialog: {str(e)}")
            QMessageBox.critical(
                self, "Error", f"Failed to open Local AI dialog: {str(e)}"
            )

    def refresh_ui(self):
        """Refresh UI elements after settings change."""
        logger.info("Refreshing UI after settings change")
        # Add any UI refresh logic here
        # For example, update the status bar, refresh open tabs, etc.
        self.status_bar.showMessage("Settings updated", 3000)
        # You might want to update other UI elements based on the new settings

    def setup_help_menu(self):
        help_menu = self.menuBar().addMenu("Help")
        self.help_actions.setup_menu(help_menu)

    def open_help_topics(self):
        self.help_actions.show_help_topics()

    def async_start(self):
        def close_future(future, loop):
            loop.call_later(10, future.cancel)
            future.cancel()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        future = asyncio.Future()

        QApplication.instance().aboutToQuit.connect(lambda: close_future(future, loop))

        with QEventLoop(loop) as qloop:
            loop.run_until_complete(future)

    def open_sftp_browser(self):
        if self.current_ssh_tab and self.current_ssh_tab.is_connected:
            try:
                # SFTP browser logic here
                pass  # Replace this with actual SFTP browser logic
            except Exception as e:
                logger.error(f"Failed to open SFTP browser: {str(e)}")
                self.error_handler.show_error(
                    "SFTP Error", f"Failed to open SFTP browser: {str(e)}"
                )
        else:
            logger.warning("No active SSH session to open file browser")
