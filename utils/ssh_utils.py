import asyncio
import logging
import socket
import time

import paramiko
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from paramiko.agent import Agent
from paramiko.channel import Channel
from paramiko.client import AutoAddPolicy, SSHClient
from paramiko.pkey import PKey
from paramiko.ssh_exception import (AuthenticationException,
                                    BadHostKeyException, SSHException)

from utils.logging_config import logger


class SSHConnection:
    def __init__(self, hostname, username, password=None, key_filename=None, port=22):
        """Initialize a new SSH connection object.
        
        Args:
            hostname (str): The hostname or IP address of the SSH server.
            username (str): The username to authenticate with on the SSH server.
            password (str, optional): The password for authentication. Defaults to None.
            key_filename (str, optional): The filename of the private key to use for authentication. Defaults to None.
            port (int, optional): The port number of the SSH server. Defaults to 22.
        
        Returns:
            None
        
        Raises:
            None
        
        Attributes:
            hostname (str): The hostname or IP address of the SSH server.
            username (str): The username for authentication.
            password (str): The password for authentication (if provided).
            key_filename (str): The filename of the private key (if provided).
            port (int): The port number of the SSH server.
            client (None): Placeholder for the SSH client object.
            channel (None): Placeholder for the SSH channel object.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None
        self.channel = None

    async def async_connect(self):
        """Asynchronously establishes an SSH connection to a remote host.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            tuple: A tuple containing:
                - bool: True if the connection was successful, False otherwise.
                - str: The OS type of the remote host if connection was successful, "unknown" otherwise.
        
        Raises:
            Exception: If there's an error during the connection process.
        """
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            connect_kwargs = {
                "hostname": self.hostname,
                "port": self.port,
                "username": self.username,
                "password": self.password,
                "key_filename": self.key_filename,
                "timeout": 10,
            }

            await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.client.connect(**connect_kwargs)
            )

            self.channel = await asyncio.get_event_loop().run_in_executor(
                None, self.client.invoke_shell
            )
            self.channel.settimeout(0.1)  # Set a short timeout for non-blocking reads

            logger.info(f"Connected to {self.hostname}")
            return True, await self.get_os_type()
        except Exception as e:
            logger.error(f"Failed to connect to {self.hostname}: {str(e)}")
            return False, "unknown"

    async def read_output(self):
        """Asynchronously reads output from an SSH channel.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            str or None: The decoded output from the SSH channel as a UTF-8 string,
            or None if no channel is available, if there's a channel exception,
            or if there's a socket timeout.
        
        Raises:
            None explicitly, but may propagate exceptions from asyncio or paramiko.
        """
        if not self.channel:
            return None

        try:
            output = await asyncio.get_event_loop().run_in_executor(
                None, self.channel.recv, 4096
            )
            return output.decode("utf-8", errors="replace")
        except paramiko.ssh_exception.ChannelException:
            return None
        except socket.timeout:
            return None  # No data available

    async def write_input(self, data):
        """Asynchronously writes input data to a channel.
        
        Args:
            data (Any): The data to be sent to the channel.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            RuntimeError: If the channel is not initialized.
        """
        if not self.channel:
            return

        await asyncio.get_event_loop().run_in_executor(None, self.channel.send, data)

    async def execute_command(self, command):
        """Executes a command asynchronously and yields the output.
        
        This method sends a command to the input stream, then continuously reads from the output stream,
        yielding any non-empty output until the stream is exhausted.
        
        Args:
            command (str): The command to be executed.
        
        Returns:
            AsyncGenerator[str, None]: An asynchronous generator that yields output strings.
        
        Raises:
            None
        """
        await self.write_input(command + "\n")
        while True:
            output = await self.read_output()
            if output:
                yield output
            else:
                break

    async def read_output_generator(self):
        """An asynchronous generator method that continuously reads output and yields it.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            AsyncGenerator[Any, None]: An asynchronous generator that yields output as it becomes available.
        
        Raises:
            None
        
        Notes:
            - This method runs in an infinite loop, continuously checking for new output.
            - If no output is available, it waits for 0.1 seconds before checking again.
            - The actual type of the output depends on what the `read_output` method returns.
        """
        while True:
            output = await self.read_output()
            if output:
                yield output
            else:
                await asyncio.sleep(0.1)

    async def get_os_type(self):
        """Asynchronously determines the operating system type of the current environment.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            str: A string representing the detected operating system type.
                 Possible values are:
                 - 'linux': For Linux-based operating systems
                 - 'macos': For macOS operating systems
                 - 'windows': For Windows operating systems
                 - 'unknown': If the operating system type cannot be determined
        
        Raises:
            None
        
        Note:
            This method uses the 'uname -s' command to determine the operating system type.
            It writes the command to the input, waits for execution, and then reads the output.
            The method has a built-in delay of 0.5 seconds to allow time for command execution.
        """
        await self.write_input("uname -s\n")
        await asyncio.sleep(0.5)  # Give some time for the command to execute
        output = await self.read_output()
        os_type = output.strip().lower() if output else "unknown"
        if "linux" in os_type:
            return "linux"
        elif "darwin" in os_type:
            return "macos"
        elif "windows" in os_type:
            return "windows"
        else:
            return "unknown"

    async def close(self):
        """Closes the connection and associated resources.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None
        
        Raises:
            None
        """
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        logger.info(f"Closed connection to {self.hostname}")

    async def open_sftp(self):
        """Open an SFTP session.
        
        This method opens an SFTP (SSH File Transfer Protocol) session using the existing SSH connection.
        If there's no active SSH connection, it raises an exception. If an SFTP session is not already
        open, it creates a new one.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            paramiko.SFTPClient: An SFTP client object for file transfer operations.
        
        Raises:
            Exception: If not connected to an SSH server when trying to open the SFTP session.
        """
        if not self.client:
            raise Exception("Not connected to SSH server")
        if not self.sftp:
            self.sftp = await asyncio.get_event_loop().run_in_executor(
                None, self.client.open_sftp
            )
        return self.sftp

    async def get_sftp_client(self):
        """Asynchronously creates and returns an SFTP client.
        
        Returns:
            asyncssh.SFTPClient: An asynchronous SFTP client object.
        """
        return await self.open_sftp()

    async def sftp_list_dir(self, path):
        """Asynchronously list the contents of a directory on an SFTP server.
        
        Args:
            path (str): The path of the directory to list.
        
        Returns:
            list: A list of filenames in the specified directory.
        
        Raises:
            SFTPError: If there's an error accessing the SFTP server or listing the directory.
        """
        sftp = await self.get_sftp_client()
        return await asyncio.get_event_loop().run_in_executor(None, sftp.listdir, path)

    async def sftp_get(self, remotepath, localpath):
        """Asynchronously retrieves a file from a remote SFTP server and saves it locally.
        
        Args:
            remotepath (str): The path of the file on the remote SFTP server.
            localpath (str): The path where the file should be saved locally.
        
        Returns:
            None: This method doesn't return anything explicitly.
        
        Raises:
            SFTPException: If there's an error during the SFTP file transfer.
            IOError: If there's an issue with local file operations.
        """
        sftp = await self.get_sftp_client()
        await asyncio.get_event_loop().run_in_executor(
            None, sftp.get, remotepath, localpath
        )

    async def sftp_put(self, localpath, remotepath):
        """Uploads a local file to a remote SFTP server asynchronously.
        
        Args:
            localpath (str): The path to the local file to be uploaded.
            remotepath (str): The destination path on the remote SFTP server.
        
        Returns:
            None: This method doesn't return anything explicitly.
        
        Raises:
            SFTPException: If there's an error during the SFTP operation.
            IOError: If there's an issue reading the local file or writing to the remote path.
        """
        sftp = await self.get_sftp_client()
        await asyncio.get_event_loop().run_in_executor(
            None, sftp.put, localpath, remotepath
        )


def retry_connection(ssh_connection, max_attempts=3, delay=5):
    """Attempts to establish an SSH connection with retry logic.
    
    Args:
        ssh_connection: The SSH connection object to be used for connecting.
        max_attempts (int): The maximum number of connection attempts. Defaults to 3.
        delay (int): The delay in seconds between connection attempts. Defaults to 5.
    
    Returns:
        bool: True if the connection was successful, False otherwise.
    """
    for attempt in range(max_attempts):
        if ssh_connection.connect():
            return True
        logger.warning(
            f"Connection attempt {attempt + 1} failed. Retrying in {delay} seconds..."
        )
        time.sleep(delay)
    return False


def execute_with_timeout(func, *args, timeout=30, **kwargs):
    """Executes a function with a timeout mechanism.
    
    Args:
        func (callable): The function to be executed.
        *args: Variable length argument list to be passed to the function.
        timeout (int, optional): Maximum execution time in seconds. Defaults to 30.
        **kwargs: Arbitrary keyword arguments to be passed to the function.
    
    Returns:
        Any: The result of the function if it completes within the timeout period, or None if it times out.
    
    Raises:
        None explicitly, but may raise exceptions from the executed function.
    """
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        result = func(*args, **kwargs)
        if result is not None:
            return result
        time.sleep(0.5)
    logger.error(f"Execution timed out after {timeout} seconds")
    return None


async def execute_ssh_command(connection, command):
    """Executes an SSH command on a remote server.
    
    Args:
        connection (SSHConnection): The established SSH connection object.
        command (str): The command to be executed on the remote server.
    
    Returns:
        str: The standard output of the executed command.
    
    Raises:
        PermissionDenied: If the user lacks the necessary permissions to execute the command.
        ConnectionLost: If the SSH connection is lost during command execution.
        Exception: For any unexpected errors that occur during command execution.
    """
    try:
        result = await connection.run(command)
        return result.stdout
    except PermissionDenied:
        logging.error(f"Permission denied for command: {command}")
    except ConnectionLost:
        logging.error("SSH connection lost. Attempting to reconnect...")
        # Implement reconnection logic
    except Exception as e:
        logging.error(f"Unexpected error executing SSH command: {str(e)}")


def generate_ssh_key():
    """Generate an SSH key pair.
    
    This function creates a new RSA key pair for SSH authentication. It generates a 2048-bit RSA private key and its corresponding public key.
    
    Args:
        None
    
    Returns:
        tuple: A tuple containing two elements:
            - bytes: The private key in PEM format.
            - rsa.RSAPublicKey: The public key object.
    
    Raises:
        cryptography.exceptions.UnsupportedAlgorithm: If the required cryptographic algorithms are not available.
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_pem, public_key
