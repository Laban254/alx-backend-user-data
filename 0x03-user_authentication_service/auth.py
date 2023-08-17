#!/usr/bin/env python3
""" Hash password """

import uuid
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """return encrypted password"""

    bytes_pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_pw, salt)
    return hashed


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation.
    This function is private to the auth module and should not
    be used outside of it.
    """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """validate login credentials"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf=8"), user.hashed_password)
