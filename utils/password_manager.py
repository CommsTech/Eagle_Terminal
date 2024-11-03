import os

import bcrypt
from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        """Initialize a new instance of the class.
        
        This method initializes a new instance of the class by loading or generating an encryption key
        and creating a Fernet object for encryption/decryption operations.
        
        Args:
            self: The instance of the class being initialized.
        
        Returns:
            None
        
        Attributes:
            key (bytes): The encryption key used for Fernet operations.
            fernet (Fernet): The Fernet instance used for encryption and decryption.
        """
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):
        """Loads an existing encryption key from a file or generates a new one if the file doesn't exist.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            bytes: The encryption key, either loaded from the file or newly generated.
        
        Raises:
            IOError: If there are issues reading from or writing to the key file.
        """
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            return key

    def hash_password(self, password):
        """Hash a password using bcrypt.
        
        Args:
            password (str): The plain text password to be hashed.
        
        Returns:
            bytes: The hashed password as a byte string.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        """Verify if a given password matches a hashed password.
        
        Args:
            password (str): The plain text password to be verified.
            hashed (bytes): The hashed password to compare against.
        
        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed)

    def encrypt_password(self, password):
        """Encrypts the given password using Fernet encryption.
        
        Args:
            password (str): The plain text password to be encrypted.
        
        Returns:
            bytes: The encrypted password as bytes.
        """
        return self.fernet.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        """Decrypts an encrypted password using the Fernet encryption scheme.
        
        Args:
            encrypted_password (bytes): The encrypted password to be decrypted.
        
        Returns:
            str: The decrypted password as a string.
        
        Raises:
            InvalidToken: If the token is invalid or expired.
            TypeError: If the input is not bytes.
        """
        return self.fernet.decrypt(encrypted_password).decode()
