from sqlmodel import SQLModel


class CreateCategoryDTO(SQLModel):
    name: str


class UpdateCategoryDTO(SQLModel):
    name: str | None = None


class CreateItemDTO(SQLModel):
    name: str
    price: float
    category_id: str


class UpdateItemDTO(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image: bytes | None = None
    category_id: str | None = None


class BaseResponse(SQLModel):
    id: str
    action: str
