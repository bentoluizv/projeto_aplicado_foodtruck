from typing import Annotated

from fastapi import Depends, FastAPI

from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.auth.token import router as token_router
from projeto_aplicado.ext.database.db import get_engine
from projeto_aplicado.resources.order.controller import router as order_router
from projeto_aplicado.resources.product.controller import router as item_router
from projeto_aplicado.resources.users.controller import router as user_router
from projeto_aplicado.resources.users.model import User
from projeto_aplicado.settings import get_settings

settings = get_settings()
engine = get_engine()

CurrentUser = Annotated[User, Depends(get_current_user)]

app = FastAPI(
    debug=settings.API_DEBUG,
    title='FoodTruck API',
    version=settings.API_VERSION,
    description="""
    API do sistema de gerenciamento de FoodTruck desenvolvido para o Projeto Aplicado do SENAI 2025.

    ## Funcionalidades

    * 🔐 **Autenticação**: Sistema de login com JWT
    * 👥 **Usuários**: Gerenciamento de usuários e perfis
    * 🍔 **Produtos**: Cadastro e gerenciamento de produtos
    * 🛍️ **Pedidos**: Sistema completo de pedidos

    ## Documentação

    * `/docs`: Interface Swagger para testes interativos
    * `/redoc`: Documentação ReDoc mais detalhada
    """,  # noqa: E501
    openapi_tags=[
        {
            'name': 'Token',
            'description': 'Operações de autenticação e geração de tokens JWT',
        },
        {
            'name': 'Usuários',
            'description': 'Gerenciamento de usuários e perfis do sistema',
        },
        {
            'name': 'Produtos',
            'description': 'Operações relacionadas ao cadastro e gerenciamento de produtos',  # noqa: E501
        },
        {
            'name': 'Pedidos',
            'description': 'Sistema de pedidos e gerenciamento de comandas',
        },
    ],
)


@app.get('/')
async def home():
    """
    Endpoint raiz que retorna informações sobre a API.
    """
    return {
        'name': 'FoodTruck API',
        'version': settings.API_VERSION,
        'description': 'API do sistema de gerenciamento de FoodTruck',
    }


app.include_router(token_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(order_router)
