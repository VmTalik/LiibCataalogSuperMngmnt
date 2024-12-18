from .base import BaseCRUDRepository
from models import Book, Author
from schemas import BookCreate, BookUpdate
from sqlalchemy import select, Result
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


class BookCRUDRepository(BaseCRUDRepository):
    async def create_book(self, book_create: BookCreate) -> Book:
        author = await self.async_session.get(Author, book_create.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Автор с таким id не найден. Добавление книги невозможно!")
        book = Book(**book_create.model_dump())
        self.async_session.add(book)
        await self.async_session.commit()
        await self.async_session.refresh(book)
        return book

    async def get_books_list(self, offset: int = 0, limit: int = 10):
        stmt = select(Book).offset(offset).limit(limit)
        result: Result = await self.async_session.execute(stmt)
        books_list = result.scalars().all()
        return books_list

    async def get_book_by_id(self, book_id: int) -> Book | None:
        stmt = select(Book).where(Book.id == book_id).options(selectinload(Book.borrows))
        result = await self.async_session.execute(stmt)
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена!")
        return book

    async def update_book(self, book_id, book_update: BookUpdate) -> Book | None:
        book = await self.async_session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Обновление невозможно, книга не найдена!")
        author = await self.async_session.get(Author, book_update.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Автор с таким id не найден. Обновление книги невозможно!")
        for name, value in book_update.model_dump().items():
            setattr(book, name, value)
        await self.async_session.commit()
        return book

    async def delete_book(self, book_id) -> None:
        book = await self.async_session.get(Book, book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Удаление невозможно, книга не найдена!")
        await self.async_session.delete(book)
        await self.async_session.commit()
