from typing import List
from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from schemas.book import BookReadForAuthor


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Имя")
    surname: str = Field(..., min_length=1, max_length=120, description="Фамилия")
    birth_date: date = Field(..., description="Дата рождения")


class AuthorCreate(AuthorBase):
    pass


class AuthorCreateResponse(AuthorBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int


class AuthorReadResponse(AuthorBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    books: List[BookReadForAuthor]


class AuthorUpdate(AuthorBase):
    pass


class AuthorUpdateResponse(AuthorCreateResponse):
    pass
