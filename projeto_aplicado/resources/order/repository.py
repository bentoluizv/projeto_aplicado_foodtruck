from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, func, select
from sqlalchemy.orm import selectinload # Importe este módulo para carregamento ansioso de relações

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.model import Order # Importa o modelo Order
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
        # Inicializa a classe base com a sessão e o modelo Order.
        super().__init__(session, Order)

    def get_total_count(self) -> int:
        """
        Retorna o número total de pedidos no banco de dados.
        """
        # Cria uma instrução SELECT para contar o número de registros na tabela Order.
        stmt = select(func.count()).select_from(Order)
        # Executa a instrução na sessão e retorna o único resultado (a contagem).
        return self.session.exec(stmt).one()

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Order]:
        """
        Retorna uma lista de pedidos, com paginação e carregamento ansioso dos itens.
        Os itens do pedido são carregados junto com a ordem para evitar consultas adicionais.
        """
        # Constrói a instrução SELECT para buscar todos os pedidos.
        # .options(selectinload(Order.products)) instrui o ORM a carregar a relação 'products'
        # (que são os OrderItems associados) junto com os dados de cada Order.
        statement = (
            select(self.model) # self.model refere-se à classe Order
            .options(selectinload(Order.products)) # Usa 'products' conforme definido no seu model.py
            .offset(offset)
            .limit(limit)
        )
        # Executa a instrução, obtém todos os resultados e usa .unique() para remover duplicatas
        # que podem surgir de carregamentos de relações one-to-many.
        return self.session.exec(statement).unique().all()

    def get_by_id(self, item_id: str) -> Order | None:
        """
        Retorna um pedido específico pelo ID, com carregamento ansioso dos itens.
        """
        # Constrói a instrução SELECT para buscar um pedido por seu ID.
        # Também carrega ansiosamente a relação 'products' para que os itens estejam disponíveis.
        statement = (
            select(self.model)
            .where(self.model.id == item_id)
            .options(selectinload(Order.products)) # Usa 'products' conforme definido no seu model.py
        )
        # Executa a instrução e retorna o primeiro resultado único encontrado, ou None se nenhum.
        return self.session.exec(statement).unique().first()

    def update(self, order: Order, dto: UpdateOrderDTO) -> Order:
        """
        Atualiza um pedido existente com base nos dados do DTO.
        """
        # Converte o DTO (Data Transfer Object) para um dicionário,
        # excluindo campos que não foram definidos no DTO (exclude_unset=True).
        update_data = dto.model_dump(exclude_unset=True)
        # Chama o método update da classe base (BaseRepository) para aplicar as atualizações.
        return super().update(order, update_data)

    # Assumindo que o BaseRepository possui métodos síncronos para 'create' e 'delete'.
    # Se não tiverem, você precisaria sobrescrevê-los aqui e implementar a lógica síncrona.
    # Exemplo (se create não for async na base):
    # def create(self, order_instance: Order) -> Order:
    #     self.session.add(order_instance)
    #     self.session.commit()
    #     self.session.refresh(order_instance)
    #     return order_instance