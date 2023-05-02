#!/usr/bin/env python3
"""
BasicAuth module for the API
"""
from api.v1.auth.auth import Auth


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
        if authorization_header is None or \
            type(authorization_header) is not str or \
                not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split()[1]
