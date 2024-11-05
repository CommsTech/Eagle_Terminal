import json
from datetime import datetime
from typing import Any, Dict, List


class DeviceManager:
    def __init__(self, file_path: str = "devices.json"):
        """Initialize a new instance of the class.
        
        Args:
            file_path (str, optional): The path to the JSON file containing device information. Defaults to "devices.json".
        
        Returns:
            None
        
        """
        self.file_path = file_path
        self.devices = self.load_devices()

    def load_devices(self) -> List[Dict[str, Any]]:
        """Loads devices from a JSON file.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a device with its properties.
                                  Returns an empty list if the file is not found.
        
        Raises:
            json.JSONDecodeError: If the file contains invalid JSON data.
        """
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_devices(self) -> None:
        """Save the devices to a JSON file.
        
        Args:
            self: The instance of the class containing the devices and file path.
        
        Returns:
            None: This method doesn't return anything.
        """
        with open(self.file_path, "w") as f:
            json.dump(self.devices, f, indent=2)

    def add_device(self, device_data):
        """Add a new device to the collection.
        
        Args:
            device_data (dict): A dictionary containing the data for the new device.
        
        Returns:
            None
        
        """
        self.devices.append(device_data)
        self.save_devices()

    def remove_device(self, name: str) -> None:
        """Remove a device from the list of devices.
        
        Args:
            name (str): The name of the device to be removed.
        
        Returns:
            None: This method doesn't return anything.
        """
        self.devices = [d for d in self.devices if d["name"] != name]
        self.save_devices()

    def get_devices(self) -> List[Dict[str, Any]]:
        """Retrieves a list of devices associated with the current instance.
        
        Returns:
            List[Dict[str, Any]]: A list of dictionaries, where each dictionary represents a device and contains its properties.
        """
        return self.devices

    def get_device(self, name: str) -> Dict[str, Any]:
        """Retrieve a device by its name from the list of devices.
        
        Args:
            name (str): The name of the device to retrieve.
        
        Returns:
            Dict[str, Any]: A dictionary containing the device information if found, or None if no device matches the given name.
        """
        return next((d for d in self.devices if d["name"] == name), None)

    def update_device(self, name: str, **kwargs) -> None:
        """Updates the properties of a device with the given name.
        
        Args:
            name (str): The name of the device to update.
            **kwargs: Arbitrary keyword arguments representing the properties to update.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            ValueError: If no device with the given name is found.
        """
        device = self.get_device(name)
        if device:
            device.update(kwargs)
            self.save_devices()

    def add_device_task(self, name: str, task: str) -> None:
        """Adds a new task to a specified device.
        
        Args:
            name str: The name of the device to add the task to.
            task str: The description of the task to be added.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            KeyError: If the specified device is not found.
        """
        device = self.get_device(name)
        if device:
            device["tasks"].append({"description": task, "completed": False})
            self.save_devices()

    def complete_device_task(self, name: str, task_index: int) -> None:
        """Completes a specific task for a given device.
        
        Args:
            name (str): The name of the device.
            task_index (int): The index of the task to be completed.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            IndexError: If the task_index is out of range for the device's tasks.
            KeyError: If the device with the given name is not found.
        """
        device = self.get_device(name)
        if device and 0 <= task_index < len(device["tasks"]):
            device["tasks"][task_index]["completed"] = True
            self.save_devices()

    def log_device_change(self, name: str, change: str) -> None:
        """Logs a change for a specific device.
        
        Args:
            name (str): The name of the device to log the change for.
            change (str): The description of the change to be logged.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            KeyError: If the device with the given name is not found.
        """
        device = self.get_device(name)
        if device:
            device["changes"].append(
                {"timestamp": datetime.now().isoformat(), "description": change}
            )
            self.save_devices()
