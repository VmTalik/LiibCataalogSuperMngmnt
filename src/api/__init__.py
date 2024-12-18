from fastapi import APIRouter
from api.routes.authors import router as authors_router
from api.routes.books import router as books_router
from api.routes.borrows import router as borrows_router

router = APIRouter()
router.include_router(authors_router)
router.include_router(books_router)
router.include_router(borrows_router)
