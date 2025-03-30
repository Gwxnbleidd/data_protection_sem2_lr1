import os
import struct
import ecdsa
from ecdsa.keys import SigningKey


def get_users_key(username: str) -> str | None:
    """
    Функция проверяет наличие ключа username.sk и возвращает его. Если он не найдет, возвращает None

    :param username: Имя пользователя
    :return: Путь до ключа или None
    """
    for file in os.listdir('private_keys'):
        if file.startswith(username):
            return os.path.join('private_keys', file)
    return None


def create_user_keys(username: str):
    """
    Функция создает пару ключей для пользователя

    :param username: Имя пользователя
    """
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()

    with open(f'private_keys/{username}.sk', 'wb') as sk_file:
        sk_file.write(private_key.to_pem())
    with open(f'public_keys/{username}.pk', 'wb') as pk_file:
        pk_file.write(public_key.to_pem())


def load_private_key(private_key_path: str) -> SigningKey | None:
    """
    Функция загружает и возвращает приватный ключ, если его нет, возвращает None

    :param private_key_path: Путь к приватному ключу пользователя
    :return: Ключ или None
    """
    if os.path.exists(private_key_path):
        with open(private_key_path, 'rb') as sk_file:
            private_key = ecdsa.SigningKey.from_pem(sk_file.read())
        return private_key
    return None


class SignedDocument:
    def __init__(self, username: str, sign: bytes,  text: str):
        self.username_length = len(username)
        self.sign_length = len(sign)
        self.username = username
        self.sign = sign
        self.text = text

    def _save_as_file(self, file_path: str):
        with open(file_path, 'wb') as file:
            file.write(struct.pack('I', self.username_length))
            file.write(self.username.encode())
            file.write(struct.pack('I', self.sign_length))
            file.write(self.sign)
            file.write(self.text.encode())

    @staticmethod
    def _load_from_file(file_path: str):
        with open(file_path, 'rb') as file:
            username_length = struct.unpack('I', file.read(4))[0]
            username = file.read(username_length).decode()
            sign_length = struct.unpack('I', file.read(4))[0]
            sign = file.read(sign_length)
            text = file.read().decode()

        return SignedDocument(username, sign, text)
