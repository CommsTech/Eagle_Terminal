import os

from cryptography.fernet import Fernet

KEY_FILE = "secret.key"


def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)


def load_key():
    return open(KEY_FILE, "rb").read()


def encrypt_data(data):
    generate_key()
    key = load_key()
    f = Fernet(key)
    return f.encrypt(data.encode())


def decrypt_data(encrypted_data):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()


def encrypt_password(password):
    generate_key()
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password


def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password)
    return decrypted_password.decode()
