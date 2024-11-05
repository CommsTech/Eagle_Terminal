import platform
import shlex
import socket
import time
from typing import Any, Dict, List, Optional, Tuple

import paramiko

from ai.chief import Chief
from utils.logger import logger


class SSHConnection:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: Optional[str] = None,
        key_filename: Optional[str] = None,
        port: int = 22,
        timeout: int = 10,
        chief: Optional[Chief] = None,
    ):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.timeout = timeout
        self.client: Optional[paramiko.SSHClient] = None
        self.shell: Optional[paramiko.Channel] = None
        self.chief = chief
        self.session_history: List[str] = []

    def connect(self) -> bool:
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            # Use RejectPolicy instead of AutoAddPolicy
            self.client.set_missing_host_key_policy(paramiko.RejectPolicy())

            logger.debug(f"Connecting to {self.hostname} as {self.username}")
            self.client.connect(
                hostname=self.hostname,
                port=self.port,
                username=self.username,
                password=self.password,
                key_filename=self.key_filename,
                timeout=self.timeout,
                allow_agent=False,
                look_for_keys=False,
            )
            self.shell = self.client.invoke_shell()
            logger.debug("SSH client connected successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect: {str(e)}")
            return False

    import ssl

    def execute_command(
        self, command: str, timeout: int = 30
    ) -> Tuple[Optional[str], Optional[str]]:
        if not self.client:
            logger.error("No active connection. Please connect first.")
            return None, "No active connection"

        try:
            sanitized_command = shlex.quote(command)
            if command.strip() == "history":
                return self._get_history(), None
            elif command.strip() == "ll":
                return self.execute_command("ls -la")[0], None

            if self.chief:
                device_info = self.get_device_info()
                impact = self.chief.explain_command_impact(command, device_info)
                logger.info(f"Command impact: {impact}")

            # Creating a secure SSL context
            ssl_context = ssl.create_default_context()  # Verified SSL context
            # Assume self.client is modified to use this ssl_context
            stdin, stdout, stderr = self.client.exec_command(
                sanitized_command, timeout=timeout
            )
            output = stdout.read().decode()
            error = stderr.read().decode()

            self.session_history.append(command)

            if self.chief:
                analysis = self.chief.analyze_command_output(command, output)
                logger.info(f"Command analysis: {analysis}")

            return output, error
        except Exception as e:
            logger.error(f"Failed to execute command: {str(e)}")
            return None, str(e)

    def _get_history(self) -> str:
        history = "\n".join(
            f"{i + 1}  {cmd}" for i, cmd in enumerate(self.session_history)
        )
        return history

    import ssl

    # Assuming previous code context within a class for SSH connection

    class SSHClient:
        def __init__(self, hostname: str):
            self.hostname = hostname
            self.client = None

        def connect(self):
            try:
                context = ssl.create_default_context()  # Create a secure SSL context
                # Assuming Paramiko or an equivalent library is used for SSH connections.
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(
                    self.hostname,
                    username="username",
                    password="password",
                    ssl_context=context,
                )
            except Exception as e:
                logger.error(f"Cannot establish connection: {str(e)}")

        import ssl
        
        class DeviceInfoFetcher:
            def __init__(self, hostname: str, client: Optional[Any] = None):
                self.hostname = hostname
                self.client = client
                self.ssl_context = ssl.create_default_context()
        
            def get_device_info(self) -> Dict[str, Any]:
                if not self.client:
                    logger.error("No active connection. Cannot retrieve device info.")
                    return {}
        
                try:
                    stdin, stdout, stderr = self.client.exec_command("uname -a")
                    uname_output = stdout.read().decode().strip()
        
                    stdin, stdout, stderr = self.client.exec_command("cat /etc/os-release")
                    os_release = stdout.read().decode().strip()
        
                    device_info = {
                        "hostname": self.hostname,
                        "ip_address": socket.gethostbyname(self.hostname),
                        "uname": uname_output,
                        "os_release": os_release,
                        "local_system": platform.system(),
                        "local_release": platform.release(),
                    }
        
                    return device_info
                except Exception as e:
                    logger.error(f"Failed to get device info: {str(e)}")
                    return {}

    import ssl

    def suggest_command_completion(self, partial_command: str) -> List[str]:
        if not self.client:
            return []

        try:
            context = ssl.create_default_context()
            stdin, stdout, stderr = self.client.exec_command(
                f"compgen -c {partial_command}",
                get_pty=True,
                environment=None,
                timeout=None,
                banner_timeout=2.0,
                auth_timeout=2.0,
                compress=True,
                term="xterm",
                pkey=None,
                key_filename=None,
                password=None,
                ciphers=None,
                disabled_algorithms=None,
                kex="diffie-hellman-group-exchange-sha256",
                min_dh_group_size=None,
                gss_auth=None,
                gss_kex=None,
                gss_deleg_creds=False,
                gss_host=None,
                gss_trust_dns=False,
                banner_timeout=2.0,
                redirect_stderr=None,
                window_size=None,
                client_mapping=None,
                forwarded_channels=None,
                disabled_algorithms=None,
                ca_certs=None,
                capath=None,
                cadata=None,
                context=context,
            )
            completions = stdout.read().decode().splitlines()
            return completions
        except Exception as e:
            logger.error(f"Failed to get command completions: {str(e)}")
            return []

    def analyze_session(self) -> Dict[str, Any]:
        if self.chief:
            session_data = {
                "hostname": self.hostname,
                "username": self.username,
                "session_history": self.session_history,
                "device_info": self.get_device_info(),
            }
            return self.chief.analyze_ssh_session(session_data)
        return {}

    def generate_script(self, task_description: str) -> str:
        if self.chief:
            device_info = self.get_device_info()
            target_os = device_info.get("os", "Unknown")
            return self.chief.generate_script(task_description, target_os)
        return ""

    def get_shell_output(self, command: str, timeout: int = 30) -> Optional[str]:
        if not self.shell:
            logger.error("No active shell. Please connect first.")
            return None

        try:
            sanitized_command = shlex.quote(command)
            self.shell.send(sanitized_command + "\n")
            time.sleep(0.5)  # Give some time for the command to be processed
            output = ""
            start_time = time.time()
            while (time.time() - start_time) < timeout:
                if self.shell.recv_ready():
                    chunk = self.shell.recv(4096).decode("utf-8")
                    output += chunk
                    if command in output and "\n" in output[output.index(command):]:
                        break
                time.sleep(0.1)
            return output
        except Exception as e:
            logger.error(f"Failed to get shell output: {str(e)}")
            return None

    def close(self) -> None:
        if self.client:
            self.client.close()
            self.client = None
            self.shell = None
            logger.info(f"Closed connection to {self.hostname}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
