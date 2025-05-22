from sqlmodel import SQLModel


class Pagination(SQLModel):
    offset: int
    limit: int
    total_count: int
    page: int
    total_pages: int


class BaseResponse(SQLModel):
    id: str
    action: str


class Icon(SQLModel):
    id: str
    icon: str
    url: str


class IconsResponse(SQLModel):
    icons: list[Icon]
