from datetime import datetime
from typing import Optional, Sequence

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from projeto_aplicado.resources.shared.schemas import (
    BaseListResponse,
    BaseUserModel,
)
from projeto_aplicado.resources.users.model import UserRole


class CreateUserDTO(SQLModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole


class UpdateUserDTO(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6)
    role: Optional[UserRole] = None


class UserOut(BaseUserModel):
    role: UserRole


class UserList(BaseListResponse[UserOut]):
    items: Sequence[UserOut] = Field(alias='users')

    class Config:
        populate_by_name = True


class PublicUser(SQLModel):
    id: str
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
