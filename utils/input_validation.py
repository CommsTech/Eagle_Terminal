import re
from typing import Any, Callable, Union


def validate_input(
    input_value: Union[str, int],
    input_type: str,
    min_length: int = 0,
    max_length: int = None,
) -> bool:
    """Validate user input based on specified criteria.

    Args:
        input_value (Union[str, int]): The input value to validate.
        input_type (str): The expected type of the input ('str' or 'int').
        min_length (int, optional): The minimum length for string inputs. Defaults to 0.
        max_length (int, optional): The maximum length for string inputs. Defaults to None.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    if input_type == "str":
        if not isinstance(input_value, str):
            return False
        if len(input_value) < min_length:
            return False
        if max_length is not None and len(input_value) > max_length:
            return False
    elif input_type == "int":
        if not isinstance(input_value, int):
            return False
    else:
        return False

    return True


# You can add more specific validation functions here if needed


def sanitize_input(input_value: str) -> str:
    """Sanitize user input by removing potentially dangerous characters."""
    return re.sub(r"[;&|]", "", input_value)


def validate_and_sanitize(input_value: str, validation_type: str) -> str:
    """Validate and sanitize user input."""
    if not validate_input(input_value, validation_type):
        raise ValueError(f"Invalid {validation_type}: {input_value}")
    return sanitize_input(input_value)


def safe_input(prompt: str, validation_type: str) -> str:
    """Safely get user input with validation and sanitization."""
    while True:
        user_input = input(prompt)
        try:
            return validate_and_sanitize(user_input, validation_type)
        except ValueError as e:
            print(f"Error: {e}. Please try again.")


"""Input validation utilities for connection parameters."""


def validate_connection_params(connection_type, host, port, username, password):
    """Validate connection parameters based on the connection type.

    Args:
        connection_type (str): The type of connection (SSH or Serial).
        host (str): The hostname or IP address for SSH connections.
        port (str): The port number for SSH or device name for Serial connections.
        username (str): The username for SSH connections.
        password (str): The password for SSH connections.

    Returns:
        bool: True if parameters are valid, False otherwise.
    """
    if connection_type == "SSH":
        return (
            host.strip() != ""
            and port.isdigit()
            and 1 <= int(port) <= 65535
            and username.strip() != ""
            and password != ""
        )
    elif connection_type == "Serial":
        return port.strip() != ""
    else:
        return False


DEFAULT_PASSWORD = None  # or use a secure method to generate a default password
