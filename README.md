# Projeto Aplicado SENAI 2025

O Projeto Aplicado é um projeto integrador do curso de Análise e Desenvolvimento de Sistemas do SENAI de Florianópolis. Esta aplicação web é escrita em FastAPI e HTMX.

## Instruções para ambiente de Desenvolvimento

### Requisitos

- Python 3.13

### Set up

1. Clone o repositório:

    ```sh
    git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git projeto_aplicado
    cd projeto_aplicado
    ```

2. Instale o [Poetry](https://python-poetry.org/docs/#installation), crie um ambiente virtual e instale as dependências:

    ```sh
    poetry use 3.13
    eval $(poetry env activate)
    poetry install
    ```

3. Execute a aplicação:

    ```sh
    task dev
    ```

4. Crie um arquivo requirements.txt a partir do Poetry:

    ```sh
    task export
    ```

### Uso do Docker Compose

1. Construa e inicie os containers

    ```sh
    docker-compose up --build
    ```

2. Acesse a aplicação em [http://localhost:8000](http://localhost:8000).
