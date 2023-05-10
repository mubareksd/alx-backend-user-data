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

    def valid_login(self, email: str, password: str) -> bool:
        """method that validates user credentials

        Args:
            email (str): email of the user
            password (str): password of the user

        Returns:
            bool: true if the email and password are found in the db else false
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except NoResultFound:
            return False
