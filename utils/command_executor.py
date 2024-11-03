import re

from utils.logger import logger


def execute_command_with_prompt(ssh_connection, command, prompt="#", timeout=30):
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
    if prompts is None:
        prompts = ["#"] * len(commands)

    results = []
    for command, prompt in zip(commands, prompts):
        result = execute_command_with_prompt(ssh_connection, command, prompt, timeout)
        results.append(result)

    return results
