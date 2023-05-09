#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Method that takes in a password string arguments and returns bytes.

    Args:
        password (String): password to hash

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """method that takes in email and password
        as arguments and returns a User object.

        Args:
            email (string): email of the user
            password (string): password of the user

        Raises:
            ValueError: if the user already exists

        Returns:
            User: the user created
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
