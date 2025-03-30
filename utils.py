import os

import ecdsa


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


class SignedDocument:
    # Длина имени подписывающего пользователя
    # Длина подписи
    # Имя подписывающего пользователя
    # Электронная подпись
    # Текст документа
    def __init__(self, username: str, sign: bytes,  text: str):
        self.username = username
        self.username_length = len(username)
        self.sign = sign
        self.text = text


class Signature:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.public_key = self.private_key.get_verifying_key()
