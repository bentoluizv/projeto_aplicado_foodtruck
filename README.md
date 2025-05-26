# Projeto Aplicado SENAI 2025

O Projeto Aplicado é desenvolvido pelos alunos da quarta fase do curso de Análise e Desenvolvimento de Sistemas do SENAI SC em Florianópolis. Trata-se de uma aplicação web escrita em Python, utilizando o framework FastAPI para o backend e HTMX para a interação dinâmica no frontend. O objetivo do projeto é integrar os conhecimentos adquiridos ao longo do curso, promovendo a aplicação prática de conceitos como desenvolvimento de APIs, gerenciamento de dependências, versionamento de código e implantação de aplicações em ambientes de produção.

## 📋 Índice

- [Requisitos](#requisitos)
- [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
  - [Instalação do Python e uv](#instale-o-python-e-o-uv)
  - [Download e Instalação do Projeto](#download-do-projeto-e-instalação)
  - [Instalação do Docker](#instalação-do-docker)
  - [Uso do Docker Compose](#uso-do-docker-compose)
- [Documentação da API](#documentação-da-api)
  - [Visão Geral](#visão-geral)
  - [Mapa de Endpoints](#mapa-de-endpoints)
  - [Detalhes dos Endpoints](#detalhes-dos-endpoints)
  - [Padrões Comuns](#padrões-comuns)

## Requisitos

- Python 3.12
- Docker e Docker Compose
- Git

## Ambiente de Desenvolvimento

> **TL:DR**
>
> Linux > Windows

### Instale o Python e o uv

1. Instale o Python 3.12 usando o [pyenv](https://github.com/pyenv/pyenv) (Linux) ou [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows):

    ***Linux***

    ```sh
    # Baixe o Pyenv
    curl -fsSL https://pyenv.run | bash

    # Adicione o Pyenv ao PATH
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
    exec "$SHELL"

    # Instale o Python
    pyenv install 3.12.0
    ```

    ***Windows***

    ```powershell
    # Instale o Pyenv
    Invoke-WebRequest -UseBasicParsing https://pyenv-win.github.io/pyenv-win/install.ps1 | Invoke-Expression

    # Atualize o Pyenv
    &"${env:PYENV_HOME}\install-pyenv-win.ps1"

    # Instale o Python
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

2. Configure o ambiente:

    ```sh
    # Crie e ative o ambiente virtual
    uv venv
    source .venv/bin/activate  # Linux/macOS
    # ou
    .venv\Scripts\activate     # Windows

    # Instale o projeto
    uv pip install -e .
    ```

### Instalação do Docker

1. Instale o Docker seguindo as instruções oficiais:
    - [Docker para Linux](https://docs.docker.com/engine/install/)
    - [Docker para Windows](https://docs.docker.com/desktop/install/windows-install/)
    - [Docker para macOS](https://docs.docker.com/desktop/install/mac-install/)

2. Verifique a instalação:

    ```sh
    docker --version
    docker-compose --version
    ```

### Uso do Docker Compose

1. Inicie os containers:

    ```sh
    docker-compose up --build
    ```

2. Acesse a documentação:
    - Swagger UI: `http://localhost:8000/docs`
    - ReDoc: `http://localhost:8000/redoc`

## Documentação da API

### Visão Geral

A API do FoodTruck é organizada em quatro módulos principais:

- 🔐 **Autenticação**: Gerenciamento de tokens JWT
- 👥 **Usuários**: Gerenciamento de contas e perfis
- 🍔 **Produtos**: Catálogo de itens disponíveis
- 🛍️ **Pedidos**: Sistema de comandas

### Mapa de Endpoints

| Método | Endpoint | Descrição | Autenticação | Permissões |
|--------|----------|-----------|--------------|------------|
| **🔐 Autenticação** |
| `POST` | `/api/v1/token` | Gera token JWT | Não | Público |
| **👥 Usuários** |
| `GET` | `/api/v1/users` | Lista usuários | Sim | Admin |
| `GET` | `/api/v1/users/{id}` | Obtém usuário | Sim | Admin |
| `POST` | `/api/v1/users` | Cria usuário | Sim | Admin |
| `PATCH` | `/api/v1/users/{id}` | Atualiza usuário | Sim | Admin |
| `DELETE` | `/api/v1/users/{id}` | Remove usuário | Sim | Admin |
| **🍔 Produtos** |
| `GET` | `/api/v1/products` | Lista produtos | Sim | Todos |
| `GET` | `/api/v1/products/{id}` | Obtém produto | Sim | Todos |
| `POST` | `/api/v1/products` | Cria produto | Sim | Admin |
| `PUT` | `/api/v1/products/{id}` | Atualiza produto | Sim | Admin |
| `PATCH` | `/api/v1/products/{id}` | Atualiza parcialmente | Sim | Admin |
| `DELETE` | `/api/v1/products/{id}` | Remove produto | Sim | Admin |
| **🛍️ Pedidos** |
| `GET` | `/api/v1/orders` | Lista pedidos | Sim | Todos |
| `GET` | `/api/v1/orders/{id}` | Obtém pedido | Sim | Todos |
| `GET` | `/api/v1/orders/{id}/items` | Lista itens do pedido | Sim | Todos |
| `POST` | `/api/v1/orders` | Cria pedido | Sim | Admin, Atendente |
| `PATCH` | `/api/v1/orders/{id}` | Atualiza pedido | Sim | Admin, Atendente |
| `DELETE` | `/api/v1/orders/{id}` | Remove pedido | Sim | Admin, Atendente |

### Padrões Comuns

#### Autenticação

Todas as requisições (exceto login) devem incluir o token JWT:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Paginação

Endpoints de listagem suportam paginação:

```http
GET /api/v1/products?offset=0&limit=10
```

Parâmetros:
- `offset`: Registros para pular (padrão: 0)
- `limit`: Registros por página (padrão: 100)

#### Códigos de Status

| Código | Descrição |
|--------|-----------|
| `200` | Requisição bem-sucedida |
| `201` | Recurso criado |
| `400` | Dados inválidos |
| `401` | Não autenticado |
| `403` | Sem permissão |
| `404` | Recurso não encontrado |
| `409` | Conflito de dados |
| `422` | Entidade não processável |
| `429` | Muitas requisições |

### Detalhes dos Endpoints

#### 🔐 Autenticação

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

#### 👥 Usuários

**Listar Usuários**
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

**Criar Usuário**
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

#### 🍔 Produtos

**Listar Produtos**
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

**Criar Produto**
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

#### 🛍️ Pedidos

**Listar Pedidos**
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

**Criar Pedido**
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
