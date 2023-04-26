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
