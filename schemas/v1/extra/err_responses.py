from typing import Literal

from fastapi import status

from pydantic import BaseModel

from utils.schema_errors import HTTPExceptionWrapper


class Exceptions:
    class UserNotFound(HTTPExceptionWrapper):
        __status_code__ = status.HTTP_404_NOT_FOUND
        __detail__ = 'user not found'


class Schemas:
    class UserNotFound(BaseModel):
        detail: Literal['user not found']

