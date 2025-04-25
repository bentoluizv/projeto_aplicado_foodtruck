from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from projeto_aplicado.resources.order.schemas import OrderStatus

from ...data.utils import get_ulid_as_str


class Order(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    created_at: str = Field(default_factory=datetime.now, nullable=False)
    locator: str = Field(index=True, nullable=False)
    customer: str = Field(index=True, nullable=False)
    status: OrderStatus = Field(nullable=False, default=OrderStatus.PENDING)
    total: float = Field(nullable=False, default=0.0)
    products: list['OrderItem'] = Relationship(back_populates='order')


from projeto_aplicado.resources.order_item.model import OrderItem  # noqa: E402

Order.model_rebuild()
