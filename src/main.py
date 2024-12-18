import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from core import db_helper, settings
from api import router as api_router


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # startup
        yield
        # shutdown
        await db_helper.dispose()

    main_app = FastAPI(lifespan=lifespan)
    main_app.include_router(api_router)
    return main_app


main_app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run_config.host,
        port=settings.run_config.port,
        reload=settings.run_config.reload
    )
