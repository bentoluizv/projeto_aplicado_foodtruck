from enum import Enum
from typing import Optional

from sqlmodel import SQLModel

from projeto_aplicado.resources.order_item.model import OrderItem


class OrderStatus(str, Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class UpdateOrderDTO(SQLModel):
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None


class CreateOrderDTO(SQLModel):
    customer_id: str
    itens: list[OrderItem]
    notes: Optional[str] = None
