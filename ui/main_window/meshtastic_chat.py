from ui.tabs.meshtastic_chat_tab import MeshtasticChat


class MeshtasticChatManagement:
    def __init__(self, main_window):
        self.main_window = main_window
        self.meshtastic_chat = None

    def toggle_meshtastic_chat(self, state):
        if state:
            # Enable Meshtastic chat
            if self.meshtastic_chat is None:
                self.meshtastic_chat = MeshtasticChat(self.main_window)
                self.main_window.tab_widget.addTab(
                    self.meshtastic_chat, "Meshtastic Chat"
                )
            self.main_window.plugin_manager.trigger_hook("meshtastic_chat_connect")
        else:
            # Disable Meshtastic chat
            if self.meshtastic_chat is not None:
                index = self.main_window.tab_widget.indexOf(self.meshtastic_chat)
                if index != -1:
                    self.main_window.tab_widget.removeTab(index)
                self.meshtastic_chat = None
            self.main_window.plugin_manager.trigger_hook("meshtastic_chat_disconnect")
