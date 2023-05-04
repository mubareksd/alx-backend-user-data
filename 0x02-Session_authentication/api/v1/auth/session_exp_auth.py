#!/usr/bin/env python3
"""
SessionExpAuth module for the API
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """_summary_
    """
    def __init__(self) -> None:
        """_summary_
        """
        try:
            duration = int(getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """_summary_

        Args:
            user_id (_type_, optional): _description_. Defaults to None.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
            }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """_summary_

        Args:
            session_id (_type_, optional): _description_. Defaults to None.
        """
        if session_id is None:
            return None
        user_details = self.user_id_by_session_id.get(session_id)
        if user_details is None:
            return None
        if 'created_at' not in user_details.keys():
            return None
        if self.session_duration <= 0:
            return user_details.get('user_id')
        created_at = user_details.get('created_at')
        allowed_window = created_at + timedelta(seconds=self.session_duration)
        if allowed_window < datetime.now():
            return None
        return user_details.get('user_id')
