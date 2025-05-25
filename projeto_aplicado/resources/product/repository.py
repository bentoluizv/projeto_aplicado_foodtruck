from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.schemas import (
    ProductList,
    ProductOut,
    UpdateProductDTO,
)
from projeto_aplicado.resources.shared.repository import BaseRepository
from projeto_aplicado.resources.shared.schemas import Pagination


def get_product_repository(session: Annotated[Session, Depends(get_session)]):
    return ProductRepository(session)


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: Session):
        super().__init__(session, Product)

    def get_total_count(self) -> int:
        stmt = select(func.count()).select_from(Product)
        return self.session.exec(stmt).one()

    def get_all(self, offset: int = 0, limit: int = 100) -> ProductList:
        total_count = self.get_total_count()
        products = super().get_all(offset=offset, limit=limit)
        pagination = Pagination.create(offset, limit, total_count)
        return ProductList(
            items=[ProductOut.model_validate(product) for product in products],
            pagination=pagination,
        )

    def get_by_name(self, name: str) -> Product | None:
        stmt = select(Product).where(Product.name == name)
        return self.session.exec(stmt).first()

    def update(self, product: Product, dto: UpdateProductDTO) -> Product:
        update_data = dto.model_dump(exclude_unset=True)
        return super().update(product, update_data)

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
