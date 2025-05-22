from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.schemas import (
    ProductList,
    UpdateProductDTO,
)
from projeto_aplicado.resources.shared.schemas import Pagination


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
        Get all items with optional pagination.
        Args:
            offset (int): The offset for pagination.
            limit (int): The maximum number of items to retrieve.
        Returns:
            ProductList: A list of items with pagination information.
        """
        try:
            products_count_stmt = select(func.count()).select_from(Product)

            total_count = self.session.exec(products_count_stmt).first()

            if not total_count:
                total_count = 0

            get_all_products_stmt = select(Product).offset(offset).limit(limit)
            products = self.session.exec(get_all_products_stmt).all()

            pagination = Pagination(
                offset=offset,
                limit=limit,
                total_count=total_count,
                page=offset // limit + 1,
                total_pages=(total_count // limit) + 1,
            )

            result = ProductList(products=products, pagination=pagination)

            return result

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
