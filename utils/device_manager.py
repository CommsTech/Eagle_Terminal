import json
from datetime import datetime
from typing import Any, Dict, List


class DeviceManager:
    def __init__(self, file_path: str = "devices.json"):
        self.file_path = file_path
        self.devices = self.load_devices()

    def load_devices(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_devices(self) -> None:
        with open(self.file_path, "w") as f:
            json.dump(self.devices, f, indent=2)

    def add_device(self, device_data):
        self.devices.append(device_data)
        self.save_devices()

    def remove_device(self, name: str) -> None:
        self.devices = [d for d in self.devices if d["name"] != name]
        self.save_devices()

    def get_devices(self) -> List[Dict[str, Any]]:
        return self.devices

    def get_device(self, name: str) -> Dict[str, Any]:
        return next((d for d in self.devices if d["name"] == name), None)

    def update_device(self, name: str, **kwargs) -> None:
        device = self.get_device(name)
        if device:
            device.update(kwargs)
            self.save_devices()

    def add_device_task(self, name: str, task: str) -> None:
        device = self.get_device(name)
        if device:
            device["tasks"].append({"description": task, "completed": False})
            self.save_devices()

    def complete_device_task(self, name: str, task_index: int) -> None:
        device = self.get_device(name)
        if device and 0 <= task_index < len(device["tasks"]):
            device["tasks"][task_index]["completed"] = True
            self.save_devices()

    def log_device_change(self, name: str, change: str) -> None:
        device = self.get_device(name)
        if device:
            device["changes"].append(
                {"timestamp": datetime.now().isoformat(), "description": change}
            )
            self.save_devices()
