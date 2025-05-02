from typing import Sequence

from sqlmodel import SQLModel

from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.schemas import Pagination


class CreateOrderItemDTO(SQLModel):
    quantity: int
    price: float
    order_id: str
    product_id: str


class UpdateOrderItemDTO(SQLModel):
    quantity: int | None = None
    price: float | None = None


class OrderItemList(SQLModel):
    order_itens: Sequence['OrderItem']
    pagination: Pagination


OrderItemList.model_rebuild()
