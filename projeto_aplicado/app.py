import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from projeto_aplicado import controllers, pages
from projeto_aplicado.ext.database.db import create_all, get_engine
from projeto_aplicado.settings import get_settings

settings = get_settings()


app = FastAPI(
    debug=settings.API_DEBUG,
    title='Projeto Aplicado SENAI 2025',
    version=settings.API_VERSION,
    description='API para o projeto aplicado do SENAI 2025',
)

app.mount(
    '/static',
    StaticFiles(directory=os.path.join(os.getcwd(), 'static')),
    name='static',
)

app.include_router(pages.router)
app.include_router(controllers.router)


if __name__ == '__main__':
    engine = get_engine()
    create_all(engine)
