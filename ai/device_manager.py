"""Device Manager module for Eagle Terminal's AI system.

This module provides functionality to manage devices and suggest actions
based on device information using AI-powered analysis.
"""

from typing import Any, Callable, Dict


class DeviceManager:
    """A class for managing devices and suggesting actions based on device
    information.

    This class provides methods to add, remove, and retrieve device
    information, as well as suggest next actions using AI-powered
    analysis.
    """

    def __init__(self):
        self.devices: Dict[str, Dict[str, Any]] = {}

    def add_device(self, device_id: str, device_info: Dict[str, Any]):
        """Add a new device to the manager.

        Args:
            device_id (str): Unique identifier for the device.
            device_info (Dict[str, Any]): Information about the device.
        """
        self.devices[device_id] = device_info

    def remove_device(self, device_id: str):
        """Remove a device from the manager.

        Args:
            device_id (str): Unique identifier of the device to remove.
        """
        self.devices.pop(device_id, None)

    def get_device(self, device_id: str) -> Dict[str, Any]:
        """Retrieve device information by its ID.

        Args:
            device_id (str): Unique identifier of the device.

        Returns:
            Dict[str, Any]: Information about the device, or an empty dict if not found.
        """
        return self.devices.get(device_id, {})

    def suggest_next_action(
        self, device: Dict[str, Any], quick_prompt: Callable[[str], str]
    ) -> str:
        """Suggest the next action for a device using AI-powered analysis.

        Args:
            device (Dict[str, Any]): Information about the device.
            quick_prompt (Callable[[str], str]): Function to generate AI responses.

        Returns:
            str: Suggested next action for the device.
        """
        device_info = (
            f"Device: {device.get('name', 'Unknown')}\n"
            f"Type: {device.get('type', 'Unknown')}\n"
            f"Status: {device.get('status', 'Unknown')}"
        )
        prompt = (
            f"Based on the following device information, suggest the next action:\n\n"
            f"{device_info}\n\nSuggested action:"
        )
        suggestion = quick_prompt(prompt)
        return (
            suggestion
            if isinstance(suggestion, str)
            else "No valid suggestion available."
        )
