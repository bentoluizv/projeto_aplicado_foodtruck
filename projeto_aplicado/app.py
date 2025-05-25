from typing import Annotated

from fastapi import Depends, FastAPI
from supabase import Client

from projeto_aplicado.ext.database.db import get_engine
from projeto_aplicado.ext.supabase.client import get_supabase_client
from projeto_aplicado.ext.supabase.storage import list_all_icons
from projeto_aplicado.resources.order.controller import router as order_router
from projeto_aplicado.resources.product.controller import router as item_router
from projeto_aplicado.resources.shared.schemas import IconsResponse
from projeto_aplicado.resources.users.controller import router as user_router
from projeto_aplicado.settings import get_settings

settings = get_settings()
engine = get_engine()

Supabase = Annotated[Client, Depends(get_supabase_client)]

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


@app.get('/icons', response_model=IconsResponse)
async def get_icons(supabase: Supabase):
    """
    Returns a list of available icons.
    """
    result = list_all_icons(supabase)
    return IconsResponse.model_validate(result)


app.include_router(item_router)
app.include_router(order_router)
app.include_router(user_router)
