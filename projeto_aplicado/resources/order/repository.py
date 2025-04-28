from turtle import st
from typing import Annotated

from fastapi import Depends
from model import (
    Order,
)
from sqlmodel import Session, select

from projeto_aplicado.ext.database.db import get_session


class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, order: Order):
        try:
            self.session.add(order)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, order_id: str):
        try:
            order = self.session.get(Order, order_id)
            return order

        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100):
        try:
            stmt = select(Order).offset(offset).limit(limit)
            orders = self.session.exec(stmt).all()
            return orders

        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, order: Order, updated_data: dict):
        try:
            for key, value in updated_data.items():
                setattr(order, key, value)

            self.session.commit()
            self.session.refresh(order)

            return order.id

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, order: Order):
        try:
            self.session.delete(order)
            self.session.commit()
            return order.id

        except Exception as e:
            self.session.rollback()
            raise e


def get_order_repository(
    session: Annotated[Session, Depends(get_session)],
):
    """
    Dependency to get the OrderRepository.
    """
    return OrderRepository(session)
