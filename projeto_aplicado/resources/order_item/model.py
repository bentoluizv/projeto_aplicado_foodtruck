from datetime import datetime

from sqlmodel import Field, SQLModel

from ...utils import get_ulid_as_str


class OrderItem(SQLModel, table=True):
    id: str = Field(default_factory=get_ulid_as_str, primary_key=True)
    created_at: str = Field(default_factory=datetime.now, nullable=False)
    quantity: int = Field(nullable=False, gt=0)
    price: float = Field(nullable=False, gt=0.0)
    order_id: str = Field(foreign_key='order.id', nullable=False)
    product_id: str = Field(foreign_key='product.id', nullable=False)

    @classmethod
    def create(cls, dto: 'CreateOrderItemDTO'):  # type: ignore # noqa: F821
        return cls(**dto.model_dump())

    def calculate_total(self) -> float:
        """
        Calculate the total price of the order item.
        """
        return self.quantity * self.price
