from fastapi import APIRouter

from projeto_aplicado.api import category, item
from projeto_aplicado.settings import get_settings

settings = get_settings()

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(item.router)
router.include_router(category.router)
