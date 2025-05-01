from sqlmodel import SQLModel


class Pagination(SQLModel):
    offset: int
    limit: int
    total_count: int
    page: int
    total_pages: int


class CreateProductDTO(SQLModel):
    name: str
    price: float
    img_url: str
    description: str | None = None
    category_id: str


class UpdateProductDTO(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image: bytes | None = None
    category_id: str | None = None


class BaseResponse(SQLModel):
    id: str
    action: str


class Icon(SQLModel):
    id: str
    icon: str
    url: str


class IconsResponse(SQLModel):
    icons: list[Icon]
