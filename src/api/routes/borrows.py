from fastapi import APIRouter, status, Depends
from schemas import (
    BorrowCreate,
    BorrowCreateResponse,
    BorrowReadResponse,
    BorrowUpdate,
    BorrowUpdateResponse
)
from crud import BorrowCRUDRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/borrows", tags=["Borrows"])


@router.post("/", response_model=BorrowCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_borrow(
        borrow_create: BorrowCreate,
        borrow_repo: BorrowCRUDRepository = Depends(get_repository(repo_type=BorrowCRUDRepository))
):
    return await borrow_repo.create_borrow(borrow_create=borrow_create)


@router.get("/", response_model=list[BorrowReadResponse], status_code=status.HTTP_200_OK)
async def get_borrows_list(
        offset: int = 0,
        limit: int = 20,
        borrow_repo: BorrowCRUDRepository = Depends(get_repository(repo_type=BorrowCRUDRepository))
):
    return await borrow_repo.get_borrows_list(offset=offset, limit=limit)


@router.get("/{id}", response_model=BorrowReadResponse, status_code=status.HTTP_200_OK)
async def get_borrow_by_id(
        id: int,
        borrow_repo: BorrowCRUDRepository = Depends(get_repository(repo_type=BorrowCRUDRepository))
):
    return await borrow_repo.get_borrow_by_id(borrow_id=id)


@router.patch("/{id}", response_model=BorrowUpdateResponse, status_code=status.HTTP_200_OK)
async def update_borrow_return_date(
        id: int,
        borrow_update: BorrowUpdate,
        borrow_repo: BorrowCRUDRepository = Depends(get_repository(repo_type=BorrowCRUDRepository))

):
    return await borrow_repo.update_borrow_return_date(borrow_id=id, borrow_update=borrow_update)
