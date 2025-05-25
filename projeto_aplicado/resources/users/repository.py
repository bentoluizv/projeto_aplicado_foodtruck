from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.shared.repository import BaseRepository
from projeto_aplicado.resources.users.model import User
from projeto_aplicado.resources.users.schemas import UpdateUserDTO


def get_user_repository(session: Annotated[Session, Depends(get_session)]):
    return UserRepository(session)


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def get_total_count(self) -> int:
        stmt = select(func.count()).select_from(User)
        return self.session.exec(stmt).one()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()

    def update(self, user: User, dto: UpdateUserDTO) -> User:
        update_data = dto.model_dump(exclude_unset=True)
        return super().update(user, update_data)
