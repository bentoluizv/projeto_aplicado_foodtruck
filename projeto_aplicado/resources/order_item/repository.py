from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order_item.model import OrderItem
from projeto_aplicado.resources.order_item.schemas import (
    OrderItemList,
    UpdateOrderItemDTO,
)
from projeto_aplicado.schemas import Pagination


class OrderItemRepository:
    """
    Repository for OrderItem model.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a database session.
        Args:
            session (Session): The database session to use.
        """
        self.session = session

    def create(self, item: OrderItem):
        """
        Create a new item.
        Args:
            item (OrderItem): The item to create.
        Returns:
            str: The ID of the created item.

        """
        try:
            self.session.add(item)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100):
        """
        Get all ordem itens with optional pagination.
        Args:
            offset (int): The offset for pagination.
            limit (int): The maximum number of itens to retrieve.
        Returns:
            ProductList: A list of order itens with pagination information.
        """
        try:
            orderitem_count_stmt = select(func.count()).select_from(OrderItem)

            total_count = self.session.exec(orderitem_count_stmt).first()

            if not total_count:
                total_count = 0

            get_all_order_items_stmt = (
                select(OrderItem).offset(offset).limit(limit)
            )

            order_items = self.session.exec(get_all_order_items_stmt).all()

            pagination = Pagination(
                offset=offset,
                limit=limit,
                total_count=total_count,
                page=offset // limit + 1,
                total_pages=(total_count // limit) + 1,
            )

            result = OrderItemList(
                order_itens=order_items, pagination=pagination
            )

            return result

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, item_id: str):
        """
        Get an order item by ID.
        Args:
            item_id (str): The ID of the order item to retrieve.
        Returns:
            OrderItem: The order item with the specified ID.
        Raises:
            Exception: If an error occurs during retrieval.
        """
        try:
            item = self.session.get(OrderItem, item_id)

            return item

        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, order_item: OrderItem, dto: UpdateOrderItemDTO):
        """
        Update an item.
        Args:
            order_item (OrderItem): The item to update.
            dto (UpdateOrderItemDTO): The data transfer object containing the updated values.
        Returns:
            str: The ID of the updated item.
        Raises:
            Exception: If an error occurs during the update.
        """  # noqa: E501
        try:
            update_data = dto.model_dump(exclude_unset=True)

            order_item.sqlmodel_update(update_data)

            self.session.commit()
            self.session.refresh(order_item)

            return order_item.id

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, order_item: OrderItem):
        """
        Delete an order item.
        Args:
            order_item (OrderItem): The order item to delete.
        Returns:
            str: The ID of the deleted order item.
        Raises:
            Exception: If an error occurs during deletion.
        """
        try:
            self.session.delete(order_item)
            self.session.commit()

            return order_item.id

        except Exception as e:
            self.session.rollback()
            raise e


def get_order_item_repository(
    session: Annotated[Session, Depends(get_session)],
):
    """
    Dependency to get the ItemRepository.
    """
    return OrderItemRepository(session)
