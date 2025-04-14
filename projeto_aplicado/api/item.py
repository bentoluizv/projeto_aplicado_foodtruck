from fastapi import APIRouter

router = APIRouter(tags=['Item'], prefix='/itens')


@router.get('/')
def get_itens():
    return
