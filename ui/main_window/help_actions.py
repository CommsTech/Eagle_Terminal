from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt5.QtCore import Qt, QUrl
    from PyQt5.QtGui import QDesktopServices
    from PyQt5.QtWidgets import (QAction, QDialog, QListWidget, QMessageBox,
                                 QPushButton, QTextBrowser, QTextEdit,
                                 QVBoxLayout)
else:
    from PyQt5.QtCore import Qt, QUrl
    from PyQt5.QtGui import QDesktopServices
    from PyQt5.QtWidgets import (
        QAction,
        QDialog,
        QListWidget,
        QMessageBox,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QTextBrowser,
    )

from utils.logger import logger

# Expanded Help Topics
HELP_TOPICS = {
    "Getting Started": """
Welcome to Eagle Terminal!

To get started:
1. Use the 'Quick Connect' button or 'File > New Connection' to create a new connection.
2. Enter the host details in the connection dialog.
3. Click 'Connect' to establish a new session.
4. Use the terminal interface to interact with the remote system.

For more information on specific features, explore the other help topics.
""",
    "SSH Connections": """
SSH Connections in Eagle Terminal:

1. Click 'New Connection' or use 'Quick Connect'.
2. Select 'SSH' as the connection type.
3. Enter the hostname, port (default is 22), username, and password or key file.
4. Click 'Connect' to establish the SSH session.
5. You can save frequently used connections for quick access.

Tips:
- Use key-based authentication for enhanced security.
- Enable compression for slower connections.
- Utilize the 'Reconnect' feature for dropped connections.
""",
    "Device Management": """
Managing Devices in Eagle Terminal:

1. Add new devices using the 'Add Device' button or through successful connections.
2. View all devices in the device list on the left side of the main window.
3. Right-click on a device to edit its details, delete it, or initiate a connection.
4. Use the search function to quickly find devices in large lists.
5. Group devices for easier management of multiple systems.

Best Practices:
- Use meaningful names for your devices.
- Regularly update device information to ensure successful connections.
- Utilize device groups for organizing related systems.
""",
    "AI Assistant (Chief)": """
Using the AI Assistant (Chief) in Eagle Terminal:

1. Chief analyzes your commands and their outputs automatically.
2. View Chief's insights in the dedicated panel below the terminal.
3. Ask Chief for help by typing '!help' followed by your question.
4. Use '!suggest' to get command suggestions based on your current context.
5. Chief learns from your interactions to provide better assistance over time.

Tips:
- Be specific in your questions to get more accurate responses.
- Use Chief's suggestions as a starting point for complex tasks.
- Provide feedback to help improve Chief's performance.
""",
    "Network Discovery": """
Using Network Discovery in Eagle Terminal:

1. Go to 'Tools > Network Discovery' to open the network discovery tool.
2. Enter the IP range you want to scan.
3. Click 'Scan' to start the discovery process.
4. View discovered devices in the results list.
5. Right-click on discovered devices to add them to your device list or connect.

Best Practices:
- Ensure you have permission to scan the network.
- Use specific IP ranges for faster and more targeted scans.
- Regularly perform scans to keep your device list up-to-date.
""",
    "File Transfer": """
Transferring Files in Eagle Terminal:

1. Connect to a remote system using SSH.
2. Use the 'Transfer' menu to select your desired transfer method (SCP, SFTP, etc.).
3. For SCP: Use 'Transfer > Send File' or 'Transfer > Receive File'.
4. For SFTP: Open the SFTP browser using 'Transfer > SFTP Browser'.
5. Drag and drop files in the SFTP browser or use the upload/download buttons.

Tips:
- Use SFTP for interactive file management.
- SCP is faster for transferring large files.
- Always verify file permissions after transfer.
""",
    "Scripting and Automation": """
Scripting and Automation in Eagle Terminal:

1. Go to 'Script > New Script' to create a new script.
2. Write your script using Python or the Eagle Terminal scripting language.
3. Use 'Script > Run' to execute your script.
4. Schedule scripts using 'Tools > Task Scheduler'.
5. Use the Script Library to store and manage your scripts.

Best Practices:
- Comment your scripts for better maintainability.
- Use error handling in your scripts for robustness.
- Leverage Chief's AI capabilities in your scripts for smarter automation.
""",
    "Customization and Settings": """
Customizing Eagle Terminal:

1. Go to 'Options > Global Options' to access the main settings.
2. Customize the appearance in the 'Display' tab.
3. Configure default connection settings in the 'Connection' tab.
4. Set up keyboard shortcuts in the 'Keyboard' tab.
5. Adjust AI assistant settings in the 'AI' tab.

Tips:
- Create multiple profiles for different use cases.
- Export your settings to easily transfer them to another installation.
- Regularly review and update your settings for optimal performance.
""",
    "Troubleshooting": """
Troubleshooting in Eagle Terminal:

1. Check the application logs in 'Help > View Logs'.
2. Verify your connection settings if you're having trouble connecting.
3. Ensure your firewall isn't blocking Eagle Terminal.
4. For AI-related issues, try retraining or resetting Chief.
5. Visit our support forum or contact support for additional help.

Common Issues:
- Connection timeouts: Check network connectivity and firewall settings.
- Authentication failures: Verify username, password, and key files.
- Performance issues: Adjust connection parameters or optimize scripts.
""",
}


class HelpTopicsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help Topics")
        self.setGeometry(100, 100, 600, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)
        layout.addWidget(self.text_browser)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

        # Load help content
        help_content = "<h1>Eagle Terminal Help Topics</h1>"
        for topic, content in HELP_TOPICS.items():
            help_content += f"<h2>{topic}</h2>{content}<hr>"
        self.text_browser.setHtml(help_content)


class HelpActions:
    def __init__(self, main_window):
        self.main_window = main_window

    def show_help_topics(self):
        """Show the help topics dialog."""
        logger.info("Showing help topics")
        dialog = HelpTopicsDialog(self.main_window)
        dialog.exec_()

    def about(self):
        """Show the about dialog."""
        logger.info("Showing about dialog")
        QMessageBox.about(
            self.main_window,
            "About Eagle Terminal",
            "Eagle Terminal v1.0\n\nAn advanced, AI-assisted SSH/Serial client with Ansible support."
            "By Commstech",
        )

    def show_license(self):
        """Show the license information."""
        logger.info("Showing license information")
        # Implement license display logic here
        QMessageBox.information(
            self.main_window, "License", "License information not yet implemented."
        )

    def eagle_term_web_page(self):
        """Open the Eagle Terminal web page."""
        logger.info("Eagle Terminal web page action triggered")
        QDesktopServices.openUrl(QUrl("https://github.com/CommsTech/Eagle_Terminal"))

    def donate(self):
        """Open the donation page."""
        logger.info("Donate action triggered")
        QDesktopServices.openUrl(QUrl("https://liberapay.com/Commstech/donate"))

    def update_now(self):
        """Check for updates and update the application."""
        logger.info("Update now action triggered")
        # Implement update logic here
        QMessageBox.information(
            self.main_window, "Update", "Update functionality not yet implemented"
        )

    def check_for_updates(self):
        """Check for updates without updating."""
        logger.info("Check for updates action triggered")
        # Implement update checking logic here
        QMessageBox.information(
            self.main_window, "Check for Updates", "Update checking not yet implemented"
        )

    def contact_support(self):
        """Open the contact support dialog or page."""
        logger.info("Contact support action triggered")
        QDesktopServices.openUrl(QUrl("mailto:support@commsnet.org"))

    def show_third_party_licenses(self):
        """Show third-party licenses."""
        logger.info("Show third-party licenses action triggered")
        # Implement third-party licenses display logic here
        QMessageBox.information(
            self.main_window,
            "Third-Party Licenses",
            "Third-party licenses not yet implemented",
        )

    def setup_menu(self, menu):
        actions = [
            ("Help Topics", self.show_help_topics),
            ("Eagle Term Web Page", self.eagle_term_web_page),
            ("Donate Now", self.donate),
            ("Update Now", self.update_now),
            ("Check for Updates", self.check_for_updates),
            ("Contact Support", self.contact_support),
            ("About", self.about),
            ("License", self.show_license),
        ]

        for name, callback in actions:
            action = QAction(name, self.main_window)
            action.triggered.connect(callback)
            menu.addAction(action)

    def show_context_help(self, context):
        """Show context-sensitive help."""
        content = HELP_TOPICS.get(context, f"No help available for '{context}'")
        QMessageBox.information(self.main_window, f"Help: {context}", content)


def create_action(text, slot, parent, shortcut=None):
    action = QAction(text, parent)
    action.triggered.connect(slot)
    if shortcut:
        action.setShortcut(shortcut)
    return action
