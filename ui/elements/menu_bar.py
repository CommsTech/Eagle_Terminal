import logging
from typing import Any, List, Optional

from PyQt5.QtWidgets import QAction, QMenu, QMenuBar

logger = logging.getLogger(__name__)


def create_menu_bar(parent: Any) -> QMenuBar:
    """Create and return a menu bar for the main window.

    Args:
        parent: The parent widget (usually the main window).

    Returns:
        QMenuBar: The created menu bar with all menus and actions.
    """
    menu_bar = QMenuBar(parent)

    # File Menu
    file_menu = menu_bar.addMenu("&File")
    add_actions(
        file_menu,
        parent.file_actions,
        [
            "quick_connect",
            "new_session",
            "connect_in_tab",
            "connect_in_shell",
            "reconnect_current_session",
            "reconnect_all_sessions",
            "disconnect_current_session",
            "disconnect_all_sessions",
            None,  # Separator
            "print_current_session",
            "print_setup",
            None,  # Separator
            "exit",
        ],
    )

    # Edit Menu
    edit_menu = menu_bar.addMenu("&Edit")
    add_actions(
        edit_menu,
        parent.edit_actions,
        [
            "copy",
            "paste",
            "copy_and_paste",
            "select_all",
            "find",
            "go_to_session",
            None,  # Separator
            "clear_scrollback",
            "clear_screen",
            "send_break",
            "reset",
        ],
    )

    # Options Menu
    options_menu = menu_bar.addMenu("&Options")
    add_actions(
        options_menu,
        parent.options_actions,
        [
            "session_options",
            "edit_default_session",
            "global_options",
            "keyword_highlighting",
            "auto_save_options",
            "save_settings_now",
            "chief_settings",
        ],
    )

    # Transfer Menu
    transfer_menu = menu_bar.addMenu("&Transfer")
    add_actions(
        transfer_menu,
        parent.transfer_actions,
        [
            "send_ascii",
            "receive_ascii",
            "send_binary",
            "send_kermit",
            "receive_kermit",
            "send_xmodem",
            "receive_xmodem",
            "send_ymodem",
            "receive_ymodem",
            "zmodem_upload_list",
            "start_zmodem_upload",
            "start_tftp_server",
        ],
    )

    # Script Menu
    script_menu = menu_bar.addMenu("&Script")
    add_actions(
        script_menu,
        parent.script_actions,
        [
            "run",
            "cancel",
            "start_recording",
            "stop_recording",
            "cancel_recording",
            "show_recent_scripts",
            "configure_scripts",
        ],
    )

    # Tools Menu
    tools_menu = menu_bar.addMenu("&Tools")
    add_actions(
        tools_menu,
        parent.tools_actions,
        [
            "keymap_editor",
            "create_public_key",
            "convert_private_key",
            "export_public_key",
            "public_key_assistant",
            "manage_agent_keys",
            "change_config_properties",
            "export_settings",
            "import_settings",
        ],
    )

    # Window Menu
    window_menu = menu_bar.addMenu("&Window")
    parent.window_actions.setup_menu(window_menu)

    # Help Menu
    help_menu = menu_bar.addMenu("&Help")
    add_actions(
        help_menu,
        parent.help_actions,
        [
            "help_topics",
            "eagle_term_web_page",
            "donate",
            "update_now",
            "check_for_updates",
            "contact_support",
            "about",
        ],
    )

    return menu_bar


def add_actions(
    menu: QMenu, action_class: Any, action_names: List[Optional[str]]
) -> None:
    """Add actions to a menu.

    Args:
        menu: The menu to add actions to.
        action_class: The class containing the action methods.
        action_names: A list of action names to add. None represents a separator.
    """
    for action_name in action_names:
        if action_name is None:
            menu.addSeparator()
        else:
            action = QAction(action_name.replace("_", " ").title(), menu)
            if hasattr(action_class, action_name):
                action.triggered.connect(getattr(action_class, action_name))
            else:
                logger.warning(
                    f"{action_class.__class__.__name__} has no attribute '{action_name}'"
                )
            menu.addAction(action)
