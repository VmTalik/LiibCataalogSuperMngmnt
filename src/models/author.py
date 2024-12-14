from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book


class Author(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    surname: Mapped[str] = mapped_column(String(120))
    date_birth: Mapped[date]
    books: Mapped[list["Book"]] = relationship(back_populates="author")
