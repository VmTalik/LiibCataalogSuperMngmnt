from typing import Type, Callable
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import db_helper
from crud import BaseCRUDRepository


def get_repository(
        repo_type: Type[BaseCRUDRepository],
) -> Callable[[AsyncSession], BaseCRUDRepository]:
    def _get_repo(
            async_session: AsyncSession = Depends(db_helper.session_getter),
    ) -> BaseCRUDRepository:
        return repo_type(async_session=async_session)

    return _get_repo
