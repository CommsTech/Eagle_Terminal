"""This module manages sessions for the Eagle Terminal application.

It handles session timeouts and provides functionality to start, stop,
and reset sessions.
"""

from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class SessionManager(QObject):
    """Manages user sessions, including timeout functionality."""

    session_timeout = pyqtSignal()

    def __init__(self, timeout_duration=300000):  # 5 minutes default
        """Initialize the SessionManager.

        Args:
            timeout_duration (int): Duration in milliseconds before a session times out.
        """
        super().__init__()
        self.timeout_duration = timeout_duration
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)
        self.active = False

    def start_session(self):
        """Start a new session and begin the timeout timer."""
        self.active = True
        self.timer.start(self.timeout_duration)

    def stop_session(self):
        """Stop the current session and the timeout timer."""
        self.active = False
        self.timer.stop()

    def reset(self):
        """Reset the timeout timer."""
        if self.active:
            self.timer.stop()
            self.timer.start(self.timeout_duration)

    def handle_timeout(self):
        """Handle session timeout by emitting the session_timeout signal."""
        self.active = False
        self.session_timeout.emit()

    def is_active(self):
        """Check if a session is currently active."""
        return self.active

    def set_timeout_duration(self, duration):
        """Set a new timeout duration.

        Args:
            duration (int): New timeout duration in milliseconds.
        """
        self.timeout_duration = duration
        if self.active:
            self.reset()

    def get_remaining_time(self):
        """Get the remaining time before session timeout."""
        return self.timer.remainingTime() if self.active else 0
