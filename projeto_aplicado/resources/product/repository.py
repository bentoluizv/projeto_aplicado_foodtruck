from typing import Annotated, Optional

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

    def get_count(self) -> int:
        return len(self.session.exec(select(Product)).all())

    def find_by_name(self, name: str) -> Optional[Product]:
        return self.session.exec(
            select(Product).where(Product.name == name)
        ).first()

    def update(
        self, product_id: str, product_dto: UpdateProductDTO
    ) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if product:
            product_data = product_dto.model_dump(exclude_unset=True)
            for key, value in product_data.items():
                setattr(product, key, value)
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
        return product

    def delete(self, product_id: str) -> bool:
        product = self.get_by_id(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            return True
        return False
