from .base import BaseCRUDRepository
from models import Author
from schemas import AuthorCreate, AuthorUpdate
from sqlalchemy import select, Result
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


class AuthorCRUDRepository(BaseCRUDRepository):
    async def create_author(self, author_create: AuthorCreate) -> Author:
        author = Author(**author_create.model_dump())
        self.async_session.add(author)
        await self.async_session.commit()
        await self.async_session.refresh(author)
        return author

    async def get_authors_list(self, offset: int = 0, limit: int = 10):
        stmt = select(Author).offset(offset).limit(limit)
        result: Result = await self.async_session.execute(stmt)
        authors_list = result.scalars().all()
        return authors_list

    async def get_author_by_id(self, author_id: int) -> Author | None:
        stmt = select(Author).where(Author.id == author_id).options(selectinload(Author.books))
        result = await self.async_session.execute(stmt)
        author = result.scalar_one_or_none()
        if not author:
            raise HTTPException(status_code=404, detail="Автор не найден!")
        return author

    async def update_author(self, author_id, author_update: AuthorUpdate) -> Author | None:
        author = await self.async_session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Обновление невозможно, автор не найден!")
        for name, value in author_update.model_dump().items():
            setattr(author, name, value)
        await self.async_session.commit()
        return author

    async def delete_author(self, author_id) -> None:
        author = await self.async_session.get(Author, author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Удаление невозможно, автор не найден!")
        await self.async_session.delete(author)
        await self.async_session.commit()
