"""Connection Tab module for managing SSH and Serial connections.

This module provides a GUI tab for establishing and managing
connections, sending commands, and handling command history and
autocompletion.
"""

from PyQt5.QtCore import QStringListModel, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QCompleter, QHBoxLayout, QLabel, QWidget

from connections.serial_connection import SerialConnection
from connections.ssh_connection import SSHConnection
from ui.elements.keyword_highlighter import KeywordHighlighter
from utils.input_validation import validate_connection_params
from utils.macro_manager import MacroManager
from utils.session_manager import SessionManager

from .connection_handlers import connect, send_command, update_terminal
from .event_handlers import handle_key_press, on_terminal_change
from .macro_handlers import play_macro, toggle_macro_recording
from .meshtastic_handlers import toggle_meshtastic_chat
from .ui_setup import setup_ui


class ConnectionThread(QThread):
    """Thread for handling connections."""

    output_received = pyqtSignal(str)
    connection_closed = pyqtSignal()

    def __init__(self, connection):
        """Initialize the ConnectionThread."""
        super().__init__()
        self.connection = connection
        self.connection.output_received.connect(self.output_received.emit)
        self.connection.connection_closed.connect(self.connection_closed.emit)

    def run(self):
        """Run the connection thread."""
        self.connection.connect()


