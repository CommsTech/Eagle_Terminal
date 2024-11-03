from utils.logger import logger


class SessionActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def new_session(self):
        self.main_window.session_management.new_session()

    def quick_connect(self):
        self.main_window.session_management.new_session()

    def connect_in_tab(self):
        logger.info("Connecting in a new tab")
        self.main_window.session_management.new_session()

    def connect_in_shell(self):
        logger.info("Connecting in shell")
        # Implement shell connection logic here

    def disconnect_current_session(self):
        current_tab = self.main_window.tab_widget.currentWidget()
        if isinstance(current_tab, self.main_window.SSHTab):
            current_tab.disconnect()
        else:
            logger.warning("No active SSH session to disconnect")

    def reconnect_current_session(self):
        current_tab = self.main_window.tab_widget.currentWidget()
        if isinstance(current_tab, self.main_window.SSHTab):
            current_tab.reconnect()
        else:
            logger.warning("No active SSH session to reconnect")

    def reconnect_all_sessions(self):
        logger.info("Reconnecting all sessions")
        for session in self.main_window.open_sessions:
            self.main_window.session_management.reconnect_session(session)

    def disconnect_all_sessions(self):
        logger.info("Disconnecting all sessions")
        for session in self.main_window.open_sessions:
            self.main_window.session_management.close_session(session)

    # ... (other session-related methods)
