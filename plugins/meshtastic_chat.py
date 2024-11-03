import time

import serial.tools.list_ports
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from utils.logger import logger

try:
    import meshtastic
    import meshtastic.serial_interface

    MESHTASTIC_AVAILABLE = True
except ImportError:
    MESHTASTIC_AVAILABLE = False
    logger.warning(
        "Meshtastic library not found. Meshtastic Chat feature will not be available."
    )


class MeshtasticChatThread(QThread):
    message_received = pyqtSignal(str, str, str)  # sender, channel, message
    nodes_updated = pyqtSignal(list)  # list of node IDs

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.interface = None
        self.running = False

    def run(self):
        if not MESHTASTIC_AVAILABLE:
            logger.error("Meshtastic library not available. Cannot start chat thread.")
            return

        try:
            self.interface = meshtastic.serial_interface.SerialInterface(self.port)
            self.running = True

            def on_receive(packet, interface):
                sender = packet.get("fromId", "Unknown")
                channel = packet.get("channel", 0)
                message = packet.get("decoded", {}).get("text", "")
                self.message_received.emit(sender, str(channel), message)

            self.interface.onReceive = on_receive

            while self.running:
                time.sleep(0.1)  # Small delay to prevent high CPU usage
                self.update_nodes()

        except Exception as e:
            logger.error(f"Meshtastic error: {str(e)}")

    def stop(self):
        self.running = False
        if self.interface:
            self.interface.close()

    def send_message(self, message, destination=None, channel=0):
        if self.interface:
            self.interface.sendText(
                message, destinationId=destination, channelIndex=channel
            )

    def get_channels(self):
        if self.interface:
            return (
                self.interface.getChannels()
            )  # Changed from getChannelSet to getChannels
        return {}

    def update_nodes(self):
        if self.interface:
            nodes = self.interface.nodes  # Changed from getNodes() to nodes attribute
            self.nodes_updated.emit(list(nodes.keys()))


class MeshtasticChat(QObject):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.chat_thread = None
        self.current_channel = 0
        self.connected_nodes = []

    def setup(self, plugin_manager):
        if not MESHTASTIC_AVAILABLE:
            logger.warning(
                "Meshtastic library not found. Meshtastic Chat feature will not be available."
            )
            QMessageBox.warning(
                self.main_window,
                "Meshtastic Not Available",
                "The Meshtastic library is not installed. Meshtastic Chat feature will not be available. "
                "Please install the Meshtastic library to use this feature.",
            )
            return

        logger.info("Setting up Meshtastic Chat plugin")
        plugin_manager.register_hook("on_connect", self.on_connect)
        plugin_manager.register_hook("on_disconnect", self.on_disconnect)

    def on_connect(self):
        if not MESHTASTIC_AVAILABLE:
            logger.error("Meshtastic library not available. Cannot connect.")
            return

        port = self.find_meshtastic_port()
        if port:
            self.chat_thread = MeshtasticChatThread(port)
            self.chat_thread.message_received.connect(self.handle_message)
            self.chat_thread.nodes_updated.connect(self.update_connected_nodes)
            self.chat_thread.start()
            self.update_channels()
        else:
            logger.error("No Meshtastic device found")
            self.main_window.error_handler.show_error(
                self.main_window, "Meshtastic Error", "No Meshtastic device found"
            )

    def find_meshtastic_port(self):
        ports = list(serial.tools.list_ports.comports())
        for port in ports:
            try:
                interface = meshtastic.serial_interface.SerialInterface(port.device)
                interface.close()
                logger.info(f"Meshtastic device found on port {port.device}")
                return port.device
            except Exception as e:
                logger.debug(f"Not a Meshtastic device on port {port.device}: {str(e)}")
        return None

    def handle_message(self, sender, channel, message):
        formatted_message = f"[Channel {channel}] {sender}: {message}"
        self.main_window.update_meshtastic_chat(formatted_message)

    def send_message(self, message, destination=None, channel=None):
        if self.chat_thread:
            channel = channel if channel is not None else self.current_channel
            self.chat_thread.send_message(
                message, destination=destination, channel=channel
            )
            self.main_window.update_meshtastic_chat(f"You: {message}")

    def get_channels(self):
        if self.chat_thread:
            return self.chat_thread.get_channels()
        return {}

    def update_channels(self):
        channels = self.get_channels()
        self.main_window.meshtastic_chat_management.update_channels(channels)

    def set_current_channel(self, channel):
        self.current_channel = channel

    def update_connected_nodes(self, nodes):
        self.connected_nodes = nodes
        self.main_window.meshtastic_chat_management.update_connected_nodes(nodes)


def setup(main_window):
    meshtastic_chat = MeshtasticChat(main_window)
    meshtastic_chat.setup(main_window.plugin_manager)
    main_window.meshtastic_chat = meshtastic_chat
