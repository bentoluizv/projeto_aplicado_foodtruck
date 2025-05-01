from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.schemas import (
    UpdateProductDTO,
)


class ProductRepository:
    def __init__(self, session: Session):
        """
        Repository for Item entity.
        """
        self.session = session

    def create(self, item: Product):
        """
        Create a new item.
        """
        try:
            self.session.add(item)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100):
        """
        Get all items.
        """
        try:
            items = self.session.exec(
                select(Product).offset(offset).limit(limit)
            ).all()

            return items

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, item_id: str):
        """
        Get an item by ID.
        """
        try:
            item = self.session.get(Product, item_id)

            return item

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_name(self, name: str):
        """
        Get an item by name.
        """
        try:
            item = self.session.exec(
                select(Product).where(Product.name == name)
            ).first()

            return item

        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, item: Product, dto: UpdateProductDTO):
        """
        Update an item.
        """
        try:
            update_data = dto.model_dump(exclude_unset=True)
            item.sqlmodel_update(update_data)

            self.session.commit()
            self.session.refresh(item)

            return item.id

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, item: Product):
        """
        Delete an item.
        """
        try:
            self.session.delete(item)
            self.session.commit()

            return item.id

        except Exception as e:
            self.session.rollback()
            raise e


def get_product_repository(
    session: Annotated[Session, Depends(get_session)],
):
    """
    Dependency to get the ItemRepository.
    """
    return ProductRepository(session)
