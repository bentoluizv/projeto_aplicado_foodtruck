from typing import List

from sqlmodel import Field, Relationship

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.shared.model import BaseModel
from projeto_aplicado.utils import generate_locator


class Order(BaseModel, table=True):
    """
    Order model representing a customer order in the system.
    """

    status: str = Field(
        max_length=20, nullable=False, default=OrderStatus.PENDING
    )
    total: float = Field(nullable=False, gt=0.0, default=0.0)
    locator: str = Field(
        default_factory=generate_locator, index=True, nullable=False
    )
    notes: str | None = Field(default=None, nullable=True, max_length=255)
    products: List['OrderItem'] = Relationship(cascade_delete=True)
    rating: int | None = Field(default=None, nullable=True, ge=1, le=5)

    @classmethod
    def create(cls, dto: 'CreateOrderDTO'):  # type: ignore # noqa: F821
        """
        Create an Order instance from a DTO.
        """
        order = cls(**dto.model_dump())
        order.total = sum(item.calculate_total() for item in order.products)
        return order


class OrderItem(BaseModel, table=True):
    """
    OrderItem model representing an item in a customer order.
    """

    quantity: int = Field(nullable=False, gt=0)
    price: float = Field(nullable=False, gt=0.0)
    order_id: str = Field(
        foreign_key='order.id', nullable=False, ondelete='CASCADE'
    )
    product_id: str = Field(foreign_key='product.id', nullable=False)

    @classmethod
    def create(cls, dto: 'CreateOrderItemDTO'):  # type: ignore # noqa: F821
        """
        Create an OrderItem instance from a DTO.
        """
        return cls(**dto.model_dump())

    def calculate_total(self) -> float:
        return self.quantity * self.price
