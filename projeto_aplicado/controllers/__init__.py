from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from projeto_aplicado.controllers import category_controller, item_controller
from projeto_aplicado.settings import get_settings

settings = get_settings()

router = APIRouter(prefix=settings.API_PREFIX)

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


router.include_router(item_controller.router)
router.include_router(category_controller.router)
