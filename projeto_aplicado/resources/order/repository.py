from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.order.schemas import UpdateOrderDTO
from projeto_aplicado.resources.shared.repository import BaseRepository


def get_order_repository(session: Annotated[Session, Depends(get_session)]):
    return OrderRepository(session)


class OrderRepository(BaseRepository[Order]):
    def __init__(self, session: Session):
        super().__init__(session, Order)

    def get_total_count(self) -> int:
        stmt = select(func.count()).select_from(Order)
        return self.session.exec(stmt).one()

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Order]:
        return super().get_all(offset=offset, limit=limit)

    def update(self, order: Order, dto: UpdateOrderDTO) -> Order:
        update_data = dto.model_dump(exclude_unset=True)
        return super().update(order, update_data)
