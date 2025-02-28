# Projeto Aplicado SENAI 2025

O Projeto Aplicado é um projeto integrador do curso de Análise e Desenvolvimento de Sistemas do SENAI de Florianópolis. Esta aplicação web é escrita em FastAPI e HTMX.

## Instruções para ambiente de Desenvolvimento

### Requisitos

- Python 3.13

### Uso do Poetry

1. Clone o repositório:

    ```sh
    git clone https://github.com/bentoluizv/senai_projeto_aplicado_3.git
    cd projeto-aplicado
    ```

2. Instale o Poetry, crie um ambiente virtual e instale as dependências::

    ```sh
    poetry use 3.13
    eval $(poetry env activate)
    poetry install
    ```

3. Execute a aplicação:

    ```sh
    task dev
    ```

### Uso do Docker Compose

1. Construa e inicie os containers

    ```sh
    docker-compose up --build
    ```

2. Acesse a aplicação em [http://localhost:8000](http://localhost:8000).

### Dependências do Projeto

As principais dependências do projeto estão listadas no arquivo `requirements.txt` e incluem:

- FastAPI
- SQLModel
- Uvicorn
- Pytest (para testes)

### Outras Informações Úteis

- O arquivo `.env` contém as variáveis de ambiente necessárias para a configuração do banco de dados e do Redis.
- O arquivo `docker-compose.yaml` define os serviços para a aplicação, banco de dados PostgreSQL e Redis.
- O arquivo `Dockerfile` é usado para criar a imagem Docker da aplicação.

Para mais detalhes sobre a estrutura do projeto e como contribuir, consulte a documentação no repositório.
