from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from ...utils import get_ulid_as_str


class OrderItem(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    created_at: str = Field(default_factory=datetime.now, nullable=False)
    quantity: int = Field(nullable=False, gt=0)
    price: float = Field(nullable=False, gt=0.0)
    order_id: str = Field(foreign_key='order.id', nullable=False)
    order: 'Order' = Relationship(back_populates='products')  # type: ignore # noqa: F821
    product_id: str = Field(foreign_key='product.id', nullable=False)
    product: 'Product' = Relationship(back_populates='order_items')  # type: ignore # noqa: F821

    @classmethod
    def create(cls, dto: 'CreateOrderItemDTO'):  # type: ignore # noqa: F821
        return cls(**dto.model_dump())

    def calculate_total(self) -> float:
        """
        Calculate the total price of the order item.
        """
        return self.quantity * self.price


OrderItem.model_rebuild()
