import os

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    debug=True,
    title='Projeto Aplicado SENAI 2025',
    version='0.1.0',
    description='API para o projeto aplicado do SENAI 2025',
)


app.mount(
    '/static',
    StaticFiles(directory=os.path.join(os.getcwd(), 'static')),
    name='static',
)

templates = Jinja2Templates(
    directory='templates',
    auto_reload=True,
    cache_size=0,
)


@app.get('/')
async def home_page(request: Request):
    """
    Serve a página principal do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/menu')
async def menu_page(request: Request):
    """
    Serve a página principal do projeto, retorna um HTML Response.

    """
    return templates.TemplateResponse('menu.html', {'request': request})
