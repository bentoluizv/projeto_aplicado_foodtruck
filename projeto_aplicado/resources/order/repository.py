from datetime import datetime
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.schemas import OrderList, UpdateOrderDTO
from projeto_aplicado.resources.shared.schemas import Pagination

from .model import (
    Order,
)


class OrderRepository:
    """
    Repository for Order model.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        Args:
            session (Session): The database session to use.
        """
        self.session = session

    def create(self, order: Order):
        """
        Create a new order.
        Args:
            order (Order): The order to create.
        Returns:
            str: The ID of the created order.
        """
        try:
            self.session.add(order)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, order_id: str):
        """
        Get an order by ID.
        Args:
            order_id (str): The ID of the order to retrieve.
        Returns:
            Order: The order with the specified ID.
        """
        try:
            order = self.session.get(Order, order_id)
            return order

        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100):
        """
        Get all orders with default pagination.
        Args:
            offset (int): The offset for pagination.
            limit (int): The maximum number of orders to retrieve.
        Returns:
            OrderList: A list of orders with pagination information.
        """
        try:
            total_count_stmt = select(func.count()).select_from(Order)
            total_count = self.session.exec(total_count_stmt).first()

            if not total_count:
                total_count = 0

            stmt = select(Order).offset(offset).limit(limit)
            orders = self.session.exec(stmt).all()

            pagination = Pagination(
                offset=offset,
                limit=limit,
                total_count=total_count,
                page=offset // limit + 1,
                total_pages=(total_count // limit) + 1,
            )

            result = OrderList(orders=orders, pagination=pagination)

            return result

        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, order: Order, update_data: UpdateOrderDTO):
        """
        Update an order by ID.
        Args:
            order (Order): The order to update.
            update_data (UpdateOrderDTO): The data to update the order with.
        Returns:
            str: The ID of the updated order.
        """
        try:
            order.sqlmodel_update(update_data)
            order.updated_at = datetime.utcnow()
            self.session.commit()
            self.session.refresh(order)

            return order.id

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, order: Order):
        """
        Delete an order by ID.
        Args:
            order (Order): The order to delete.
        Returns:
            str: The ID of the deleted order.
        """
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
    Args:
        session (Session): The database session to use.
    Returns:
        OrderRepository: An instance of the OrderRepository.
    """
    return OrderRepository(session)
