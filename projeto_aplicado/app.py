import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from projeto_aplicado import controllers, pages
from projeto_aplicado.ext.database.db import (
    get_engine,
)

# from projeto_aplicado.models.entities import create_all
from projeto_aplicado.settings import get_settings

settings = get_settings()

engine = get_engine()

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

app.include_router(pages.router)
app.include_router(controllers.router)
