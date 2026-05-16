from __future__ import annotations

import base64
import hashlib
import hmac
import os

from app.db.models import User
from app.db.repositories import UserRepository
from app.utils.validators import validate_passwords, validate_required


PBKDF2_ITERATIONS = 260_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return "pbkdf2_sha256${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(digest_b64)
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


class AuthService:
    def __init__(self, users: UserRepository | None = None) -> None:
        self.users = users or UserRepository()

    def register(self, login: str, full_name: str, password: str, password_repeat: str) -> User:
        validate_required(login, "Логин не должен быть пустым")
        validate_required(full_name, "Имя пользователя не должно быть пустым")
        validate_required(password, "Пароль не должен быть пустым")
        validate_passwords(password, password_repeat)
        return self.users.create(login, full_name, hash_password(password))

    def authenticate(self, login: str, password: str) -> User | None:
        user = self.users.get_by_login(login)
        if user and verify_password(password, user.password_hash):
            return user
        return None

