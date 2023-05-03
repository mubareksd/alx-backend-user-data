#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """_summary_
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """_summary_

        Args:
            path (str): _description_
            excluded_paths (List[str]): _description_

        Returns:
            bool: _description_
        """
        if excluded_paths is not None:
            for excluded in excluded_paths:
                if excluded.startswith(path):
                    return False
                if path.startswith(excluded):
                    return False
                if excluded[-1] == '*':
                    if path.startswith(excluded[:-1]):
                        return False

        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """_summary_

        Args:
            request (_type_, optional): _description_. Defaults to None.

        Returns:
            str: _description_
        """
        if request is None or 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        return None