class ConnectionTab(QWidget):
    """Main widget for the Connection Tab."""

    def __init__(self, parent):
        """Initialize the ConnectionTab."""
        super().__init__(parent)
        self.parent = parent
        self.connection = None
        self.connection_thread = None
        self.macro_manager = MacroManager()
        self.command_history = []
        self.history_index = 0
        self.session_manager = SessionManager()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QHBoxLayout(self)
        self = setup_ui(self)

        self.highlighter = KeywordHighlighter(
            self.terminal.document(), self.parent.chief
        )

        self.connect_button.clicked.connect(self.connect)
        self.command_input.returnPressed.connect(self.send_command)
        self.record_macro_button.clicked.connect(self.toggle_macro_recording)
        self.play_macro_button.clicked.connect(self.play_macro)

        self._setup_command_history_and_autocomplete()
        self._setup_chief_overlay()

    def _setup_command_history_and_autocomplete(self):
        """Set up command history and autocomplete functionality."""
        self.command_input.installEventFilter(self)
        self.completer = QCompleter(self)
        self.completer.setModel(QStringListModel())
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.command_input.setCompleter(self.completer)

    def _setup_chief_overlay(self):
        """Set up Chief's assistance overlay."""
        self.chief_overlay = QLabel(self.command_input)
        self.chief_overlay.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.8); color: #333; padding: 2px;"
        )
        self.chief_overlay.hide()

    def eventFilter(self, obj, event):
        """Handle key press events for command history navigation."""
        if obj == self.command_input and event.type() == event.KeyPress:
            if event.key() == Qt.Key_Up:
                self.show_previous_command()
                return True
            elif event.key() == Qt.Key_Down:
                self.show_next_command()
                return True
        return super().eventFilter(obj, event)

    def show_previous_command(self):
        """Show the previous command in history."""
        if self.history_index > 0:
            self.history_index -= 1
            self.command_input.setText(self.command_history[self.history_index])

    def show_next_command(self):
        """Show the next command in history or clear if at the end."""
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.setText(self.command_history[self.history_index])
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.command_input.clear()

    def connect(self):
        """Establish a connection."""
        connection_type = self.connection_type_combo.currentText()
        host = self.host_input.text()
        port = self.port_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not validate_connection_params(
            connection_type, host, port, username, password
        ):
            self.terminal.append(
                "Invalid connection parameters. Please check your inputs."
            )
            return

        if connection_type == "SSH":
            self.connection = SSHConnection(host, port, username, password)
        elif connection_type == "Serial":
            self.connection = SerialConnection(port)
        else:
            self.terminal.append(f"Unsupported connection type: {connection_type}")
            return

        session_id = self.session_manager.add_session(connection_type, self.connection)
        self.terminal.append(f"Session {session_id} created.")

        self.connection_thread = ConnectionThread(self.connection)
        self.connection_thread.output_received.connect(self.update_terminal)
        self.connection_thread.connection_closed.connect(self.on_connection_closed)
        self.connection_thread.start()

        self.terminal.append(f"Connecting to {connection_type}...")
        self.connect_button.setEnabled(False)

    def toggle_macro_recording(self):
        """Toggle macro recording."""
        if self.macro_manager.is_recording:
            self.macro_manager.stop_recording()
            self.record_macro_button.setText("Record Macro")
            self.terminal.append("Macro recording stopped.")
        else:
            macro_name = self.macro_name_input.text()
            if not macro_name:
                self.terminal.append("Please enter a name for the macro.")
                return
            self.macro_manager.start_recording(macro_name)
            self.record_macro_button.setText("Stop Recording")
            self.terminal.append(f"Started recording macro: {macro_name}")

    def play_macro(self):
        """Play a recorded macro."""
        macro_name = self.macro_name_input.text()
        if not macro_name:
            self.terminal.append("Please enter the name of the macro to play.")
            return

        macro = self.macro_manager.get_macro(macro_name)
        if not macro:
            self.terminal.append(f"Macro '{macro_name}' not found.")
            return

        for command in macro:
            self.send_command(command)
            # Add a small delay between commands to simulate user input
            QThread.msleep(100)

        self.terminal.append(f"Finished playing macro: {macro_name}")

    def send_command(self, command=None):
        """Send a command through the established connection."""
        if command is None:
            command = self.command_input.text()
        if self.connection and self.connection.connected:
            self.connection.send_command(command)
            self.command_input.clear()
            self.add_to_history(command)
            self.update_autocomplete()
            if self.macro_manager.is_recording:
                self.macro_manager.add_command(command)
        else:
            self.terminal.append("Not connected. Please connect first.")

    def add_to_history(self, command):
        """Add a command to the history."""
        if command and (
            not self.command_history or command != self.command_history[-1]
        ):
            self.command_history.append(command)
            if len(self.command_history) > 100:  # Limit history to 100 commands
                self.command_history.pop(0)
        self.history_index = len(self.command_history)

    def update_autocomplete(self):
        """Update autocomplete suggestions."""
        all_commands = set(self.command_history)
        chief_suggestions = self.parent.chief.suggest_commands(
            self.command_input.text()
        )
        all_commands.update(chief_suggestions)
        self.completer.model().setStringList(list(all_commands))

    def update_terminal(self, output):
        """Update the terminal with output and Chief's insights."""
        self.terminal.append(output)
        insights = self.parent.chief.analyze_command_output(
            self.command_input.text(), output
        )
        if insights:
            self.terminal.append(f"Chief's insights: {insights}")

    def on_connection_closed(self):
        """Handle connection closure."""
        self.terminal.append("Connection closed.")
        if self.connection:
            session_id = next(
                (
                    sid
                    for sid, conn in self.session_manager.get_all_sessions().items()
                    if conn == self.connection
                ),
                None,
            )
            if session_id:
                self.session_manager.remove_session(session_id)
                self.terminal.append(f"Session {session_id} removed.")
        self.connection = None
        self.connect_button.setEnabled(True)

    def on_command_input_changed(self, text):
        """Handle changes in command input."""
        self.update_autocomplete()
        assistance = self.parent.chief.suggest_command_completion(text)
        if assistance:
            self.show_chief_assistance(assistance)
        else:
            self.chief_overlay.hide()

    def show_chief_assistance(self, assistance):
        """Display Chief's assistance overlay."""
        self.chief_overlay.setText(assistance)
        self.chief_overlay.adjustSize()
        self.chief_overlay.move(self.command_input.cursorRect().topRight())
        self.chief_overlay.show()

    def reconnect(self):
        """Reconnect to the current connection."""
        if self.connection:
            self.connection.close()
        self.connect()

    def toggle_macro_recording(self):
        """Toggle macro recording."""
        # TODO: Implement macro recording logic
        pass

    def play_macro(self):
        """Play a recorded macro."""
        # TODO: Implement macro playback logic
        pass
