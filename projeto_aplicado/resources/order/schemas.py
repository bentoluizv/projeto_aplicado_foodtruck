from typing import Optional, Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.schemas import Pagination


class UpdateOrderDTO(SQLModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class CreateOrderDTO(SQLModel):
    customer_id: str
    items: list[OrderItem]
    notes: Optional[str] = None


class OrderList(SQLModel):
    orders: Sequence[Order]
    pagination: Pagination
