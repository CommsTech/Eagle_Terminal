import meshtastic
from meshtastic import tcp_interface

from utils.logger import logger


class MeshtasticIntegration:
    def __init__(self):
        self.interface = None

    def connect(self, host, port):
        try:
            self.interface = tcp_interface.TCPInterface(host, port)
            logger.info(f"Connected to Meshtastic device at {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to connect to Meshtastic device: {str(e)}")

    def get_nodes(self):
        if self.interface and hasattr(self.interface, "nodes"):
            return self.interface.nodes
        else:
            logger.warning("Meshtastic interface does not have 'nodes' attribute")
            return {}

    # Add other Meshtastic-related methods as needed
