import time
from threading import Thread

import meshtastic
import meshtastic.serial_interface
from meshtastic import portnums_pb2
from pubsub import pub
from PyQt5 import QtCore, QtWidgets

from utils.logger import logger


class MeshtasticChatTab(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.init_ui()
        if hasattr(parent, "meshtastic_chat_management"):
            parent.meshtastic_chat_management.nodes_updated.connect(self.update_radios)

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        # Channel selection
        channel_layout = QtWidgets.QHBoxLayout()
        self.channel_combo = QtWidgets.QComboBox()
        self.channel_combo.addItem("All")
        channel_layout.addWidget(QtWidgets.QLabel("Channel:"))
        channel_layout.addWidget(self.channel_combo)
        self.add_channel_button = QtWidgets.QPushButton("Add Channel")
        self.add_channel_button.clicked.connect(self.add_channel)
        channel_layout.addWidget(self.add_channel_button)
        layout.addLayout(channel_layout)

        # Radio selection for direct messages
        radio_layout = QtWidgets.QHBoxLayout()
        self.radio_combo = QtWidgets.QComboBox()
        self.radio_combo.addItem("All")
        radio_layout.addWidget(QtWidgets.QLabel("Send to:"))
        radio_layout.addWidget(self.radio_combo)
        layout.addLayout(radio_layout)

        # Chat display
        self.chat_display = QtWidgets.QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Message input
        input_layout = QtWidgets.QHBoxLayout()
        self.input_field = QtWidgets.QLineEdit()
        self.send_button = QtWidgets.QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

    def add_channel(self):
        channel_name, ok = QtWidgets.QInputDialog.getText(
            self, "Add Channel", "Enter channel name:"
        )
        if ok and channel_name:
            self.channel_combo.addItem(channel_name)

    def send_message(self):
        message = self.input_field.text()
        if message:
            channel = self.channel_combo.currentText()
            recipient = self.radio_combo.currentText()
            recipients = [recipient] if recipient != "All" else ["All"]
            self.chat_display.append(f"You to {recipient} ({channel}): {message}")
            self.input_field.clear()
            # Here you would typically send the message to the Meshtastic network
            if hasattr(self.parent(), "meshtastic_chat_management"):
                self.parent().meshtastic_chat_management.send_message(
                    message, channel, recipients
                )

    def receive_message(self, sender, channel, message):
        self.chat_display.append(f"{sender} ({channel}): {message}")

    def update_channels(self, channels):
        self.channel_combo.clear()
        self.channel_combo.addItem("All")
        for channel in channels:
            self.channel_combo.addItem(channel)

    def update_radios(self, radios):
        self.radio_combo.clear()
        self.radio_combo.addItem("All")
        for radio in radios:
            self.radio_combo.addItem(radio)


class MeshtasticChatManagement(QtCore.QObject):
    message_received = QtCore.pyqtSignal(str, str, str)
    nodes_updated = QtCore.pyqtSignal(list)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.chat_tab = None
        self.radio_status = "Disconnected"
        self.interface = None
        self.message_received.connect(self.on_message_received)
        self.nodes_updated.connect(self.update_radios)

    def toggle_meshtastic_chat(self, checked):
        if checked:
            self.open_meshtastic_chat()
        else:
            self.close_meshtastic_chat()

    def open_meshtastic_chat(self):
        if not self.chat_tab:
            self.chat_tab = MeshtasticChatTab(self.main_window)
            self.main_window.tab_widget.addTab(self.chat_tab, "Meshtastic Chat")
        self.main_window.tab_widget.setCurrentWidget(self.chat_tab)
        self.connect_to_meshtastic()

    def close_meshtastic_chat(self):
        if self.chat_tab:
            index = self.main_window.tab_widget.indexOf(self.chat_tab)
            if index != -1:
                self.main_window.tab_widget.removeTab(index)
            self.chat_tab = None
        self.disconnect_from_meshtastic()

    def connect_to_meshtastic(self):
        try:
            self.interface = meshtastic.serial_interface.SerialInterface()
            logger.info("Connected to Meshtastic device via serial")
            self.update_radio_status("Connected")
            self.start_message_listener()
            self.start_node_polling()
        except Exception as e:
            logger.error(f"Failed to connect to Meshtastic device: {str(e)}")
            self.update_radio_status("Connection Failed")

    def start_node_polling(self):
        def poll_nodes():
            while self.interface:
                try:
                    if hasattr(self.interface, "nodes"):
                        nodes = self.interface.nodes
                        node_names = ["All"] + [
                            nodes[node_id].get("user", {}).get("longName")
                            or nodes[node_id].get("user", {}).get("shortName")
                            or node_id
                            for node_id in nodes
                        ]
                        self.nodes_updated.emit(node_names)
                    else:
                        logger.warning(
                            "Meshtastic interface does not have 'nodes' attribute"
                        )
                except Exception as e:
                    logger.error(f"Error polling nodes: {str(e)}")
                time.sleep(30)  # Poll every 30 seconds

        thread = Thread(target=poll_nodes)
        thread.daemon = True
        thread.start()

    def disconnect_from_meshtastic(self):
        if self.interface:
            try:
                self.interface.close()
            except AttributeError:
                logger.warning(
                    "Meshtastic interface was already closed or not fully initialized."
                )
            except Exception as e:
                logger.error(f"Error closing Meshtastic interface: {str(e)}")
            finally:
                self.interface = None
        self.update_radio_status("Disconnected")

    def update_radio_status(self, status):
        self.radio_status = status
        logger.info(f"Meshtastic radio status: {status}")
        # Update UI to reflect the new status

    def on_message_received(self, sender, channel, message):
        if self.chat_tab:
            self.chat_tab.receive_message(sender, channel, message)
        else:
            logger.warning(f"Received message from {sender} but chat tab is not open")

    def send_message(self, message, channel, recipients):
        if not self.interface:
            logger.error("Not connected to Meshtastic network")
            return

        try:
            dest_id = None if recipients == ["All"] else recipients[0]
            self.interface.sendText(
                message,
                destinationId=dest_id,
                channelIndex=None if channel == "All" else int(channel),
                wantAck=True,
            )
            logger.info(
                f"Sent message to {recipients[0]} on channel {channel}: {message}"
            )
            if self.chat_tab:
                self.chat_tab.receive_message("You", channel, message)
        except Exception as e:
            logger.error(f"Failed to send message: {str(e)}")

    def update_channels(self):
        if self.interface:
            try:
                channels = self.interface.getChannels()
                channel_names = ["All"] + [
                    ch.settings.name for ch in channels.values() if ch.settings.name
                ]
                if self.chat_tab:
                    self.chat_tab.update_channels(channel_names)
            except AttributeError:
                logger.warning(
                    "Meshtastic interface does not have 'getChannels' method"
                )
            except Exception as e:
                logger.error(f"Error updating channels: {str(e)}")

    def update_radios(self):
        if self.interface:
            nodes = self.interface.nodes
            radio_names = ["All"] + [
                nodes[node_id].get("user", {}).get("longName")
                or nodes[node_id].get("user", {}).get("shortName")
                or node_id
                for node_id in nodes
            ]
            if self.chat_tab:
                self.chat_tab.update_radios(radio_names)

    def start_message_listener(self):
        def onReceive(packet, interface):
            sender = packet["fromId"]
            try:
                message = packet["decoded"]["text"]
                channel = packet.get("channelIndex", "Unknown")
                self.message_received.emit(sender, str(channel), message)
            except KeyError:
                pass  # Not a text message

        pub.subscribe(onReceive, "meshtastic.receive.text")

    def run_interface(self):
        while self.interface:
            time.sleep(1)  # Adjust as needed

    def start_interface_thread(self):
        thread = Thread(target=self.run_interface)
        thread.daemon = True
        thread.start()
