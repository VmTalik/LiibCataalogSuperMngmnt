from pydantic import BaseModel, ConfigDict, PositiveInt
from datetime import date
from .book import BookCreate


class BorrowBase(BaseModel):
    book_id: PositiveInt
    reader_name: str


class BorrowCreate(BorrowBase):
    pass


class BorrowCreateResponse(BorrowBase):
    id: int
    borrow_date: date


class BorrowReadResponse(BorrowCreateResponse):
    book: BookCreate


class BorrowUpdate(BaseModel):
    return_date: date


class BorrowUpdateResponse(BorrowCreateResponse):
    return_date: date
