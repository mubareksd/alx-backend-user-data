#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password):
    """Method that takes in a password string arguments and returns bytes.

    Args:
        password (String): password to hash

    Returns:
        bytes: hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
