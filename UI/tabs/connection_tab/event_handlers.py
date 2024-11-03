from PyQt5.QtCore import Qt


def handle_key_press(self, event):
    if event.key() == Qt.Key_Return:
        self.send_command()
    elif event.key() == Qt.Key_Up:
        self.show_previous_command()
    elif event.key() == Qt.Key_Down:
        self.show_next_command()
    else:
        super().keyPressEvent(event)


def handle_mouse_press(self, event):
    if event.button() == Qt.RightButton:
        self.show_context_menu(event.pos())
    else:
        super().mousePressEvent(event)


def show_context_menu(self, pos):
    context_menu = self.create_context_menu()
    context_menu.exec_(self.mapToGlobal(pos))


def on_terminal_change(self):
    cursor = self.terminal.textCursor()
    if cursor.position() < self.command_start_position:
        cursor.setPosition(self.terminal.document().characterCount())
        self.terminal.setTextCursor(cursor)

    current_command = self.terminal.toPlainText()[self.command_start_position :]
    if self.chief_enabled:
        self.chief.analyze_command(current_command)

    self.update_syntax_highlighting()
