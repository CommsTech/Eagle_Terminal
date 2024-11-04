import re
import threading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtGui import QTextCursor
    from PyQt5.QtWidgets import QTextEdit
else:
    from PyQt5.QtCore import Qt, pyqtSignal
    from PyQt5.QtGui import QTextCursor
    from PyQt5.QtWidgets import QTextEdit


class SSHConsole(QTextEdit):
    command_executed = pyqtSignal(str, str)  # command, output

    def __init__(self, session_data, chief):
        super().__init__()
        self.session_data = session_data
        self.chief = chief
        self.ssh_client = None
        self.shell = None
        self.setReadOnly(False)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setUndoRedoEnabled(False)
        self.prompt = ""
        self.current_command = ""
        self.command_history = []
        self.history_index = 0
        self.ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

    def set_ssh_client(self, ssh_client):
        self.ssh_client = ssh_client

    def set_shell(self, shell):
        self.shell = shell
        if self.shell:
            self.read_output()

    def read_output(self):
        def _read():
            while self.shell:
                if self.shell.recv_ready():
                    data = self.shell.recv(1024).decode("utf-8")
                    cleaned_data = self.ansi_escape.sub("", data)
                    self.append_output(cleaned_data)
                    if cleaned_data.strip().endswith("$"):
                        self.prompt = cleaned_data.strip()

        threading.Thread(target=_read, daemon=True).start()

    def keyPressEvent(self, event):
        if self.shell:
            if event.key() == Qt.Key_Return:
                self.execute_command()
            elif event.key() == Qt.Key_Backspace:
                if self.textCursor().positionInBlock() > len(self.prompt):
                    super().keyPressEvent(event)
            elif event.key() == Qt.Key_Up:
                self.show_previous_command()
            elif event.key() == Qt.Key_Down:
                self.show_next_command()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def execute_command(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
        command = cursor.selectedText()[len(self.prompt):].strip()

        if command:
            self.append("")  # Move to the next line
            self.shell.send(command + "\n")
            self.command_history.append(command)
            self.history_index = len(self.command_history)
            self.current_command = ""

            # Ask Chief for assistance
            self.get_chief_assistance(command)

    def get_chief_assistance(self, command):
        if self.chief:
            assistance = self.chief.analyze_command(command)
            self.append_output(f"\nChief's Assistance: {assistance}\n")

    def show_previous_command(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.show_command_from_history()

    def show_next_command(self):
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.show_command_from_history()
        elif self.history_index == len(self.command_history) - 1:
            self.history_index += 1
            self.clear_current_command()

    def show_command_from_history(self):
        self.clear_current_command()
        if 0 <= self.history_index < len(self.command_history):
            self.insertPlainText(self.command_history[self.history_index])

    def clear_current_command(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()
        self.insertPlainText(self.prompt)

    def append_output(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
