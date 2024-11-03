import os

import bcrypt
from cryptography.fernet import Fernet


class PasswordManager:
    def __init__(self):
        self.key = self.load_or_generate_key()
        self.fernet = Fernet(self.key)

    def load_or_generate_key(self):
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
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def verify_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)

    def encrypt_password(self, password):
        return self.fernet.encrypt(password.encode())

    def decrypt_password(self, encrypted_password):
        return self.fernet.decrypt(encrypted_password).decode()
