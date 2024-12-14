from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .author import Author
    from .borrow import Borrow


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    quantity: Mapped[int]
    author: Mapped["Author"] = relationship(back_populates="books")
    borrows: Mapped[list["Borrow"]] = relationship(back_populates="book")
