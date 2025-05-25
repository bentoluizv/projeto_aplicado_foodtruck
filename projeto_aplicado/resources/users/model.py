from enum import Enum

from sqlmodel import Field

from projeto_aplicado.resources.shared.model import BaseModel


class UserRole(str, Enum):
    KITCHEN = 'kitchen'
    ATTENDANT = 'attendant'


class User(BaseModel, table=True):
    """
    User model representing a user in the system.
    """

    name: str = Field(nullable=False, max_length=100)
    email: str = Field(nullable=False, unique=True, max_length=255, index=True)
    password: str = Field(nullable=False, max_length=255)
    role: UserRole = Field(nullable=False)
