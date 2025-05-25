# Projeto Aplicado SENAI 2025

O Projeto Aplicado é desenvolvido pelos alunos da quarta fase do curso de Análise e Desenvolvimento de Sistemas do SENAI SC em Florianópolis. Trata-se de uma aplicação web escrita em Python, utilizando o framework FastAPI para o backend e HTMX para a interação dinâmica no frontend. O objetivo do projeto é integrar os conhecimentos adquiridos ao longo do curso, promovendo a aplicação prática de conceitos como desenvolvimento de APIs, gerenciamento de dependências, versionamento de código e implantação de aplicações em ambientes de produção.

## Requisitos

- Python 3.12

## Ambiente de Desenvolvimento

> **TL:DR**
>
> Linux > Windows

### Instale o Python e o uv

1. Instale o Python 3.12 usando o [pyenv](https://github.com/pyenv/pyenv) (Linux) ou [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows):

    ***Linux***

    - Baixe o Pyenv

    ```sh
    curl -fsSL https://pyenv.run | bash
    ```

    - Adicione o Pyenv ao PATH

    ```sh
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
    exec "$SHELL"
    ```

    - Instale o Python

    ```sh
    pyenv install 3.12.0
    ```

    ***Windows***

    ```powershell
    Invoke-WebRequest -UseBasicParsing https://pyenv-win.github.io/pyenv-win/install.ps1 | Invoke-Expression
    ```
    - Para atualizar o Pyenv pelo  Power Shell:
    ```
    &"${env:PYENV_HOME}\install-pyenv-win.ps1"
    ```
     - Instalação:
    ```
    pyenv install 3.12.0
    ```

2. Instale o [uv](https://github.com/astral-sh/uv):

    ***Linux***

    ```sh
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

    ***Windows***

    ```powershell
    (Invoke-WebRequest -Uri "https://astral.sh/uv/install.ps1" -UseBasicParsing).Content | pwsh -Command -
    ```

### Download do Projeto e Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git projeto_aplicado
    cd projeto_aplicado
    ```

2. Crie um ambiente virtual e instale as dependências:

    ```sh
    uv venv # Cria um ambiente virtual
    source .venv/bin/activate # Ativa o venv (Linux/macOS)
    # ou
    .venv\Scripts\activate # Ativa o venv (Windows)
    uv pip install -e . # Instala o projeto em modo de desenvolvimento
    ```

3. Crie um arquivo requirements.txt a partir do uv:

    ```sh
    uv pip freeze > requirements.txt
    ```

### Instalação do Docker

1. Instale o Docker seguindo as instruções oficiais para o seu sistema operacional:
    - [Docker para Linux](https://docs.docker.com/engine/install/)
    - [Docker para Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Docker para macOS](https://docs.docker.com/desktop/install/mac-install/)
2. Após a instalação, verifique se o Docker está funcionando corretamente:

    ```sh
    docker --version
    ```

3. Instale o Docker Compose, caso ele não venha incluído na instalação do Docker:
    - [Instruções para instalar o Docker Compose](https://docs.docker.com/compose/install/)
4. Verifique a instalação do Docker Compose:

    ```sh
    docker-compose --version
    ```

5. Certifique-se de que o serviço do Docker está em execução antes de usar os comandos do Docker Compose.

### Uso do Docker Compose

1. Construa e inicie os containers:

    ```sh
    docker-compose up --build
    ```
    Certifique-se de que o banco de dados foi inicializado corretamente antes de prosseguir.

### Próximos Passos

Após configurar o ambiente e inicializar o banco de dados, você pode explorar a documentação interativa da API fornecida pelo FastAPI. A aplicação disponibiliza duas rotas principais para documentação:

1. **Swagger UI**: Acesse a rota `/docs` para visualizar e testar os endpoints da API de forma interativa.
    - URL: `http://localhost:8000/docs`
2. **ReDoc**: Acesse a rota `/redoc` para uma documentação mais detalhada e estruturada.
    - URL: `http://localhost:8000/redoc`

Certifique-se de que a aplicação está em execução antes de acessar as rotas de documentação.

## Documentação da API

A API do FoodTruck é organizada em quatro módulos principais:

### 🔐 Autenticação

O módulo de autenticação gerencia o acesso à API através de tokens JWT.

```http
POST /api/v1/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=secure_password123
```

**Resposta:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

### 👥 Usuários

O módulo de usuários permite gerenciar contas e perfis do sistema.

#### Listar Usuários
```http
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Resposta:**
```json
{
    "items": [
        {
            "id": "1",
            "name": "Admin User",
            "email": "admin@example.com",
            "role": "admin",
            "created_at": "2024-03-20T10:00:00",
            "updated_at": "2024-03-20T10:00:00"
        }
    ],
    "pagination": {
        "offset": 0,
        "limit": 100,
        "total_count": 1,
        "total_pages": 1,
        "page": 1
    }
}
```

#### Criar Usuário
```http
POST /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "name": "New User",
    "email": "new@example.com",
    "password": "secure_password123",
    "role": "attendant"
}
```

### 🍔 Produtos

O módulo de produtos gerencia o catálogo de itens disponíveis.

#### Listar Produtos
```http
GET /api/v1/products
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Resposta:**
```json
{
    "items": [
        {
            "id": "1",
            "name": "X-Burger",
            "description": "Hambúrguer artesanal com queijo",
            "price": 25.90,
            "category": "burger",
            "image_url": "https://example.com/x-burger.jpg",
            "is_available": true,
            "created_at": "2024-03-20T10:00:00",
            "updated_at": "2024-03-20T10:00:00"
        }
    ],
    "pagination": {
        "offset": 0,
        "limit": 100,
        "total_count": 1,
        "total_pages": 1,
        "page": 1
    }
}
```

#### Criar Produto
```http
POST /api/v1/products
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "name": "X-Bacon",
    "description": "Hambúrguer com bacon e queijo",
    "price": 29.90,
    "category": "burger",
    "image_url": "https://example.com/x-bacon.jpg",
    "is_available": true
}
```

### 🛍️ Pedidos

O módulo de pedidos gerencia as comandas e itens solicitados.

#### Listar Pedidos
```http
GET /api/v1/orders
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Resposta:**
```json
{
    "orders": [
        {
            "id": "1",
            "status": "pending",
            "total": 41.80,
            "created_at": "2024-03-20T10:00:00",
            "updated_at": "2024-03-20T10:00:00",
            "locator": "A123",
            "notes": "Sem cebola"
        }
    ],
    "pagination": {
        "offset": 0,
        "limit": 100,
        "total_count": 1,
        "total_pages": 1,
        "page": 1
    }
}
```

#### Criar Pedido
```http
POST /api/v1/orders
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
    "items": [
        {
            "product_id": "1",
            "quantity": 1
        },
        {
            "product_id": "2",
            "quantity": 2
        }
    ],
    "notes": "Sem cebola"
}
```

### Códigos de Status

A API utiliza os seguintes códigos de status HTTP:

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `400 Bad Request`: Dados inválidos
- `401 Unauthorized`: Não autenticado
- `403 Forbidden`: Sem permissão
- `404 Not Found`: Recurso não encontrado
- `409 Conflict`: Conflito de dados
- `422 Unprocessable Entity`: Entidade não processável
- `429 Too Many Requests`: Muitas requisições

### Autenticação

Todas as requisições à API (exceto login) devem incluir o token JWT no header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Paginação

Os endpoints de listagem suportam paginação através dos parâmetros:

- `offset`: Número de registros para pular (padrão: 0)
- `limit`: Limite de registros por página (padrão: 100)

Exemplo:
```http
GET /api/v1/products?offset=0&limit=10
```
