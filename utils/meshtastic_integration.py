import meshtastic
from meshtastic import tcp_interface

from utils.logger import logger


class MeshtasticIntegration:
    def __init__(self):
        """Initialize the class instance.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            interface (None): An attribute to store the interface, initially set to None.
        """
        self.interface = None

    def connect(self, host, port):
        """Establishes a connection to a Meshtastic device using TCP.
        
        Args:
            host (str): The hostname or IP address of the Meshtastic device.
            port (int): The port number to connect to on the Meshtastic device.
        
        Returns:
            None
        
        Raises:
            Exception: If the connection to the Meshtastic device fails.
        """
        try:
            self.interface = tcp_interface.TCPInterface(host, port)
            logger.info(f"Connected to Meshtastic device at {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to connect to Meshtastic device: {str(e)}")

    def get_nodes(self):
        """Get the nodes from the Meshtastic interface.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: A dictionary of nodes if available, or an empty dictionary if not.
        
        Raises:
            AttributeError: Implicitly if 'nodes' attribute is not found (caught and logged).
        """
        if self.interface and hasattr(self.interface, "nodes"):
            return self.interface.nodes
        else:
            logger.warning("Meshtastic interface does not have 'nodes' attribute")
            return {}

    # Add other Meshtastic-related methods as needed
