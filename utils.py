import os
import struct

import ecdsa
from ecdsa.keys import SigningKey, VerifyingKey


def get_private_key(username: str) -> str | None:
    """
    Функция проверяет наличие ключа username.sk и возвращает его. Если он не найдет, возвращает None

    :param username: Имя пользователя
    :return: Путь до ключа или None
    """
    for file in os.listdir('private_keys'):
        if file.startswith(username):
            return os.path.join('private_keys', file)
    return None


def get_public_key(username: str) -> str | None:
    """
    Функция проверяет наличие ключа username.pk и возвращает его. Если он не найдет, возвращает None

    :param username: Имя пользователя
    :return: Путь до ключа или None
    """
    for file in os.listdir('public_keys'):
        if file.startswith(username):
            return os.path.join('public_keys', file)
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


def load_public_key(public_key_path: str) -> VerifyingKey | None:
    """
    Функция загружает и возвращает открытый ключ, если его нет, возвращает None

    :param public_key_path: Путь к открытому ключу пользователя
    :return: Ключ или None
    """
    if os.path.exists(public_key_path):
        with open(public_key_path, 'rb') as pk_file:
            public_key = ecdsa.VerifyingKey.from_pem(pk_file.read())
        return public_key
    return None


class SignedDocument:
    def __init__(self, username: str, sign: bytes, text: str, username_length: str = None, sign_length: str = None):
        self.username = username
        self.sign = sign
        self.text = text
        self.username_length = str(len(username))
        self.sign_length = str(len(sign))

    def _save_as_file(self, file_path: str):
        separator = b'|||'
        bytes_values = [str(item).encode('utf-8') if not isinstance(item, bytes) else item for item in
                        [self.username, self.text, self.username_length, self.sign_length]]
        bytes_values.append(self.sign)

        with open(file_path, 'wb') as f:
            f.write(separator.join(bytes_values))

    @staticmethod
    def _load_from_file(file_path: str):
        separator = b'|||'
        with open(file_path, 'rb') as f:
            bytes_values = f.read()

        username, text, username_length, sign_length = map(
            lambda x: x.decode('utf-8'), bytes_values.split(separator)[:-1]
        )
        sign = bytes_values.split(separator)[-1]

        return SignedDocument(username=username, sign=sign, text=text, username_length=username_length,
                              sign_length=sign_length)

