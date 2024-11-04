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
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.port = port
        self.client = None
        self.channel = None

    async def async_connect(self):
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
        if not self.channel:
            return

        await asyncio.get_event_loop().run_in_executor(None, self.channel.send, data)

    async def execute_command(self, command):
        await self.write_input(command + "\n")
        while True:
            output = await self.read_output()
            if output:
                yield output
            else:
                break

    async def read_output_generator(self):
        while True:
            output = await self.read_output()
            if output:
                yield output
            else:
                await asyncio.sleep(0.1)

    async def get_os_type(self):
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
        if self.channel:
            self.channel.close()
        if self.client:
            self.client.close()
        logger.info(f"Closed connection to {self.hostname}")

    async def open_sftp(self):
        if not self.client:
            raise Exception("Not connected to SSH server")
        if not self.sftp:
            self.sftp = await asyncio.get_event_loop().run_in_executor(
                None, self.client.open_sftp
            )
        return self.sftp

    async def get_sftp_client(self):
        return await self.open_sftp()

    async def sftp_list_dir(self, path):
        sftp = await self.get_sftp_client()
        return await asyncio.get_event_loop().run_in_executor(None, sftp.listdir, path)

    async def sftp_get(self, remotepath, localpath):
        sftp = await self.get_sftp_client()
        await asyncio.get_event_loop().run_in_executor(
            None, sftp.get, remotepath, localpath
        )

    async def sftp_put(self, localpath, remotepath):
        sftp = await self.get_sftp_client()
        await asyncio.get_event_loop().run_in_executor(
            None, sftp.put, localpath, remotepath
        )


def retry_connection(ssh_connection, max_attempts=3, delay=5):
    for attempt in range(max_attempts):
        if ssh_connection.connect():
            return True
        logger.warning(
            f"Connection attempt {attempt + 1} failed. Retrying in {delay} seconds..."
        )
        time.sleep(delay)
    return False


def execute_with_timeout(func, *args, timeout=30, **kwargs):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        result = func(*args, **kwargs)
        if result is not None:
            return result
        time.sleep(0.5)
    logger.error(f"Execution timed out after {timeout} seconds")
    return None


async def execute_ssh_command(connection, command):
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
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_pem, public_key
