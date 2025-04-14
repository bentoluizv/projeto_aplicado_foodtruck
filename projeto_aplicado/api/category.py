from fastapi import APIRouter

router = APIRouter(tags=['Category'], prefix='/categories')


@router.get('/')
def get_categories():
    return
