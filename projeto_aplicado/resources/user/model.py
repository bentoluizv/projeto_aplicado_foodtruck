from enum import Enum
from typing import Optional

from sqlmodel import Field

from projeto_aplicado.resources.shared.model import BaseModel


class UserRole(str, Enum):
    KITCHEN = 'kitchen'
    ATTENDANT = 'attendant'
    ADMIN = 'admin'


class User(BaseModel, table=True):
    """
    User model representing a user in the system.
    """

    username: str = Field(
        nullable=False, unique=True, max_length=20, index=True
    )
    email: str = Field(nullable=False, unique=True, max_length=255, index=True)
    password: str = Field(nullable=False, max_length=255)
    full_name: Optional[str] = Field(max_length=100, nullable=True)
    role: UserRole = Field(nullable=False)
