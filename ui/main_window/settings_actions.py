import json
from typing import Any, Dict

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                             QFileDialog, QFormLayout, QInputDialog, QLineEdit,
                             QMessageBox, QPushButton, QTabWidget, QVBoxLayout,
                             QWidget)

from ui.dialogs.chief_settings_dialog import ChiefSettingsDialog
from utils.logger import logger


class SessionOptionsDialog(QDialog):
    def __init__(self, parent=None, session_data=None):
        super().__init__(parent)
        self.session_data = session_data or {}
        self.setWindowTitle("Session Options")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Create tab widget
        tab_widget = QTabWidget()

        # General tab
        general_tab = QWidget()
        general_layout = QFormLayout(general_tab)
        self.session_name = QLineEdit(self.session_data.get("name", ""))
        general_layout.addRow("Session Name:", self.session_name)
        tab_widget.addTab(general_tab, "General")

        # Display tab
        display_tab = QWidget()
        display_layout = QFormLayout(display_tab)
        self.keyword_highlighting = QCheckBox()
        self.keyword_highlighting.setChecked(
            self.session_data.get("keyword_highlighting", True)
        )
        display_layout.addRow("Keyword Highlighting:", self.keyword_highlighting)
        tab_widget.addTab(display_tab, "Display")

        # AI tab
        ai_tab = QWidget()
        ai_layout = QFormLayout(ai_tab)
        self.chief_enabled = QCheckBox()
        self.chief_enabled.setChecked(self.session_data.get("chief_enabled", True))
        ai_layout.addRow("Enable Chief AI:", self.chief_enabled)
        tab_widget.addTab(ai_tab, "AI")

        # Meshtastic tab
        meshtastic_tab = QWidget()
        meshtastic_layout = QFormLayout(meshtastic_tab)
        self.meshtastic_enabled = QCheckBox()
        self.meshtastic_enabled.setChecked(
            self.session_data.get("meshtastic_enabled", False)
        )
        meshtastic_layout.addRow("Enable Meshtastic:", self.meshtastic_enabled)
        tab_widget.addTab(meshtastic_tab, "Meshtastic")

        layout.addWidget(tab_widget)

        # Dialog buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_settings(self):
        return {
            "name": self.session_name.text(),
            "keyword_highlighting": self.keyword_highlighting.isChecked(),
            "chief_enabled": self.chief_enabled.isChecked(),
            "meshtastic_enabled": self.meshtastic_enabled.isChecked(),
        }


