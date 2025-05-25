from datetime import datetime
from typing import Generic, Sequence, TypeVar

from pydantic import EmailStr
from sqlmodel import SQLModel

T = TypeVar('T')


class BaseResponse(SQLModel):
    id: str
    action: str


class Pagination(SQLModel):
    offset: int
    limit: int
    total_count: int
    total_pages: int
    page: int

    @classmethod
    def create(cls, offset: int, limit: int, total_count: int) -> 'Pagination':
        return cls(
            offset=offset,
            limit=limit,
            total_count=total_count,
            total_pages=(total_count + limit - 1) // limit,
            page=offset // limit + 1,
        )


class BaseListResponse(SQLModel, Generic[T]):
    items: Sequence[T]
    pagination: Pagination

    class Config:
        populate_by_name = True


class BaseModel(SQLModel):
    id: str
    created_at: datetime
    updated_at: datetime


class BaseUserModel(BaseModel):
    name: str
    email: EmailStr


class Icon(SQLModel):
    id: str
    icon: str
    url: str


class IconsResponse(SQLModel):
    icons: list[Icon]
