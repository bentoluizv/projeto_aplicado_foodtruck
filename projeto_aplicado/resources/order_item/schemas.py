from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.schemas import Pagination


class CreateOrderItemDTO(SQLModel):
    """
    Data transfer object for creating an order item.
    """

    quantity: int
    price: float
    order_id: str
    product_id: str


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
