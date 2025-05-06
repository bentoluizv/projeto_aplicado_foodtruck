from datetime import datetime
from typing import List, Self

from pydantic import model_validator
from sqlmodel import Field, Relationship, SQLModel

from ...utils import generate_locator, get_ulid_as_str
from .enums import OrderStatus


class Order(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    created_at: str = Field(default_factory=datetime.now, nullable=False)
    locator: str = Field(
        default_factory=generate_locator, index=True, nullable=False
    )
    status: OrderStatus = Field(nullable=False, default=OrderStatus.PENDING)
    total: float = Field(nullable=False, default=0.0, gt=0)
    notes: str | None = Field(default=None, nullable=True, max_length=255)
    customer_id: str = Field(foreign_key='customer.id', nullable=False)
    products: List['OrderItem'] = Relationship()  # type: ignore # noqa: F821

    @classmethod
    def create(cls, dto: 'CreateOrderDTO'):  # type: ignore # noqa: F821
        return cls(**dto.model_dump())

    @model_validator(mode='after')
    def calculate_total(self) -> Self:
        total = sum(product.calculate_total() for product in self.products)
        self.total = total
        return self
