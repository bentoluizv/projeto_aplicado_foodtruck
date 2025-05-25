from typing import Optional, Sequence

from pydantic import Field, field_validator
from sqlmodel import SQLModel

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.shared.schemas import Pagination


class CreateOrderItemDTO(SQLModel):
    """
    Data transfer object for creating an order item.
    """

    quantity: int = Field(gt=0)
    product_id: str
    price: float = Field(gt=0.0)


class UpdateOrderDTO(SQLModel):
    """
    Data transfer object for updating an order.
    """

    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class CreateOrderDTO(SQLModel):
    """
    Data transfer object for creating an order.
    """

    items: list[CreateOrderItemDTO]
    notes: Optional[str] = None

    @field_validator('items')
    @classmethod
    def validate_items_not_empty(
        cls, items: list[CreateOrderItemDTO]
    ) -> list[CreateOrderItemDTO]:
        if not items:
            raise ValueError('Order must have at least one item')
        return items


CreateOrderDTO.model_rebuild()


class OrderList(SQLModel):
    """
    Response model for listing orders with pagination.
    """

    orders: Sequence[Order]
    pagination: Pagination


OrderList.model_rebuild()


class UpdateOrderItemDTO(SQLModel):
    """
    Data transfer object for updating an order item.
    """

    quantity: int | None = None
    price: float | None = None


class OrderItemList(SQLModel):
    """
    Response model for listing order items with pagination.
    """

    order_items: Sequence[OrderItem]
    pagination: Pagination


OrderItemList.model_rebuild()
