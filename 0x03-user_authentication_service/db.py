#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Method that saves a new user to the database.

        Args:
            email (String): email of the user
            hashed_password (String): hashed password of the user

        Returns:
            user (User): the user created
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Method that finds a user in the database.

        Args:
            kwargs (dict): arguments to search for a user

        Returns:
            User: the user found
        """
        users = self._session.query(User)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in users:
                if getattr(user, key) == value:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """Method that updates a user in the database.

        Args:
            user_id (int): user id to update
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()
