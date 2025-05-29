from datetime import datetime
from typing import Optional, Sequence

from pydantic import EmailStr, Field, field_validator
from sqlmodel import SQLModel

from projeto_aplicado.auth.password import get_password_hash
from projeto_aplicado.resources.shared.schemas import (
    BaseListResponse,
)
from projeto_aplicado.resources.user.model import UserRole


class PasswordHashMixin:
    @field_validator('password', mode='after')
    def hash_password(cls, v):
        if v:
            return get_password_hash(v)
        return v


class CreateUserDTO(SQLModel, PasswordHashMixin):
    username: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: UserRole
    full_name: Optional[str] = None


class UpdateUserDTO(SQLModel, PasswordHashMixin):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=6)
    role: Optional[UserRole] = None


class UserOut(SQLModel):
    id: str
    username: str
    full_name: Optional[str]
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime


class UserList(BaseListResponse[UserOut]):
    items: Sequence[UserOut] = Field(alias='users')

    class Config:
        populate_by_name = True
