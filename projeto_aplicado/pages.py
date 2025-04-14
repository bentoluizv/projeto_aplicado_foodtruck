from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)


@router.get('/')
async def home_page(request: Request):
    """
    Serve a página principal do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/menu')
async def menu_page(request: Request):
    """
    Serve a página de cardápio do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse('menu.html', {'request': request})
