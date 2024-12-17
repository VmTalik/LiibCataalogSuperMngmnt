from typing import List

from pydantic import BaseModel, Field
from datetime import date
from .book import BookCreateResponse


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Имя")
    surname: str = Field(..., min_length=1, max_length=120, description="Фамилия")
    date_birth: date = Field(..., description="Дата рождения")


class AuthorCreate(AuthorBase):
    pass


class AuthorCreateResponse(AuthorBase):
    id: int


class AuthorReadResponse(AuthorCreateResponse):
    pass


class AuthorReadByIdResponse(AuthorCreateResponse):
    books: List[BookCreateResponse]


class AuthorUpdate(AuthorBase):
    pass


class AuthorUpdateResponse(AuthorCreateResponse):
    pass
