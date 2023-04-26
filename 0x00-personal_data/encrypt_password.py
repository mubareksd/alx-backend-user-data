#!/usr/bin/env python3
"""encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt_password function that expects one string argument name password

    Args:
        password (str): string to encrypt

    Returns:
        bytes: salted hashed password, which is a byte string
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid function that expects 2 arguments and returns a boolean

    Args:
        hashed_password (bytes): salted hashed password
        password (str): string to check

    Returns:
        bool: True if the password is valid, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
