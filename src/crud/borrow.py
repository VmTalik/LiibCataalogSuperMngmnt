from .base import BaseCRUDRepository
from models import Borrow, Book
from schemas import BorrowCreate, BorrowUpdate
from typing import Sequence
from sqlalchemy import select, Result, func
from fastapi import HTTPException
from sqlalchemy.orm import selectinload


class BorrowCRUDRepository(BaseCRUDRepository):
    async def create_borrow(self, borrow_create: BorrowCreate) -> Borrow:
        async with self.async_session.begin():
            # Получаем книгу с пессиместической блокировкой на обновление
            book_query = await self.async_session.execute(
                select(Book).where(Book.id == borrow_create.book_id).with_for_update()
            )
            book = book_query.scalar_one_or_none()
            if not book:
                raise HTTPException(status_code=400, detail="Нет такой книги в бибилотеке!")
            if book.quantity < 1:
                raise HTTPException(status_code=400, detail="Нет доступных экземпляров книг для выдачи!")
            book.quantity -= 1
            borrow = Borrow(**borrow_create.model_dump())
            self.async_session.add(borrow)
        await self.async_session.refresh(borrow)
        return borrow

    async def get_borrows_list(self, offset: int = 0, limit: int = 20) -> Sequence[Borrow]:
        stmt = select(Borrow).options(selectinload(Borrow.book)).offset(offset).limit(limit)
        result: Result = await self.async_session.execute(stmt)
        orders_list = result.scalars().all()
        return orders_list

    async def get_borrow_by_id(self, borrow_id: int) -> Borrow | None:
        stmt = select(Borrow).where(Borrow.id == borrow_id).options(selectinload(Borrow.book))
        result = await self.async_session.execute(stmt)
        borrow = result.scalar_one_or_none()
        if not borrow:
            raise HTTPException(status_code=404, detail="Выдача не найдена!")
        return borrow

    async def update_borrow_return_date(
            self,
            borrow_id: int,
            borrow_update: BorrowUpdate
    ) -> Borrow | None:
        async with self.async_session.begin():
            borrow = await self.async_session.get(Borrow, borrow_id)
            if not borrow:
                raise HTTPException(
                    status_code=404,
                    detail="Указание даты возврата невозможно, выдача не найдена!"
                )
            borrow_return_date = borrow_update.return_date
            if borrow_return_date is not None:
                borrow.return_date = borrow_return_date
            else:
                borrow.return_date = func.current_date()
            book_query = await self.async_session.execute(
                select(Book).where(Book.id == borrow.book_id).with_for_update()
            )
            book = book_query.scalar_one_or_none()
            book.quantity += 1
        return borrow
