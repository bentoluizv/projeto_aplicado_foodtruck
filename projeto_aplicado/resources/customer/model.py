from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from projeto_aplicado.utils import get_ulid_as_str


class Customer(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    name: str = Field(index=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)

    @classmethod
    def create(cls, dto: 'CreateCustomerDTO'):  # type: ignore # noqa: F821
        return cls(**dto.model_dump())  # type: ignore
