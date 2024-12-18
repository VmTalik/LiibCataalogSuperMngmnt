from pydantic import BaseModel, Field, PositiveInt


class BookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Название")
    description: str = Field(..., min_length=2, max_length=120, description="Описание")
    quantity: int = Field(..., ge=0, description="Количество доступных экземпляров")


class BookCreate(BookBase):
    author_id: PositiveInt


class BookCreateResponse(BookBase):
    id: int
    author_id: PositiveInt


class BookReadResponse(BookCreateResponse):
    pass


class BookUpdate(BookCreate):
    pass


class BookUpdateResponse(BookCreateResponse):
    author_id: int
