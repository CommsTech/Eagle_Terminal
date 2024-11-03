from PyQt5.QtWidgets import QInputDialog, QMessageBox

from ui.dialogs.network_discovery_dialog import NetworkDiscoveryDialog
from ui.tabs.network_discovery import NetworkDiscovery
from utils.logger import logger
from utils.network_discovery import parse_ip_range, scan_network


class NetworkDiscoveryManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.network_discovery_tab = None

    def discover_devices(self):
        dialog = NetworkDiscoveryDialog(self.main_window)
        if dialog.exec_():
            network_input = dialog.get_network_input()
            scan_type = dialog.get_scan_type()

            try:
                if scan_type == "IP":
                    ip_list = [network_input]
                elif scan_type == "Range":
                    start_ip, end_ip = network_input.split("-")
                    ip_list = parse_ip_range(start_ip.strip(), end_ip.strip())
                elif scan_type == "CIDR":
                    ip_list = parse_ip_range(network_input)
                else:
                    raise ValueError("Invalid scan type")

                devices = scan_network(ip_list)
                self.update_device_list(devices)
            except Exception as e:
                logger.error(f"Error during network discovery: {str(e)}")
                QMessageBox.warning(
                    self.main_window,
                    "Network Discovery Error",
                    f"An error occurred: {str(e)}",
                )

    def update_device_list(self, devices):
        for device in devices:
            self.main_window.device_management.add_device(device)
        self.main_window.update_status(f"{len(devices)} new devices discovered")

    def open_network_discovery_tab(self):
        if not self.network_discovery_tab:
            self.network_discovery_tab = NetworkDiscovery(self.main_window)
            self.main_window.tab_widget.addTab(
                self.network_discovery_tab, "Network Discovery"
            )
        self.main_window.tab_widget.setCurrentWidget(self.network_discovery_tab)

    def close_network_discovery_tab(self):
        if self.network_discovery_tab:
            index = self.main_window.tab_widget.indexOf(self.network_discovery_tab)
            if index != -1:
                self.main_window.tab_widget.removeTab(index)
            self.network_discovery_tab = None
