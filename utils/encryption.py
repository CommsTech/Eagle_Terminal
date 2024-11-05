import os

from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def generate_key():
    """Generate a new encryption key and save it to a file.
    
    This function checks if a key file already exists. If not, it generates a new
    Fernet encryption key and writes it to the specified file.
    
    Args:
        None
    
    Returns:
        None
    
    Raises:
        IOError: If there's an issue writing the key to the file.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    """Reads and returns the contents of a key file.
    
    Args:
        None
    
    Returns:
        bytes: The binary contents of the key file.
    
    Raises:
        FileNotFoundError: If the KEY_FILE does not exist.
        IOError: If there's an error reading the file.
    """
    return open(KEY_FILE, "rb").read()


def encrypt_data(data):
    """Encrypts the provided data using Fernet symmetric encryption.
    
    Args:
        data (str): The data to be encrypted.
    
    Returns:
        bytes: The encrypted data as a byte string.
    
    Raises:
        TypeError: If the input data is not a string.
        CryptographyError: If there's an issue with key generation or encryption.
    """
    generate_key()
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())


def decrypt_data(encrypted_data):
    """Decrypts encrypted data using a Fernet key.
    
    Args:
        encrypted_data (bytes): The encrypted data to be decrypted.
    
    Returns:
        str: The decrypted data as a string.
    
    Raises:
        ValueError: If the encrypted_data is not valid or the key is incorrect.
        TypeError: If the encrypted_data is not of type bytes.
    """
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()


def encrypt_password(password):
    """Encrypts a given password using the Fernet symmetric encryption.
    
    Args:
        password (str): The password to be encrypted.
    
    Returns:
        bytes: The encrypted password as bytes.
    
    Raises:
        TypeError: If the password is not a string.
        CryptographyError: If there's an issue with key generation or encryption.
    """
    generate_key()
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    """Decrypts an encrypted password using a Fernet key.
    
    Args:
        encrypted_password (bytes): The encrypted password to be decrypted.
    
    Returns:
        str: The decrypted password as a string.
    
    Raises:
        ValueError: If the encrypted_password is invalid or the key is incorrect.
        TypeError: If the encrypted_password is not in bytes format.
    """
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()
