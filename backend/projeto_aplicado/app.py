import os
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Header, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from supabase import Client

from projeto_aplicado.data.schemas import IconsResponse

# from projeto_aplicado.data.utils import create_all
from projeto_aplicado.ext.database.db import (
    get_engine,
)
from projeto_aplicado.ext.supabase.client import get_supabase_client
from projeto_aplicado.ext.supabase.storage import list_all_icons
from projeto_aplicado.resources.category.api import router as category_router
from projeto_aplicado.resources.product.api import router as item_router
from projeto_aplicado.settings import get_settings

settings = get_settings()

engine = get_engine()

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)

Supabase = Annotated[Client, Depends(get_supabase_client)]

app = FastAPI(
    debug=settings.API_DEBUG,
    title='Projeto Aplicado SENAI 2025',
    version=settings.API_VERSION,
    description='API para o projeto aplicado do SENAI 2025',
    # # Se deixar o lifespan, não é possível rodar os testes com pytest,
    # pois ele tenta executar o lifespan antes da fixture que faz override
    # do engine. Isso gera um erro, pois o engine não está configurado para
    # o banco de dados correto. Ainda tentando descobrir como resolver isso.
    # lifespan=create_all(engine),
)

app.mount(
    '/static',
    StaticFiles(directory=os.path.join(os.getcwd(), 'static')),
    name='static',
)


@app.get('/', include_in_schema=False)
async def home_page(request: Request):
    """
    Serve a página principal do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse(request, 'index.html')


@app.get('/menu', include_in_schema=False)
async def menu_page(request: Request):
    """
    Serve a página de cardápio do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse(request, 'menu.html')


@app.get('/icons', response_model=IconsResponse, include_in_schema=False)
async def icons_page(
    request: Request,
    supabase: Supabase,
    hx_request: Annotated[Union[str, None], Header()] = None,
):
    """
    Serve a página de ícones de categorias do projeto,
    retorna um HTML Response.

    """
    result = list_all_icons(supabase)
    icons = IconsResponse.model_validate(result).icons

    if hx_request:
        return templates.TemplateResponse(
            request, 'icons.html', context={'icons': icons}
        )

    return {'icons': icons}


app.include_router(item_router)
app.include_router(category_router)
