import json
import os

from cryptography.fernet import Fernet


class SecureStorage:
    def __init__(self):
        """Initialize the SecureStorage object.
        
        This method initializes a SecureStorage object by loading or generating an encryption key,
        creating a Fernet instance for encryption/decryption, and setting the storage file path.
        
        Args:
            None
        
        Returns:
            None
        
        Attributes:
            key (bytes): The encryption key used for secure storage.
            fernet (Fernet): Fernet instance for encryption and decryption.
            storage_file (str): The file path for storing encrypted data.
        """
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)
        self.storage_file = "secure_storage.enc"

    def load_or_generate_key(self):
        """Loads an existing encryption key from a file or generates a new one if the file doesn't exist.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            bytes: The encryption key, either loaded from the file or newly generated.
        
        Raises:
            IOError: If there are issues reading from or writing to the key file.
        """
        key_file = "secure_storage.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as file:
                return file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as file:
                file.write(key)
            return key

    def save_data(self, data):
        """Saves encrypted data to a file.
        
        Args:
            data (Any): The data to be encrypted and saved. Can be any JSON-serializable object.
        
        Returns:
            None
        
        Raises:
            JSONEncodeError: If the data cannot be serialized to JSON.
            IOError: If there's an error writing to the file.
        """
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.storage_file, "wb") as file:
            file.write(encrypted_data)

    def load_data(self):
        """Loads encrypted data from a file and decrypts it.
        
        Args:
            self: The instance of the class containing this method.
        
        Returns:
            dict: A dictionary containing the decrypted data if the file exists and can be decrypted successfully. Returns an empty dictionary if the file does not exist.
        
        Raises:
            cryptography.fernet.InvalidToken: If the encryption key is invalid or the data is corrupted.
            json.JSONDecodeError: If the decrypted data is not valid JSON.
        """
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        return {}

    def add_or_update_item(self, key, value):
        """Adds a new item or updates an existing item in the data store.
        
        Args:
            key (Any): The key of the item to add or update.
            value (Any): The value to associate with the key.
        
        Returns:
            None: This method doesn't return anything.
        """
        data = self.load_data()
        data[key] = value
        self.save_data(data)

    def get_item(self, key):
        """Retrieves an item from the loaded data using the provided key.
        
        Args:
            key (Any): The key to look up in the loaded data.
        
        Returns:
            Any: The value associated with the given key, or None if the key is not found.
        """
        data = self.load_data()
        return data.get(key)

    def delete_item(self, key):
        """Deletes an item from the data storage using the provided key.
        
        Args:
            key (Any): The key of the item to be deleted from the data storage.
        
        Returns:
            None: This method doesn't return anything.
        
        Raises:
            KeyError: If the specified key is not found in the data storage.
        """
        data = self.load_data()
        if key in data:
            del data[key]
            self.save_data(data)
