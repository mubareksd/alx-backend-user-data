#!/usr/bin/env python3
"""
BasicAuth module for the API
"""
import base64
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """_summary_
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """_summary_

        Args:
            authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """_summary_

        Args:
            base64_authorization_header (str): _description_

        Returns:
            str: _description_
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(decoded)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """_summary_

        Args:
            self (_type_): _description_
            str (_type_): _description_

        Returns:
            _type_: _description_
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':', 1)[0]
        password = decoded_base64_authorization_header.split(':', 1)[1]
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """_summary_

        Args:
            self (_type_): _description_
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """_summary_
        """
        header = self.authorization_header(request)
        if header:
            token = self.extract_base64_authorization_header(header)
            if token:
                decoded = self.decode_base64_authorization_header(token)
                if decoded:
                    email, pwd = self.extract_user_credentials(decoded)
                    if email and pwd:
                        return self.user_object_from_credentials(email, pwd)
        return None
