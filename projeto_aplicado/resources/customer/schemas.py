from typing import Sequence

from pydantic import EmailStr
from sqlmodel import SQLModel

from projeto_aplicado.resources.customer.model import Customer
from projeto_aplicado.schemas import Pagination


class CreateCustomerDTO(SQLModel):
    """
    Data transfer object for creating a customer.
    """

    name: str
    email: EmailStr


class UpdateCustomerDTO(SQLModel):
    """
    Data transfer object for updating a customer.
    """

    name: str | None = None
    email: EmailStr | None = None


class CustomerList(SQLModel):
    """
    Response model for listing customers with pagination.
    """

    customers: Sequence[Customer]
    pagination: Pagination
