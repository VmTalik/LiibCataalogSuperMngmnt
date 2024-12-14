from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, func
from .base import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .book import Book


class Borrow(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    reader_name: Mapped[str] = mapped_column(String(120))
    borrow_date: Mapped[date] = mapped_column(server_default=func.current_date())
    return_date: Mapped[date]
    book: Mapped["Book"] = relationship(back_populates="borrows")
