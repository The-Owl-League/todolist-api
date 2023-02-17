from typing import NewType

from hashlib import sha256

HashedPassword = NewType("HashedPassword", str)


def hash_password(password: str) -> HashedPassword:
    return HashedPassword(sha256(password.encode('utf-8')).hexdigest())
