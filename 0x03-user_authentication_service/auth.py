#!/usr/bin/env python3
""" Hash password """

import bcrypt


def _hash_password(password: str) -> bytes:
    """return encrypted password"""

    bytes_pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_pw, salt)
    return hashed
