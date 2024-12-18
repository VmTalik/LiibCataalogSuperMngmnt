from fastapi import APIRouter, status, Depends
from schemas import (
    BookCreate,
    BookCreateResponse,
    BookReadResponse,
    BookUpdate,
    BookUpdateResponse
)
from crud import BookCRUDRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=BookCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_book(
        book_create: BookCreate,
        book_repo: BookCRUDRepository = Depends(get_repository(repo_type=BookCRUDRepository))
):
    return await book_repo.create_book(book_create=book_create)


@router.get("/", response_model=list[BookReadResponse], status_code=status.HTTP_200_OK)
async def get_books_list(
        offset: int = 0,
        limit: int = 10,
        book_repo: BookCRUDRepository = Depends(get_repository(repo_type=BookCRUDRepository))
):
    return await book_repo.get_books_list(offset=offset, limit=limit)


@router.get("/{id}", response_model=BookReadResponse, status_code=status.HTTP_200_OK)
async def get_book_by_id(
        id: int,
        book_repo: BookCRUDRepository = Depends(get_repository(repo_type=BookCRUDRepository))
):
    return await book_repo.get_book_by_id(book_id=id)


@router.put("/{id}", response_model=BookUpdateResponse, status_code=status.HTTP_200_OK)
async def update_book(
        id: int,
        book_update: BookUpdate,
        book_repo: BookCRUDRepository = Depends(get_repository(repo_type=BookCRUDRepository))
):
    return await book_repo.update_book(book_id=id, book_update=book_update)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        id: int,
        book_repo: BookCRUDRepository = Depends(get_repository(repo_type=BookCRUDRepository))
):
    await book_repo.delete_book(book_id=id)
