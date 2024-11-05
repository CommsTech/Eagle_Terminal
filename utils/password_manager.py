import os

import bcrypt
from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        """Initialize the object with a key and Fernet instance.
        
        This method initializes the object by loading or generating a key and creating a Fernet instance with that key. The key is used for encryption and decryption operations.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            key (bytes): The encryption key, either loaded from storage or newly generated.
            fernet (Fernet): A Fernet instance initialized with the key for cryptographic operations.
        
        Raises:
            CryptographyError: If there's an issue loading or generating the key.
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
        """Hashes a password using bcrypt.
        
        Args:
            password (str): The plain text password to be hashed.
        
        Returns:
            bytes: The hashed password as a byte string.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        """Verify if a given password matches the stored hashed password.
        
        Args:
            password (str): The plaintext password to verify.
            hashed (bytes): The hashed password to compare against.
        
        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return bcrypt.checkpw(password.encode(), hashed)

    def encrypt_password(self, password):
        """Encrypts a given password using Fernet encryption.
        
        Args:
            password (str): The password to be encrypted.
        
        Returns:
            bytes: The encrypted password as bytes.
        """
        return self.fernet.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        """Decrypts an encrypted password using the Fernet symmetric encryption.
        
        Args:
            encrypted_password (bytes): The encrypted password to be decrypted.
        
        Returns:
            str: The decrypted password as a string.
        
        Raises:
            cryptography.fernet.InvalidToken: If the token is invalid or expired.
        """
        return self.fernet.decrypt(encrypted_password).decode()
