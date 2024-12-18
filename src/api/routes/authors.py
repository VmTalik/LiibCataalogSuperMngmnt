from fastapi import APIRouter, status, Depends
from schemas import (
    AuthorCreate,
    AuthorCreateResponse,
    AuthorReadResponse,
    AuthorReadByIdResponse,
    AuthorUpdate,
    AuthorUpdateResponse
)
from crud import AuthorCRUDRepository
from api.dependencies import get_repository

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=AuthorCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_author(
        author_create: AuthorCreate,
        author_repo: AuthorCRUDRepository = Depends(get_repository(repo_type=AuthorCRUDRepository))
):
    return await author_repo.create_author(author_create=author_create)


@router.get("/", response_model=list[AuthorReadResponse], status_code=status.HTTP_200_OK)
async def get_authors_list(
        offset: int = 0,
        limit: int = 10,
        author_repo: AuthorCRUDRepository = Depends(get_repository(repo_type=AuthorCRUDRepository))
):
    return await author_repo.get_authors_list(offset=offset, limit=limit)


@router.get("/{id}", response_model=AuthorReadByIdResponse, status_code=status.HTTP_200_OK)
async def get_author_by_id(
        id: int,
        author_repo: AuthorCRUDRepository = Depends(get_repository(repo_type=AuthorCRUDRepository))
):
    return await author_repo.get_author_by_id(author_id=id)


@router.put("/{id}", response_model=AuthorUpdateResponse, status_code=status.HTTP_200_OK)
async def update_product(
        id: int,
        author_update: AuthorUpdate,
        author_repo: AuthorCRUDRepository = Depends(get_repository(repo_type=AuthorCRUDRepository))
):
    return await author_repo.update_author(author_id=id, author_update=author_update)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        id: int,
        author_repo: AuthorCRUDRepository = Depends(get_repository(repo_type=AuthorCRUDRepository))
):
    await author_repo.delete_author(author_id=id)
