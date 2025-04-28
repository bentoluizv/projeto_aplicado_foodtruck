from sqlmodel import SQLModel


class CreateOrderItemDTO(SQLModel):
    quantity: int
    price: float
    order_id: str
    product_id: str
