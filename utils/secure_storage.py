import json
import os

from cryptography.fernet import Fernet


class SecureStorage:
    def __init__(self):
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)
        self.storage_file = "secure_storage.enc"

    def load_or_generate_key(self):
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
        encrypted_data = self.fernet.encrypt(json.dumps(data).encode())
        with open(self.storage_file, "wb") as file:
            file.write(encrypted_data)

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "rb") as file:
                encrypted_data = file.read()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return json.loads(decrypted_data)
        return {}

    def add_or_update_item(self, key, value):
        data = self.load_data()
        data[key] = value
        self.save_data(data)

    def get_item(self, key):
        data = self.load_data()
        return data.get(key)

    def delete_item(self, key):
        data = self.load_data()
        if key in data:
            del data[key]
            self.save_data(data)
