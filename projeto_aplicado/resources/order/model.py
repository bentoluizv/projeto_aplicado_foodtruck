from datetime import datetime
from typing import List, Self

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel

from ...utils import generate_locator, get_ulid_as_str
from .enums import OrderStatus


class Order(SQLModel, table=True):
    """
    Order model representing a customer order in the system.
    """

    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    customer_id: str = Field(foreign_key='customer.id', nullable=False)
    status: str = Field(max_length=20, nullable=False)
    total: float = Field(nullable=False, gt=0.0)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    locator: str = Field(
        default_factory=generate_locator, index=True, nullable=False
    )
    notes: str | None = Field(default=None, nullable=True, max_length=255)
    products: List['OrderItem'] = Relationship()  # type: ignore # noqa: F821

    @classmethod
    def create(cls, dto: 'CreateOrderDTO'):  # type: ignore  # noqa: F821
        """
        Create an Order instance from a DTO.
        """
        return cls(**dto.model_dump())

    @model_validator(mode='after')
    def calculate_total(self) -> Self:
        total = sum(product.calculate_total() for product in self.products)
        self.total = total
        return self
