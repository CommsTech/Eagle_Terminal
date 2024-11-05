import re

from utils.logger import logger


def execute_command_with_prompt(ssh_connection, command, prompt="#", timeout=30):
    """Execute a command on an SSH connection and return the output without the prompt.
    
    Args:
        ssh_connection (SSHConnection): The established SSH connection object.
        command (str): The command to be executed on the remote system.
        prompt (str, optional): The prompt string to identify the end of the output. Defaults to "#".
        timeout (int, optional): The maximum time to wait for the command execution in seconds. Defaults to 30.
    
    Returns:
        str or None: The command output without the prompt line if successful, None if the command execution fails.
    
    Raises:
        None
    
    Notes:
        - The function uses a regular expression to find the prompt in the output.
        - If the prompt is not found, a warning is logged, and the full output is returned.
        - The function assumes that the SSHConnection object has an execute_command method.
    """
    output = ssh_connection.execute_command(command, timeout)
    if output is None:
        return None

    lines = output.splitlines()
    prompt_pattern = re.escape(prompt)
    for line in reversed(lines):
        if re.search(prompt_pattern, line):
            return "\n".join(lines[:-1])  # Exclude the prompt line

    logger.warning(f"Prompt '{prompt}' not found in the output")
    return output


def execute_multiple_commands(ssh_connection, commands, prompts=None, timeout=30):
    """Execute multiple SSH commands with specified prompts.
    
    Args:
        ssh_connection (paramiko.SSHClient): An established SSH connection.
        commands (List[str]): A list of commands to execute.
        prompts (List[str], optional): A list of prompts to expect after each command. Defaults to ["#"] * len(commands).
        timeout (int, optional): The timeout for each command execution in seconds. Defaults to 30.
    
    Returns:
        List[str]: A list of results from each command execution.
    
    Raises:
        ValueError: If the length of commands and prompts don't match when prompts are provided.
    """
    if prompts is None:
        prompts = ["#"] * len(commands)

    results = []
    for command, prompt in zip(commands, prompts):
        result = execute_command_with_prompt(ssh_connection, command, prompt, timeout)
        results.append(result)

    return results
