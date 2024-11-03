from ui.dialogs.network_discovery_dialog import NetworkDiscoveryDialog


class NetworkDiscoveryManagement:
    def __init__(self, main_window):
        self.main_window = main_window

    def run_network_discovery(self):
        dialog = NetworkDiscoveryDialog(self.main_window)
        dialog.exec_()
