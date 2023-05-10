#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from uuid import uuid4
from user import User


def _hash_password(password: str) -> bytes:
    """Method that takes in a password string arguments and returns bytes.

    Args:
        password (String): password to hash

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates uuid

    Returns:
        str: the generated uuid
    """
    return str(uuid4())


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

    def create_session(self, email: str) -> str:
        """method that create user session

        Args:
            email (str): user email

        Returns:
            str: session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[None, User]:
        """method that returns user using session id

        Args:
            session_id (str): session id

        Returns:
            Union[None, User]: user
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
