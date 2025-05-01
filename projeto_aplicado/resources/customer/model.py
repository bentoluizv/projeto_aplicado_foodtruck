from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Customer(SQLModel, table=True):
    id: Optional[str] = Field(
        default_factory=get_ulid_as_str, primary_key=True
    )
    name: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)
    orders: list['Order'] = Relationship(back_populates='customer')  # type: ignore # noqa: F821
