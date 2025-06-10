from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select
from sqlalchemy.orm import selectinload

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.order.schemas import UpdateOrderDTO
from projeto_aplicado.resources.shared.repository import BaseRepository


def get_order_repository(session: Annotated[Session, Depends(get_session)]):
    """
    Dependência que fornece uma instância de OrderRepository com a sessão do banco de dados.
    """
    return OrderRepository(session)


class OrderRepository(BaseRepository[Order]):
    """
    Repositório para gerenciar operações de dados (CRUD) do modelo Order.
    Herda de BaseRepository para funcionalidades comuns e adiciona lógica específica para pedidos.
    """
    def __init__(self, session: Session):
        super().__init__(session, Order)

    async def get_total_count(self) -> int:
        """
        Retorna o número total de pedidos no banco de dados de forma assíncrona.
        A execução da consulta é síncrona, mas a função é awaitable.
        """
        stmt = select(func.count()).select_from(Order)
        # REMOVIDO: await antes de self.session.exec()
        return self.session.exec(stmt).one()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Order]:
        """
        Retorna uma lista de pedidos de forma assíncrona, com paginação e carregamento ansioso dos itens.
        Os itens do pedido são carregados junto com a ordem para evitar consultas adicionais.
        """
        statement = (
            select(self.model)
            .options(selectinload(Order.products)) # Usa 'products' conforme definido no seu model.py
            .offset(offset)
            .limit(limit)
        )
        # REMOVIDO: await antes de self.session.exec()
        return self.session.exec(statement).unique().all()

    async def get_by_id(self, item_id: str) -> Order | None:
        """
        Retorna um pedido específico pelo ID de forma assíncrona, com carregamento ansioso dos itens.
        """
        statement = (
            select(self.model)
            .where(self.model.id == item_id)
            .options(selectinload(Order.products)) # Usa 'products' conforme definido no seu model.py
        )
        # REMOVIDO: await antes de self.session.exec()
        return self.session.exec(statement).unique().first()

    async def update(self, order: Order, dto: UpdateOrderDTO) -> Order:
        """
        Atualiza um pedido existente de forma assíncrona com base nos dados do DTO.
        """
        update_data = dto.model_dump(exclude_unset=True)
        return await super().update(order, update_data)


