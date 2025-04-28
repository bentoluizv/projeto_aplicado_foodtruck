from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from projeto_aplicado.data.schemas import (
    UpdateCategoryDTO,
)
from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.category.model import Category


class CategoryRepository:
    def __init__(self, session: Session):
        """
        Repository for Category entity.
        """
        self.session = session

    def create(self, category: Category):
        try:
            self.session.add(category)
            self.session.commit()

            return category.id

        except Exception as e:
            self.session.rollback()
            raise e

    def get_all(self, offset: int = 0, limit: int = 100):
        try:
            categories = self.session.exec(
                select(Category).offset(offset).limit(limit)
            ).all()

            return categories

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_id(self, category_id: str):
        try:
            category = self.session.get(Category, category_id)

            return category

        except Exception as e:
            self.session.rollback()
            raise e

    def get_by_name(self, name: str):
        """
        Get a category by name.
        """
        try:
            category = self.session.exec(
                select(Category).where(Category.name == name)
            ).first()

            return category

        except Exception as e:
            self.session.rollback()
            raise e

    def update(self, category: Category, dto: UpdateCategoryDTO):
        """
        Update a category.
        """
        try:
            update_data = dto.model_dump(exclude_unset=True)
            category.sqlmodel_update(update_data)

            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def delete(self, category: Category):
        try:
            self.session.delete(category)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e


def get_category_repository(
    session: Annotated[Session, Depends(get_session)],
):
    """
    Dependency to get the CategoryRepository.

    """
    return CategoryRepository(session)
