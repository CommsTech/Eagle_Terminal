import json

import bcrypt
from cryptography.fernet import Fernet

from utils.logger import EagleTerminalException, logger
from utils.secure_storage import SecureStorage


class UserAuth:
    def __init__(self, users_file="users.json", key_file="secret.key"):
        """Initialize the UserAuthentication class.
        
        Args:
            users_file (str, optional): The path to the JSON file containing user data. Defaults to "users.json".
            key_file (str, optional): The path to the file containing the encryption key. Defaults to "secret.key".
        
        Returns:
            None
        
        """
        self.users_file = users_file
        self.key_file = key_file
        self.users = self.load_users()
        self.fernet = self.load_or_create_key()
        self.secure_storage = SecureStorage()

    def load_or_create_key(self):
        """Loads an existing encryption key from a file or creates a new one if not found.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            Fernet: A Fernet instance initialized with the loaded or newly created key.
        
        Raises:
            FileNotFoundError: If the key file is not found (handled internally).
        """
        try:
            with open(self.key_file, "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
        return Fernet(key)

    def load_users(self):
        """Loads user data from a JSON file.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: A dictionary containing user data loaded from the JSON file. If the file is not found, an empty dictionary is returned.
        
        Raises:
            FileNotFoundError: If the specified users file does not exist. This exception is caught and handled internally.
        """
        try:
            with open(self.users_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        """Saves the current user data to a JSON file.
        
        This method writes the user data stored in the `self.users` dictionary
        to a JSON file specified by `self.users_file`.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            None
        
        Raises:
            IOError: If there is an error writing to the file.
            JSONDecodeError: If there is an error encoding the user data to JSON.
        """
        with open(self.users_file, "w") as file:
            json.dump(self.users, file)

    def register_user(self, username, password):
        """Registers a new user with the provided username and password.
        
        Args:
            username (str): The desired username for the new user.
            password (str): The password for the new user.
        
        Returns:
            None
        
        Raises:
            EagleTerminalException: If the username already exists in the system.
        """
        if username in self.users:
            raise EagleTerminalException("Username already exists")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.users[username] = hashed.decode("utf-8")
        self.save_users()

    def authenticate_user(self, username, password):
        """Authenticates a user by comparing the provided username and password.
        
        Args:
            username (str): The username of the user to authenticate.
            password (str): The password to check against the stored hash.
        
        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        if username not in self.users:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"), self.users[username].encode("utf-8")
        )

    def encrypt_data(self, data):
        """Encrypts the provided data using Fernet encryption.
        
        Args:
            data (Any): The data to be encrypted. Can be any JSON-serializable object.
        
        Returns:
            bytes: The encrypted data as a byte string.
        """
        return self.fernet.encrypt(json.dumps(data).encode("utf-8"))

    def decrypt_data(self, encrypted_data):
        """Decrypts the given encrypted data using the Fernet encryption system.
        
        Args:
            encrypted_data (bytes): The encrypted data to be decrypted.
        
        Returns:
            dict: The decrypted data as a Python dictionary.
        
        Raises:
            json.JSONDecodeError: If the decrypted data is not valid JSON.
            cryptography.fernet.InvalidToken: If the encrypted data is invalid or tampered with.
        """
        return json.loads(self.fernet.decrypt(encrypted_data).decode("utf-8"))

    def set_password(self, password):
        """Sets a hashed password in secure storage.
        
        Args:
            password (str): The plain text password to be hashed and stored.
        
        Returns:
            None
        
        Raises:
            TypeError: If the password is not a string.
            ValueError: If the password is an empty string.
        """
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.secure_storage.add_or_update_item("app_password", hashed.decode())

    def verify_password(self, password):
        """Verifies if the provided password matches the stored password hash.
        
        Args:
            password (str): The password to be verified.
        
        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        stored_hash = self.secure_storage.get_item("app_password")
        if stored_hash:
            return bcrypt.checkpw(password.encode(), stored_hash.encode())
        return False

    def is_password_set(self):
        """Checks if a password is set in the secure storage.
        
        Returns:
            bool: True if a password is set, False otherwise.
        """
        return self.secure_storage.get_item("app_password") is not None
