from typing import TypeVar

from pydantic.generics import BaseModel


_T = TypeVar("_T")
_MT = TypeVar("_MT", bound=str)


class NoContentResponse(BaseModel):
    message: str
