from fastapi import FastAPI

app = FastAPI(
    debug=True,
    title='Projeto Aplicado SENAI 2025',
    version='0.1.0',
    description='API para o projeto aplicado do SENAI 2025',
)


@app.get('/')
async def read_root():
    return {'message': 'Hello World'}
