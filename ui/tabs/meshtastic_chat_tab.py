import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QListWidget, QMessageBox, QPushButton, QTextEdit,
                             QVBoxLayout, QWidget)


class MeshtasticChatTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)

        chat_layout = QVBoxLayout()

        # Channel selection
        channel_layout = QHBoxLayout()
        channel_layout.addWidget(QLabel("Channel:"))
        self.channel_combo = QComboBox()
        self.channel_combo.currentIndexChanged.connect(self.on_channel_changed)
        channel_layout.addWidget(self.channel_combo)
        chat_layout.addLayout(channel_layout)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(self.chat_display)

        # Message input
        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        chat_layout.addLayout(input_layout)

        layout.addLayout(chat_layout, 2)

        # Connected nodes list
        nodes_layout = QVBoxLayout()
        nodes_layout.addWidget(QLabel("Connected Nodes:"))
        self.nodes_list = QListWidget()
        self.nodes_list.itemClicked.connect(self.on_node_selected)
        nodes_layout.addWidget(self.nodes_list)

        layout.addLayout(nodes_layout, 1)

        # Radio status indicator
        self.radio_status_label = QLabel("Radio Status: Disconnected")
        chat_layout.addWidget(self.radio_status_label)

    @pyqtSlot()
    def send_message(self):
        message = self.message_input.text()
        if message and hasattr(self.parent, "meshtastic_chat"):
            try:
                channel = self.channel_combo.currentText()
                destination = (
                    self.nodes_list.currentItem().text()
                    if self.nodes_list.currentItem()
                    else None
                )
                self.parent.meshtastic_chat.send_message(
                    message, destination=destination, channel=channel
                )
                self.message_input.clear()
            except Exception as e:
                logging.error(f"Error sending message: {str(e)}")
                # Optionally, show an error message to the user
                QMessageBox.warning(self, "Error", f"Failed to send message: {str(e)}")

    def update_chat(self, message):
        self.chat_display.append(message)

    def update_channels(self, channels):
        self.channel_combo.clear()
        for channel_name in channels.keys():
            self.channel_combo.addItem(channel_name)

    @pyqtSlot(int)
    def on_channel_changed(self, index):
        if hasattr(self.parent, "meshtastic_chat"):
            channel_name = self.channel_combo.itemText(index)
            self.parent.meshtastic_chat.set_current_channel(channel_name)

    def update_connected_nodes(self, nodes):
        self.nodes_list.clear()
        for node in nodes:
            self.nodes_list.addItem(node)

    @pyqtSlot()
    def on_node_selected(self):
        # You can add functionality here when a node is selected, if needed
        pass

    def update_radio_status(self, status):
        self.radio_status_label.setText(f"Radio Status: {status}")
