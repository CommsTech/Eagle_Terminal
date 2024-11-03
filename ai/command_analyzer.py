"""This module provides functionality for analyzing and processing commands in
an AI-assisted terminal.

It includes classes and methods for command suggestion, execution, and
result analysis.
"""

from typing import Any, Dict, List


class CommandAnalyzer:
    """A class for analyzing and processing commands in an AI-assisted terminal
    environment.

    This class provides methods for suggesting commands, executing them,
    and analyzing results.
    """

    def __init__(self):
        self.command_history: List[tuple] = []

    def analyze_command_output(
        self, command: str, output: str, os_type: str = "unknown"
    ) -> str:
        """Analyze the output of a command and provide insights.

        Args:
            command (str): The executed command.
            output (str): The output of the command.
            os_type (str): The type of operating system (e.g., "ubuntu", "cisco", "windows").

        Returns:
            str: Analysis of the command output.
        """
        analysis = []

        analysis.append(f"Command executed: {command}")

        if not output.strip():
            analysis.append("The command produced no output.")
        else:
            if os_type.lower() in ("ubuntu", "linux"):
                analysis.extend(self._analyze_linux_command(command, output))
            elif os_type.lower() == "cisco":
                analysis.extend(self._analyze_cisco_command(command, output))
            else:
                analysis.extend(self._analyze_generic_command(output))

        return "\n".join(analysis)

    def _analyze_linux_command(self, command: str, output: str) -> List[str]:
        analysis = []

        if command.startswith("sudo"):
            analysis.append("The command was executed with sudo privileges.")
        elif "permission denied" in output.lower():
            analysis.append(
                "The command resulted in a permission denied error. "
                "You may need to use sudo."
            )

        if command.startswith("cat"):
            if "No such file or directory" in output:
                analysis.append("The specified file or directory does not exist.")
            else:
                analysis.append(
                    "The command successfully displayed the contents of the file."
                )

        if "ansible-playbook" in command:
            if "PLAY RECAP" in output:
                analysis.append("An Ansible playbook was executed.")
                if "failed=0" in output:
                    analysis.append(
                        "The playbook execution was successful with no failures."
                    )
                else:
                    analysis.append("The playbook execution had some failures.")
            else:
                analysis.append(
                    "The command attempted to run an Ansible playbook, "
                    "but it may not have executed successfully."
                )

        return analysis

    def _analyze_cisco_command(self, command: str, output: str) -> List[str]:
        analysis = []

        if "Invalid input detected" in output:
            analysis.append("The command resulted in an error: Invalid input detected.")
            analysis.append(
                "This usually means the command syntax is incorrect or not supported "
                "in the current mode."
            )
        elif "Incomplete command" in output:
            analysis.append(
                "The command is incomplete. Additional parameters may be required."
            )
        elif "% Password:  timeout expired!" in output:
            analysis.append(
                "Authentication failed due to a timeout. "
                "Please try entering the password again."
            )
        elif "Error in authentication" in output:
            analysis.append(
                "Authentication failed. Please check your credentials and try again."
            )
        elif "SSH connection closed" in output:
            analysis.append(
                "The SSH connection was closed unexpectedly. "
                "This might be due to network issues or server-side configuration."
            )
        else:
            analysis.append("The command executed successfully.")
            if command.lower().startswith(("sh", "show")):
                analysis.append(
                    "This is a show command, used to display information about "
                    "the device configuration or status."
                )

        return analysis

    def _analyze_generic_command(self, output: str) -> List[str]:
        analysis = []

        if "error" in output.lower():
            analysis.append(
                "The command resulted in an error. "
                "Please check the syntax and permissions."
            )
        elif "not found" in output.lower():
            analysis.append(
                "The command or file was not found. "
                "Please verify it exists and is in the system path."
            )
        else:
            analysis.append("The command executed successfully.")

        return analysis

    def suggest_next_command(
        self, command_history: List[str], device_info: Dict[str, Any]
    ) -> str:
        """Suggest the next command based on command history and device
        information.

        Args:
            command_history (List[str]): List of previously executed commands.
            device_info (Dict[str, Any]): Information about the device.

        Returns:
            str: Suggested next command.
        """
        os_type = device_info.get("os_type", "unknown").lower()

        if os_type in ("ubuntu", "linux"):
            return self._suggest_linux_command(command_history)
        elif os_type == "cisco":
            return self._suggest_cisco_command(command_history)
        else:
            return "ls -la"  # A generally useful command for many systems

    def _suggest_linux_command(self, command_history: List[str]) -> str:
        if any("permission denied" in cmd.lower() for cmd in command_history[-3:]):
            return f"sudo {command_history[-1]}"  # Suggest using sudo for last command
        elif command_history and command_history[-1].startswith("cat"):
            return f"ls -l {command_history[-1].split()[-1]}"  # List dir of last viewed file
        else:
            return "df -h"  # Show disk usage

    def _suggest_cisco_command(self, command_history: List[str]) -> str:
        if any("Invalid input detected" in cmd for cmd in command_history[-3:]):
            return "show running-config"  # Suggest showing full config after an error
        elif command_history and command_history[-1].lower().startswith(("sh", "show")):
            return "show interfaces status"  # Suggest showing interface status after a show command
        else:
            return "show version"  # Show device version information

    def learn_from_command(self, command: str, output: str) -> None:
        """Learn from the executed command and its output.

        Args:
            command (str): The executed command.
            output (str): The output of the command.
        """
        self.command_history.append((command, output))
        if len(self.command_history) > 50:
            self.command_history.pop(0)

    def explain_command(self, command: str, os_type: str) -> str:
        """Provide an explanation for the given command.

        Args:
            command (str): The command to explain.
            os_type (str): The type of operating system.

        Returns:
            str: Explanation of the command.
        """
        if os_type.lower() in ("ubuntu", "linux"):
            return self._explain_linux_command(command)
        elif os_type.lower() == "cisco":
            return self._explain_cisco_command(command)
        else:
            return (
                "This command may provide useful information or configuration options "
                "for the device."
            )

    def _explain_linux_command(self, command: str) -> str:
        if command.startswith("sudo"):
            return (
                "This command is being run with superuser privileges, "
                "allowing actions that require elevated permissions."
            )
        elif command.startswith("cat"):
            return "This command displays the contents of a file."
        elif "ansible-playbook" in command:
            return (
                "This command runs an Ansible playbook, which is a set of instructions "
                "for automating system configurations or application deployments."
            )
        else:
            return (
                f"This is a Linux command. For more information, you can check its "
                f"man page by running 'man {command.split()[0]}'."
            )

    def _explain_cisco_command(self, command: str) -> str:
        if command == "enable":
            return (
                "This command is used to enter privileged EXEC mode, which is required "
                "for many configuration and show commands."
            )
        elif command.startswith("show running-config"):
            return (
                "This command displays the current configuration of the device. "
                "It requires privileged EXEC mode."
            )
        elif command == "show interfaces status":
            return (
                "This command shows the status of all interfaces on the device, "
                "including their operational state and configuration."
            )
        else:
            return (
                "This is a Cisco IOS command. It may provide information about "
                "the device's configuration or status."
            )