class SettingsActions:
    def __init__(self, main_window):
        self.main_window = main_window
        self.settings_file = "config/settings.json"
        self.load_settings()

    def load_settings(self):
        """Load settings from the settings file."""
        try:
            with open(self.settings_file, "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            logger.warning("Settings file not found. Using default settings.")
            self.settings = {}
        except json.JSONDecodeError:
            logger.error("Error decoding settings file. Using default settings.")
            self.settings = {}

    def save_settings(self):
        """Save current settings to the settings file."""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully.")
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            QMessageBox.critical(
                self.main_window, "Error", f"Failed to save settings: {str(e)}"
            )

    def open_settings_dialog(self):
        """Open the main settings dialog."""
        logger.info("Opening settings dialog")
        # Implement a comprehensive settings dialog here
        QMessageBox.information(
            self.main_window, "Settings", "Settings dialog not yet implemented."
        )

    def change_theme(self):
        """Change the application theme."""
        themes = ["Light", "Dark", "System"]
        theme, ok = QInputDialog.getItem(
            self.main_window, "Change Theme", "Select a theme:", themes, 0, False
        )
        if ok and theme:
            self.settings["theme"] = theme
            self.save_settings()
            # Implement theme change logic here
            logger.info(f"Theme changed to {theme}")
            QMessageBox.information(
                self.main_window,
                "Theme Changed",
                f"Theme set to {theme}. Restart may be required.",
            )

    def configure_ai(self):
        """Configure AI settings."""
        logger.info("Opening AI configuration dialog")
        # Implement AI configuration dialog here
        QMessageBox.information(
            self.main_window,
            "AI Configuration",
            "AI configuration dialog not yet implemented.",
        )

    def configure_plugins(self):
        """Configure plugin settings."""
        logger.info("Opening plugin configuration dialog")
        # Implement plugin configuration dialog here
        QMessageBox.information(
            self.main_window,
            "Plugin Configuration",
            "Plugin configuration dialog not yet implemented.",
        )

    def export_settings(self):
        """Export current settings to a file."""
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window, "Export Settings", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(self.settings, f, indent=4)
                logger.info(f"Settings exported to {file_path}")
                QMessageBox.information(
                    self.main_window,
                    "Settings Exported",
                    f"Settings exported to {file_path}",
                )
            except Exception as e:
                logger.error(f"Error exporting settings: {str(e)}")
                QMessageBox.critical(
                    self.main_window, "Error", f"Failed to export settings: {str(e)}"
                )

    def import_settings(self):
        """Import settings from a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.main_window, "Import Settings", "", "JSON Files (*.json)"
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    imported_settings = json.load(f)
                self.settings.update(imported_settings)
                self.save_settings()
                logger.info(f"Settings imported from {file_path}")
                QMessageBox.information(
                    self.main_window,
                    "Settings Imported",
                    f"Settings imported from {file_path}",
                )
            except Exception as e:
                logger.error(f"Error importing settings: {str(e)}")
                QMessageBox.critical(
                    self.main_window, "Error", f"Failed to import settings: {str(e)}"
                )

    def reset_settings(self):
        """Reset all settings to default values."""
        confirm = QMessageBox.question(
            self.main_window,
            "Reset Settings",
            "Are you sure you want to reset all settings to default values?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            self.settings = {}  # Reset to empty dictionary (default settings)
            self.save_settings()
            logger.info("Settings reset to default values")
            QMessageBox.information(
                self.main_window,
                "Settings Reset",
                "All settings have been reset to default values.",
            )

    def session_options(self):
        logger.info("Opening session options")
        current_session = self.main_window.session_management.get_current_session()
        dialog = SessionOptionsDialog(self.main_window, current_session)
        if dialog.exec_():
            new_settings = dialog.get_settings()
            self.apply_session_settings(new_settings)

    def apply_session_settings(self, settings: Dict[str, Any]):
        logger.info(f"Applying session settings: {settings}")
        current_session = self.main_window.session_management.get_current_session()
        if current_session:
            current_session.update(settings)
            self.main_window.session_management.update_session(current_session)
            # Apply the settings to the current session
            self.apply_keyword_highlighting(settings["keyword_highlighting"])
            self.toggle_chief_ai(settings["chief_enabled"])
            self.toggle_meshtastic(settings["meshtastic_enabled"])

    def apply_keyword_highlighting(self, enabled: bool):
        # Implement keyword highlighting toggle
        pass

    def toggle_chief_ai(self, enabled: bool):
        # Implement Chief AI toggle
        pass

    def toggle_meshtastic(self, enabled: bool):
        if hasattr(self.main_window, "meshtastic_chat_management"):
            self.main_window.meshtastic_chat_management.toggle_meshtastic_chat(enabled)
        else:
            logger.warning("Meshtastic chat management not initialized")

    def keyword_highlighting(self):
        logger.info("Opening keyword highlighting settings")
        # Implement keyword highlighting settings dialog

    def chief_settings(self):
        logger.info("Opening Chief AI settings")
        current_settings = self.main_window.chief.settings
        dialog = ChiefSettingsDialog(self.main_window, current_settings)
        if dialog.exec_():
            new_settings = dialog.get_settings()
            self.apply_chief_settings(new_settings)

    def apply_chief_settings(self, settings: Dict[str, Any]):
        logger.info(f"Applying Chief AI settings: {settings}")
        self.main_window.chief.settings = settings
        self.main_window.chief.setup_ai_model()

    # Add other settings-related methods as needed
