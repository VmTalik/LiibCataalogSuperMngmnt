from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120, description="Название")
    description: str = Field(..., min_length=2, max_length=120, description="Описание")
    quantity: int = Field(..., ge=1, description="Количество доступных экземпляров")


class BookCreate(BookBase):
    author_id: int


class BookCreateResponse(BookBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int


class BookReadResponse(BookBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    author_id: int


class BookUpdate(BookBase):
    pass


class BookUpdateResponse(BookCreateResponse):
    pass


class BookReadForAuthor(BookBase):
    model_config = ConfigDict(
        from_attributes=True
    )
