from typing import Optional, Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.schemas import Pagination


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

    customer_id: str
    items: list[OrderItem]
    notes: str | None = None


CreateOrderDTO.model_rebuild()


class OrderList(SQLModel):
    """
    Response model for listing orders with pagination.
    """

    orders: Sequence[Order]
    pagination: Pagination


OrderList.model_rebuild()
