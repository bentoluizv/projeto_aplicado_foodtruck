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
    title='Projeto Aplicado SENAI 2025',
    version=settings.API_VERSION,
    description='API para o projeto aplicado do SENAI 2025',
)


@app.get('/')
async def home():
    """
    Root endpoint that returns API information.
    """
    return {
        'name': 'Projeto Aplicado SENAI 2025',
        'version': settings.API_VERSION,
        'description': 'API para o projeto aplicado do SENAI 2025',
    }


app.include_router(token_router)
app.include_router(user_router)
app.include_router(item_router)
app.include_router(order_router)
