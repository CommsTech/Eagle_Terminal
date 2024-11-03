import json

import bcrypt
from cryptography.fernet import Fernet

from utils.logger import EagleTerminalException, logger
from utils.secure_storage import SecureStorage


class UserAuth:
    def __init__(self, users_file="users.json", key_file="secret.key"):
        self.users_file = users_file
        self.key_file = key_file
        self.users = self.load_users()
        self.fernet = self.load_or_create_key()
        self.secure_storage = SecureStorage()

    def load_or_create_key(self):
        try:
            with open(self.key_file, "rb") as file:
                key = file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as file:
                file.write(key)
        return Fernet(key)

    def load_users(self):
        try:
            with open(self.users_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(self.users_file, "w") as file:
            json.dump(self.users, file)

    def register_user(self, username, password):
        if username in self.users:
            raise EagleTerminalException("Username already exists")
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.users[username] = hashed.decode("utf-8")
        self.save_users()

    def authenticate_user(self, username, password):
        if username not in self.users:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"), self.users[username].encode("utf-8")
        )

    def encrypt_data(self, data):
        return self.fernet.encrypt(json.dumps(data).encode("utf-8"))

    def decrypt_data(self, encrypted_data):
        return json.loads(self.fernet.decrypt(encrypted_data).decode("utf-8"))

    def set_password(self, password):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.secure_storage.add_or_update_item("app_password", hashed.decode())

    def verify_password(self, password):
        stored_hash = self.secure_storage.get_item("app_password")
        if stored_hash:
            return bcrypt.checkpw(password.encode(), stored_hash.encode())
        return False

    def is_password_set(self):
        return self.secure_storage.get_item("app_password") is not None
