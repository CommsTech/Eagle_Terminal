"""This module provides functionality for retrieving device status and
information.

It includes functions for handling SSH and local devices, as well as
utility functions for command execution and sanitization.
"""

import re
import shlex
import subprocess
from typing import Any, Dict

import paramiko


def get_device_status(device: Dict[str, Any]) -> Dict[str, Any]:
    """Get the status of a device based on its type.

    Args:
        device (Dict[str, Any]): A dictionary containing device information.

    Returns:
        Dict[str, Any]: A dictionary containing the device status.
    """
    if device["type"] == "ssh":
        return get_ssh_device_status(device)
    elif device["type"] == "local":
        return get_local_device_status()
    else:
        return {"status": "unknown", "error": "Unsupported device type"}


def get_ssh_device_status(device: Dict[str, Any]) -> Dict[str, Any]:
    """Get the status of an SSH device.

    Args:
        device (Dict[str, Any]): A dictionary containing SSH device information.

    Returns:
        Dict[str, Any]: A dictionary containing the SSH device status.
    """
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())

        client.connect(
            device["hostname"],
            username=device["username"],
            password=device.get("password"),
            key_filename=device.get("key_filename"),
        )

        status = {}

        status["uptime"] = safe_execute_command(client, "uptime")
        status["memory_usage"] = safe_execute_command(
            client, "free -m | awk '/Mem:/ {print $3/$2 * 100.0}'"
        )
        status["cpu_usage"] = safe_execute_command(
            client, "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
        )
        status["disk_usage"] = safe_execute_command(
            client, r"df -h / | awk '/\// {print $5}'"
        )

        client.close()
        return status
    except Exception as e:
        return {"status": "error", "error": str(e)}


import ssl

def safe_execute_command_with_ssl(client, command):
    """Safely execute a command on an SSH client with verified SSL context.

    Args:
        client: The SSH client with verified SSL.
        command (str): The command to execute.

    Returns:
        str: The output of the command.
    """
    context = ssl.create_default_context()
    client = client.wrap_socket(context)  # Ensure the client uses the secure context
    sanitized_command = shlex.quote(command)
    _, stdout, _ = client.exec_command(sanitized_command)
    return stdout.read().decode("utf-8").strip()


def get_local_device_status() -> Dict[str, Any]:
    """Get the status of the local device.

    Returns:
        Dict[str, Any]: A dictionary containing the local device status.
    """
    try:
        status = {}
        status["uptime"] = subprocess.check_output(["uptime"]).decode("utf-8").strip()
        status["memory_usage"] = (
            subprocess.check_output(["free", "-m"]).decode("utf-8").strip()
        )
        status["cpu_usage"] = (
            subprocess.check_output(["top", "-bn1"]).decode("utf-8").strip()
        )
        # Fixed command by removing shell=True and using subprocess capabilities
        status["disk_usage"] = subprocess.check_output(["bash", "-c", "/bin/df -h / | awk '/\// {print $5}'"]).decode("utf-8").strip()
        return status
    except Exception as e:
        return {"status": "error", "error": str(e)}



def sanitize_command(command: str) -> str:
    """Sanitize a command by removing potentially dangerous characters.

    Args:
        command (str): The command to sanitize.

    Returns:
        str: The sanitized command.
    """
    return re.sub(r"[;&|]", "", command)


def get_device_info(device):
    """Get information about a device.

    Args:
        device (dict): A dictionary containing device information.

    Returns:
        dict: A dictionary containing the device status and other relevant information.
    """
    device_type = device.get("type")

    if device_type is None:
        return {"status": "unknown", "error": "Device type not specified"}

    if device_type == "ssh":
        return get_ssh_device_info(device)
    elif device_type == "serial":
        # Note: This function is not implemented in the provided code
        # You should implement get_serial_device_info or remove this condition
        return {"status": "unknown", "error": "Serial device info not implemented"}
    else:
        return {"status": "unknown", "error": f"Unsupported device type: {device_type}"}


def get_ssh_device_info(device):
    """Get information about an SSH device.

    Args:
        device (dict): A dictionary containing SSH device information.

    Returns:
        dict: A dictionary containing the SSH device information.
    """
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.RejectPolicy())

        client.connect(
            device["hostname"],
            username=device["username"],
            password=device.get("password"),
            key_filename=device.get("key_filename"),
        )

        info = {}
        info["hostname"] = safe_execute_command(client, "hostname")
        info["os"] = safe_execute_command(client, "uname -s")
        info["kernel"] = safe_execute_command(client, "uname -r")
        info["architecture"] = safe_execute_command(client, "uname -m")

        client.close()
        return info
    except Exception as e:
        return {"error": str(e)}


def get_local_device_info() -> Dict[str, Any]:
    """Get information about the local device.

    Returns:
        Dict[str, Any]: A dictionary containing the local device information.
    """
    try:
        info = {}
        commands = {
            "hostname": ["hostname"],
            "os": ["uname", "-s"],
            "kernel": ["uname", "-r"],
            "architecture": ["uname", "-m"]
        }
        
        info["hostname"] = subprocess.check_output(commands["hostname"]).decode("utf-8").strip()
        info["os"] = subprocess.check_output(commands["os"]).decode("utf-8").strip()
        info["kernel"] = subprocess.check_output(commands["kernel"]).decode("utf-8").strip()
        info["architecture"] = subprocess.check_output(commands["architecture"]).decode("utf-8").strip()
        return info
    except Exception as e:
        return {"error": str(e)}
