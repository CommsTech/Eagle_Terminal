import asyncio
import re

from PyQt5.QtCore import QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QTextCursor
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QInputDialog,
                             QLineEdit, QMessageBox, QPushButton, QSplitter,
                             QTextEdit, QVBoxLayout, QWidget)

from ai.chief import Chief
from utils.logger import logger
from utils.ssh_utils import SSHConnection


class SSHWorker(QObject):
    output_ready = pyqtSignal(str, str)

    def __init__(self, ssh_connection):
        super().__init__()
        self.ssh_connection = ssh_connection

    async def run_command(self, command):
        try:
            stdout, stderr = await self.ssh_connection.async_execute_command(command)
            self.output_ready.emit(stdout, stderr)
        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            self.output_ready.emit("", str(e))


class SSHTab(QWidget):
    def __init__(self, session_data, chief: Chief):
        super().__init__()
        self.session_data = session_data
        self.chief = chief
        self.ssh_connection = None
        self.command_history = []
        self.history_index = -1
        self.os_type = session_data.get("os_type", "unknown")
        self.is_cisco = "cisco" in self.os_type.lower()
        self.init_ui()
        self.is_connected = False
        self.insights_visible = True
        self.setup_chief_interaction()
        self.last_prompt_position = 0
        self.output_buffer = ""
        self.read_output_task = None
        self.sudo_in_progress = False

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Create a splitter to separate the terminal and Chief's analysis
        self.splitter = QSplitter(Qt.Vertical)

        # Terminal
        self.terminal = QTextEdit()
        self.terminal.setFont(QFont("Consolas", 10))
        self.terminal.setStyleSheet(
            """
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
                padding: 5px;
            }
        """
        )
        self.terminal.keyPressEvent = self.terminal_key_press
        self.splitter.addWidget(self.terminal)

        # Chief's analysis output
        self.chief_output = QTextEdit()
        self.chief_output.setFont(QFont("Consolas", 9))
        self.chief_output.setStyleSheet(
            """
            QTextEdit {
                background-color: #2d2d2d;
                color: #87CEFA;
                border: none;
                padding: 5px;
            }
        """
        )
        self.chief_output.setReadOnly(True)
        self.splitter.addWidget(self.chief_output)

        # Set initial sizes (70% terminal, 30% Chief's output)
        self.splitter.setSizes([700, 300])

        layout.addWidget(self.splitter)

    async def connect_async(self):
        try:
            port = int(self.session_data.get("port", 22))
            self.ssh_connection = SSHConnection(
                hostname=self.session_data["hostname"],
                username=self.session_data["username"],
                password=self.session_data.get("password"),
                key_filename=self.session_data.get("key_filename"),
                port=port,
            )
            connected, os_type = await self.ssh_connection.async_connect()
            if connected:
                self.is_connected = True
                self.os_type = os_type
                self.is_cisco = os_type == "cisco"
                self.show_prompt()
                self.read_output_task = asyncio.create_task(self.read_output_loop())
                return True
            else:
                raise Exception(
                    "Failed to connect. Please check your credentials and try again."
                )
        except Exception as e:
            logger.error(
                f"Failed to connect to {self.session_data['hostname']}: {str(e)}"
            )
            QMessageBox.critical(
                self, "Connection Error", f"Failed to connect: {str(e)}"
            )
            return False

    async def read_output_loop(self):
        while self.is_connected:
            try:
                output = await asyncio.wait_for(
                    self.ssh_connection.read_output(), timeout=0.1
                )
                if output:
                    self.output_buffer += output
                    self.update_terminal()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in read_output_loop: {str(e)}")
                break
            await asyncio.sleep(0.01)

    def update_terminal(self):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)

        # Updated ANSI escape sequence pattern
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

        # Remove ANSI escape sequences and other control characters
        clean_text = ansi_escape.sub("", self.output_buffer)
        clean_text = re.sub(
            r"^\s*[=>]\s*", "", clean_text, flags=re.MULTILINE
        )  # Remove leading '=' or '>'

        cursor.insertText(clean_text)
        self.terminal.setTextCursor(cursor)
        self.terminal.ensureCursorVisible()
        self.output_buffer = ""
        QApplication.processEvents()

    def terminal_key_press(self, event):
        if event.key() == Qt.Key_Return:
            cursor = self.terminal.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            line = cursor.selectedText()
            command = line.split("$ ", 1)[-1].strip()
            if command:
                self.last_command = command
                self.command_history.append(command)
                self.history_index = -1
                self.terminal.insertPlainText("\n")  # Add a new line after the command
                asyncio.create_task(self.send_command(command))
            else:
                self.show_prompt()
        elif event.key() == Qt.Key_Up:
            self.show_previous_command()
        elif event.key() == Qt.Key_Down:
            self.show_next_command()
        elif event.key() == Qt.Key_C and (event.modifiers() & Qt.ControlModifier):
            asyncio.create_task(self.send_ctrl_c())
        else:
            QTextEdit.keyPressEvent(self.terminal, event)

    async def send_command(self, command):
        if self.ssh_connection and self.ssh_connection.channel:
            try:
                # Don't echo the command locally
                await self.ssh_connection.write_input(command + "\n")

                # Wait for the command output
                output = await self.read_command_output(command)
                if output:
                    self.terminal.insertPlainText(output)
                    self.terminal.moveCursor(QTextCursor.End)
                    QApplication.processEvents()

                if self.chief and self.chief.is_functional():
                    analysis = await self.chief.analyze_command_output(
                        command, output, self.os_type
                    )
                    self.chief_output.clear()
                    self.chief_output.append("Chief's Analysis:")
                    self.chief_output.append(analysis["basic_analysis"])

                    next_command = await self.chief.suggest_next_command(
                        self.command_history, {"os_type": self.os_type}
                    )
                    risk_level = self.assess_risk_level(
                        next_command.split()[0] if next_command else ""
                    )

                    self.chief_output.append("\nSuggested next command:")
                    self.chief_output.append(f"{next_command}")
                    self.chief_output.append(f"Risk Level: {risk_level}")
            except Exception as e:
                self.terminal.append(f"Error: {str(e)}")
                if "SSH connection closed" in str(e):
                    self.reconnect()
                else:
                    QMessageBox.critical(
                        self,
                        "Command Execution Error",
                        f"An error occurred while executing the command: {str(e)}",
                    )
        else:
            self.terminal.append("Not connected to SSH server.")

    async def read_command_output(self, command):
        output = ""
        command_echo_received = False
        prompt_received = False
        while not prompt_received:
            chunk = await self.ssh_connection.read_output()
            if not chunk:
                await asyncio.sleep(0.1)
                continue

            # Remove the echoed command from the output
            if not command_echo_received:
                if command in chunk:
                    chunk = chunk.replace(command + "\r\n", "", 1)
                    command_echo_received = True

            output += chunk

            # Check if we've received the prompt, indicating the command has finished
            if self.session_data["username"] in chunk and (
                "$ " in chunk or "# " in chunk
            ):
                prompt_received = True

        # Clean up the output
        output = self.clean_ansi_escape_sequences(output)
        output = output.strip()

        # Remove the final prompt from the output
        prompt = f"{self.session_data['username']}@{self.session_data['hostname']}:~$ "
        output = output.rsplit(prompt, 1)[0]

        return output.strip()

    def clean_ansi_escape_sequences(self, text):
        ansi_escape = re.compile(
            r"""
            \x1B  # ESC
            (?:   # 7-bit C1 Fe (except CSI)
                [@-Z\\-_]
            |     # or [ for CSI, followed by a control sequence
                \[
                [0-?]*  # Parameter bytes
                [ -/]*  # Intermediate bytes
                [@-~]   # Final byte
            )
        """,
            re.VERBOSE,
        )
        return ansi_escape.sub("", text)

    async def handle_sudo_command(self, command):
        if self.sudo_in_progress:
            return

        self.sudo_in_progress = True
        try:
            password, ok = QInputDialog.getText(
                self, "Sudo Password", "Enter sudo password:", QLineEdit.Password
            )
            if not ok:
                self.terminal.append("Sudo command cancelled")
                return

            # Send the sudo command
            await self.ssh_connection.write_input(f"{command}\n")

            # Wait for password prompt
            while True:
                output = await self.ssh_connection.read_output()
                if output:
                    self.terminal.insertPlainText(output)
                    self.terminal.moveCursor(QTextCursor.End)
                    QApplication.processEvents()
                if "[sudo] password for" in output:
                    break

            # Send the password
            await self.ssh_connection.write_input(f"{password}\n")

            # Read and display the output
            while True:
                output = await self.ssh_connection.read_output()
                if output:
                    # Mask the password in the output
                    output = output.replace(password, "*" * len(password))
                    self.terminal.insertPlainText(output)
                    self.terminal.moveCursor(QTextCursor.End)
                    QApplication.processEvents()
                if self.session_data["username"] in output and "$" in output:
                    break  # Command prompt returned, sudo command completed
        finally:
            self.sudo_in_progress = False

    async def handle_real_time_command(self, command):
        while True:
            output = await self.ssh_connection.read_output()
            if not output:
                break
            self.output_buffer += output
            self.update_terminal()
            await asyncio.sleep(0.1)

    async def send_ctrl_c(self):
        if self.ssh_connection and self.ssh_connection.channel:
            await self.ssh_connection.write_input("\x03")  # Send Ctrl+C character

    async def handle_ansible_playbook(self, command):
        await self.send_command(command)

    async def process_output(self, stdout_gen, stderr_gen, channel):
        async def read_stream(stream_gen):
            async for line in stream_gen:
                self.terminal.append(line.strip())
                self.terminal.moveCursor(QTextCursor.End)
                QApplication.processEvents()

        stdout_task = asyncio.create_task(read_stream(stdout_gen))
        stderr_task = asyncio.create_task(read_stream(stderr_gen))

        await asyncio.gather(stdout_task, stderr_task)
        exit_status = await asyncio.get_event_loop().run_in_executor(
            None, channel.recv_exit_status
        )

        if exit_status != 0:
            self.terminal.append(f"Command exited with status: {exit_status}")

    def assess_risk_level(self, command: str) -> str:
        """Assess the risk level of a suggested command."""
        high_risk_keywords = ["rm", "mkfs", "dd", "format", "fdisk"]
        medium_risk_keywords = ["chmod", "chown", "mount", "umount", "kill"]

        command_lower = command.lower()

        if any(keyword in command_lower for keyword in high_risk_keywords):
            return "High"
        elif any(keyword in command_lower for keyword in medium_risk_keywords):
            return "Medium"
        else:
            return "Low"

    def show_prompt(self):
        prompt = f"{self.session_data['username']}@{self.session_data['hostname']}:~$ "
        self.terminal.insertPlainText(prompt)
        self.terminal.moveCursor(QTextCursor.End)
        self.last_prompt_position = self.terminal.textCursor().position()

    def show_previous_command(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.set_command_in_terminal(
                self.command_history[-(self.history_index + 1)]
            )

    def show_next_command(self):
        if self.history_index > -1:
            self.history_index -= 1
            if self.history_index == -1:
                self.set_command_in_terminal("")
            else:
                self.set_command_in_terminal(
                    self.command_history[-(self.history_index + 1)]
                )

    def set_command_in_terminal(self, command):
        cursor = self.terminal.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        cursor.insertText(
            f"{self.session_data['username']}@{self.session_data['hostname']}:~$ {command}"
        )

    def closeEvent(self, event):
        if self.ssh_connection:
            self.ssh_connection.close()
        super().closeEvent(event)

    def toggle_insights(self):
        """Toggle the visibility of Chief's analysis output."""
        if self.insights_visible:
            # Hide Chief's output
            self.chief_output.hide()
            # Adjust splitter sizes to give full height to terminal
            self.splitter.setSizes([self.height(), 0])
        else:
            # Show Chief's output
            self.chief_output.show()
            # Restore original splitter sizes
            self.splitter.setSizes([self.height() * 0.7, self.height() * 0.3])

        # Toggle the visibility state
        self.insights_visible = not self.insights_visible

    def reconnect(self):
        """Reconnect to the SSH server."""
        logger.debug("Reconnecting to SSH")
        if self.ssh_connection:
            self.ssh_connection.close()
        asyncio.create_task(self.connect_async())

    def display_session_info(self):
        info = f"Connected to {self.session_data['hostname']} as {self.session_data['username']}\n"
        info += f"OS Type: {self.os_type}\n"
        info += f"Connection Type: {'Cisco' if self.is_cisco else 'Standard'} SSH\n"
        info += "-" * 40 + "\n"
        self.terminal.append(info)

    async def close(self):
        self.is_connected = False
        if self.read_output_task:
            self.read_output_task.cancel()
            try:
                await self.read_output_task
            except asyncio.CancelledError:
                pass
        if self.ssh_connection:
            await self.ssh_connection.close()
        self.ssh_connection = None

    def setup_chief_interaction(self):
        self.chief_input = QLineEdit()
        self.chief_input.setPlaceholderText("Ask Chief a question...")
        self.chief_input.returnPressed.connect(self.trigger_send_chief_query)

        chief_input_layout = QHBoxLayout()
        chief_input_layout.addWidget(self.chief_input)

        ask_chief_button = QPushButton("Ask Chief")
        ask_chief_button.clicked.connect(self.trigger_send_chief_query)
        chief_input_layout.addWidget(ask_chief_button)

        self.layout().addLayout(chief_input_layout)

    def trigger_send_chief_query(self):
        asyncio.create_task(self.send_chief_query())

    async def send_chief_query(self):
        query = self.chief_input.text()
        self.chief_input.clear()

        if self.chief and self.chief.is_functional():
            try:
                response = await self.chief.direct_interaction(
                    query, {"os_type": self.os_type}
                )
                self.chief_output.append(f"You: {query}")
                self.chief_output.append(f"Chief: {response}")
            except Exception as e:
                self.chief_output.append(
                    f"Error: Failed to get response from Chief. {str(e)}"
                )
        else:
            self.chief_output.append("Error: Chief AI assistant is not available.")

    async def read_stream(self, stream, is_error=False):
        while True:
            line = await stream.readline()
            if not line:
                break
            decoded_line = line.decode().strip()
            if is_error:
                self.terminal.append(f"<span style='color: red;'>{decoded_line}</span>")
            else:
                self.terminal.append(decoded_line)
            self.terminal.moveCursor(QTextCursor.End)
            QApplication.processEvents()
