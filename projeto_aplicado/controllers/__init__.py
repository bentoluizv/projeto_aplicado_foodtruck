from fastapi import APIRouter

from projeto_aplicado.controllers import category_controller, item_controller
from projeto_aplicado.settings import get_settings

settings = get_settings()

router = APIRouter(prefix=settings.API_PREFIX)

router.include_router(item_controller.router)
router.include_router(category_controller.router)
