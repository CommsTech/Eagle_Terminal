"""Security Manager module for Eagle Terminal's AI system.

This module provides functionality to handle security-related tasks such
as input sanitization, validation, anomaly detection, and data
protection.
"""

import hashlib
import re
import secrets
from typing import List


class SecurityManager:
    """A class for managing security-related operations in Eagle Terminal.

    This class provides methods for input sanitization, validation,
    anomaly detection, and various cryptographic operations to enhance
    the security of the system.
    """

    def __init__(self):
        """Initialize the SecurityManager with predefined sensitive
        patterns."""
        self.sensitive_patterns = [
            r"\b(?:password|pwd|pass)\s*[:=]\s*\S+",
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        ]

    def sanitize_input(self, text: str) -> str:
        """Sanitize the input text by redacting sensitive information.

        Args:
            text (str): The input text to sanitize.

        Returns:
            str: The sanitized text with sensitive information redacted.
        """
        for pattern in self.sensitive_patterns:
            text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
        return text

    def validate_input(self, text: str) -> bool:
        """Validate the input text for potential security risks.

        Args:
            text (str): The input text to validate.

        Returns:
            bool: True if the input is valid, False otherwise.
        """
        max_length = 1000  # Adjust as needed
        return len(text) <= max_length and not re.search(r"[<>]", text)

    def detect_anomalies(self, command_history: List[str]) -> List[str]:
        """Detect anomalies in the command history.

        Args:
            command_history (List[str]): A list of previously executed commands.

        Returns:
            List[str]: A list of detected anomalies.
        """
        anomalies = []
        if len(command_history) > 1:
            for i in range(1, len(command_history)):
                if command_history[i] == command_history[i - 1]:
                    anomalies.append(f"Repeated command: {command_history[i]}")

                # Check for potentially dangerous commands
                dangerous_commands = ["rm -rf", "format", "mkfs"]
                for cmd in dangerous_commands:
                    if cmd in command_history[i].lower():
                        anomalies.append(
                            f"Potentially dangerous command detected: {command_history[i]}"
                        )

        return anomalies

    def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data using SHA-256.

        Args:
            data (str): The sensitive data to hash.

        Returns:
            str: The hashed data.
        """
        return hashlib.sha256(data.encode()).hexdigest()

    def generate_secure_token(self) -> str:
        """Generate a secure token for authentication or other purposes.

        Returns:
            str: A secure, URL-safe token.
        """
        return secrets.token_urlsafe(32)

    def verify_integrity(self, data: str, signature: str) -> bool:
        """Verify the integrity of data using a signature.

        Args:
            data (str): The data to verify.
            signature (str): The signature to check against.

        Returns:
            bool: True if the data integrity is verified, False otherwise.
        """
        return hashlib.sha256(data.encode()).hexdigest() == signature
