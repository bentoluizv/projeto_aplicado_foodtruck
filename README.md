# 🚚 Food Truck Management System

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Test Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](https://coverage.readthedocs.io)

> **Projeto Aplicado SENAI 2025** - Um sistema completo de gerenciamento para food trucks desenvolvido com Python, FastAPI, e tecnologias modernas.

## 🎯 Visão Geral

O **Food Truck Management System** é uma aplicação web moderna desenvolvida para gerenciar operações de food trucks. O sistema oferece uma API RESTful robusta construída com FastAPI, autenticação JWT, e uma arquitetura limpa que segue os princípios SOLID.

### 🎨 Tecnologias Principais

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) + [SQLModel](https://sqlmodel.tiangolo.com/)
- **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
- **Autenticação**: [JWT](https://jwt.io/) com [argon2](https://github.com/hynek/argon2-cffi)
- **CLI**: [Cyclopts](https://github.com/BrianPugh/cyclopts)
- **Testes**: [Pytest](https://pytest.org/) + [TestContainers](https://testcontainers.com/)
- **Containerização**: [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)
- **Gerenciamento de Dependências**: [uv](https://github.com/astral-sh/uv)

### 🎭 Personas e Papéis

| Papel | Descrição | Permissões |
|-------|-----------|------------|
| **👑 Admin** | Administrador do sistema | Acesso total, gerenciamento de usuários |
| **👥 Atendente** | Operador de vendas | Criar/editar pedidos, visualizar produtos |
| **👨‍🍳 Cozinha** | Operador da cozinha | Atualizar status dos pedidos |
| **👤 Cliente** | *Futuro* | Visualizar cardápio, fazer pedidos |

## 📋 Índice

- [✨ Funcionalidades](#-funcionalidades)
- [🏗️ Arquitetura](#️-arquitetura)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Instalação Completa](#️-instalação-completa)
- [📖 CLI Tools](#-cli-tools)
- [🧪 Testes](#-testes)
- [📚 Documentação da API](#-documentação-da-api)
- [🔒 Segurança](#-segurança)
- [📈 Monitoramento](#-monitoramento)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

## ✨ Funcionalidades

### 🔐 Sistema de Autenticação
- Login seguro com JWT tokens
- Hash de senhas com Argon2ID
- Controle de acesso baseado em papéis (RBAC)
- Refresh tokens (*planejado*)

### 👥 Gerenciamento de Usuários
- CRUD completo de usuários
- Diferentes níveis de acesso
- Perfis personalizáveis
- Auditoria de ações (*planejado*)

### 🍔 Catálogo de Produtos
- Gestão de produtos e categorias
- Upload de imagens (*planejado*)
- Controle de disponibilidade
- Histórico de preços (*planejado*)

### 🛍️ Sistema de Pedidos
- Criação e gerenciamento de pedidos
- Status de acompanhamento
- Cálculo automático de totais
- Sistema de localizadores (A123, B456...)
- Avaliações de pedidos

### 🏃‍♂️ CLI Moderno (Clean Architecture)
- **Arquitetura Limpa**: Separação entre comandos, serviços e infraestrutura
- **SOLID Principles**: Fácil manutenção e extensão
- **Dependency Injection**: Baixo acoplamento entre componentes
- **100% Testado**: Cobertura completa com 71 testes dedicados
- **Rich Output**: Interface visual moderna com cores e símbolos

## 🏗️ Arquitetura

O projeto segue uma **arquitetura em camadas** com separação clara de responsabilidades:

### 📁 Estrutura do Projeto

```
projeto_aplicado/
├── 🎯 app.py                    # Aplicação FastAPI principal
├── ⚙️  settings.py              # Configurações do sistema
├── 🔐 auth/                     # Sistema de autenticação
│   ├── password.py             # Hash de senhas
│   ├── security.py             # Middleware de segurança
│   └── token.py                # Geração/validação JWT
├── 💾 ext/                      # Extensões e infraestrutura
│   └── database/               # Configuração do banco
├── 📚 resources/                # Recursos da API
│   ├── user/                   # Gestão de usuários
│   ├── product/                # Catálogo de produtos
│   ├── order/                  # Sistema de pedidos
│   └── shared/                 # Componentes compartilhados
└── 🛠️ cli/                      # Ferramentas CLI (Arquitetura Limpa)
    ├── app.py                  # CLI principal
    ├── base/                   # Classes base (SOLID)
    ├── commands/               # Comandos CLI
    ├── services/               # Lógica de negócio
    └── tests/                  # Testes do CLI
```

### 🔄 Fluxo de uma Requisição

1. **🌐 Controller** recebe requisição HTTP
2. **🔒 Auth Middleware** valida autenticação/autorização
3. **📋 Pydantic** valida dados de entrada (DTO)
4. **🏢 Repository** executa operações no banco
5. **📤 Response** formatada e enviada

## 🚀 Quick Start

### 📋 Pré-requisitos

- [Python 3.12+](https://www.python.org/downloads/)
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)

### ⚡ Início Rápido (5 minutos)

```bash
# 1. Clone o repositório
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# 2. Inicie os serviços
docker-compose up --build -d

# 3. Configure o sistema (cria banco + admin)
docker-compose exec api uv run task cli-setup

# 4. Acesse a documentação
open http://localhost:8000/docs
```

🎉 **Pronto!** Seu sistema está rodando em `http://localhost:8000`

### 🔑 Credenciais Padrão

- **Usuário**: `admin`
- **Email**: `admin@foodtruck.com`
- **Senha**: `admin123`

## 🛠️ Instalação Completa

### 🐍 Instalação Local (Desenvolvimento)

#### 1. Instale o Python e uv

**Linux/macOS:**
```bash
# Instale pyenv para gerenciar versões Python
curl https://pyenv.run | bash

# Instale Python 3.12
    pyenv install 3.12.0
pyenv local 3.12.0

# Instale uv (gerenciador de dependências moderno)
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

**Windows (PowerShell):**
    ```powershell
# Instale pyenv-win
Invoke-WebRequest -UseBasicParsing https://pyenv-win.github.io/pyenv-win/install.ps1 | Invoke-Expression

# Instale Python 3.12
pyenv install 3.12.0
pyenv local 3.12.0

# Instale uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Configure o Ambiente

```bash
# Clone e entre no diretório
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Crie ambiente virtual
    uv venv

# Ative o ambiente virtual
    source .venv/bin/activate  # Linux/macOS
    # ou
    .venv\Scripts\activate     # Windows

# Instale o projeto em modo desenvolvimento
uv pip install -e ".[dev]"
```

#### 3. Configure o Banco de Dados

```bash
# Inicie PostgreSQL com Docker
docker run -d \
  --name foodtruck-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=foodtruck \
  -p 5432:5432 \
  postgres:16

# Configure o banco e crie admin
uv run task cli-setup
```

#### 4. Inicie o Servidor

```bash
# Modo desenvolvimento (com reload)
uvicorn projeto_aplicado.app:app --reload --host 0.0.0.0 --port 8000

# Ou usando uv
uv run uvicorn projeto_aplicado.app:app --reload
```

### 🐳 Docker (Produção)

#### docker-compose.yml

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOSTNAME=db
      - POSTGRES_DB=foodtruck
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=foodtruck
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## 📖 CLI Tools

O sistema inclui uma ferramenta de linha de comando moderna construída com **Cyclopts** seguindo **arquitetura limpa** e princípios **SOLID**.

### 🏗️ Arquitetura CLI

- **🎯 Clean Architecture**: Separação clara entre comandos, serviços e infraestrutura
- **🔧 SOLID Principles**: Fácil extensão e manutenção
- **🧪 100% Testado**: Cobertura completa de testes unitários e integração
- **🚀 Dependency Injection**: Baixo acoplamento entre componentes

### 🎯 Comandos Principais

```bash
# Verificar status do sistema
uv run task cli-health

# Gerenciamento de administradores
uv run task cli-admin create <username> <email> <password> <full_name>
uv run task cli-admin check <email>        # Verificar se admin existe
uv run task cli-admin list-admins          # Listar administradores

# Gerenciamento de banco de dados
uv run task cli-database init              # Inicializar banco com migrações
uv run task cli-database status            # Status do banco e migrações
uv run task cli-database upgrade           # Atualizar migrações
uv run task cli-database create <message>  # Criar nova migração

# Instalação e configuração
uv run task cli-install check              # Verificar dependências
uv run task cli-install setup              # Configurar ambiente
uv run task cli-install status             # Status do sistema

# Informações do sistema
uv run python -m projeto_aplicado.cli.app version
uv run python -m projeto_aplicado.cli.app --help
```

### 💡 Exemplos de Uso

```bash
# Criar um administrador personalizado
uv run task cli-admin create superadmin admin@mycompany.com mysecret123 "Super Administrator"

# Verificação de saúde com output detalhado
uv run task cli-health
# 🏥 System Health Check
# ✓ Database connection: OK
# ✓ Admin users: 2 found  
# ✓ Settings loaded: OK
#   Database: foodtruck
#   Host: localhost:5432
# 🎉 All 3 health checks passed!

# Verificar se um admin específico existe
uv run task cli-admin check admin@foodtruck.com
# ✓ User found: admin (admin@foodtruck.com) - System Administrator

# Listar todos os administradores
uv run task cli-admin list-admins
# ✓ Found 2 admin user(s):
#   • admin (admin@foodtruck.com) - System Administrator
#   • superadmin (admin@mycompany.com) - Super Administrator

# Verificar status do banco de dados
uv run task cli-database status
# 📊 Database Status
# ✓ Database connection: OK
# ✓ Alembic configuration: OK
# ✓ Migrations directory: Found
# ℹ Current migration: ca713c51cd3c (head)

# Verificar dependências do sistema
uv run task cli-install check
# 🔍 Dependency Check
# ✓ python: Python 3.13.6
# ✓ uv: uv 0.8.8
# ✓ git: git version 2.34.1
# ✓ docker: Docker version 28.3.2

# Usar com Docker (ambiente de produção)
docker-compose exec api uv run task cli-health --db-host postgres
```

### 🔧 Comandos de Desenvolvimento

```bash
# Comandos do taskipy (uv run task <comando>)
uv run task test           # Executar testes
uv run task test-cov       # Testes com cobertura
uv run task lint           # Verificar código
uv run task format         # Formatar código
uv run task dev            # Servidor desenvolvimento

# Comandos específicos do CLI
uv run task cli            # CLI interativo
uv run task cli-health     # Verificação de saúde
uv run task cli-admin      # Comandos de administrador
uv run task cli-database   # Comandos de banco de dados
uv run task cli-install    # Comandos de instalação

# Migrações de banco de dados
uv run task migrate-create <message>  # Criar migração
uv run task migrate-upgrade           # Aplicar migrações
uv run task migrate-current           # Migração atual
```

### 🏗️ Estrutura da Arquitetura CLI

```
projeto_aplicado/cli/
├── 📱 app.py                   # Factory do app CLI (Clean Architecture)
├── 🏛️ base/                    # Classes abstratas (SOLID)
│   ├── command.py             # BaseCommand (SRP + OCP)
│   └── service.py             # BaseService (SRP + ISP)
├── 🎮 commands/                # Comandos CLI (SRP)
│   ├── admin.py               # Gerenciamento de admins
│   ├── database.py            # Comandos de banco e migrações
│   ├── health.py              # Verificações de saúde
│   └── install.py             # Comandos de instalação
├── ⚙️ services/                # Lógica de negócio (SRP + DIP)
│   ├── database.py            # Conexão e operações DB
│   ├── health.py              # Lógica de health checks
│   ├── installer.py           # Instalação e configuração
│   ├── migration.py           # Operações de migração
│   └── user.py                # Operações de usuário
└── 🧪 tests/                   # Testes abrangentes
    ├── test_app.py            # Testes de integração
    ├── test_commands.py       # Testes unitários comandos
    ├── test_services.py       # Testes unitários serviços
    └── test_integration.py    # Testes end-to-end
```

## 🧪 Testes

O projeto possui uma suíte de testes abrangente com **175 testes** e **94% de cobertura**, incluindo **71 testes dedicados** à nova arquitetura CLI.

### 🏃‍♂️ Executando Testes

```bash
# Todos os testes
uv run task test

# Com relatório de cobertura
uv run task test-cov

# Testes específicos da API
uv run pytest tests/test_api_orders.py -v

# Testes específicos do CLI
uv run pytest projeto_aplicado/cli/tests/ -v

# Testes com saída detalhada
uv run pytest -v -s

# Executar um teste específico
uv run pytest tests/test_api_orders.py::test_create_order -v

# Testes CLI específicos
uv run pytest projeto_aplicado/cli/tests/test_services.py::TestDatabaseService -v
```

### 📊 Estrutura de Testes

```
tests/                                    # Testes principais (104 testes)
├── 🔐 test_auth/                        # Testes de autenticação
├── 🌐 test_api_*.py                     # Testes de integração da API
├── ⚙️  conftest.py                      # Configurações compartilhadas
└── 📝 test_*.py                        # Testes unitários

projeto_aplicado/cli/tests/              # Testes CLI (71 testes)
├── 🧪 test_services.py                 # Testes unitários dos serviços
├── 🎮 test_commands.py                 # Testes unitários dos comandos
├── 📱 test_app.py                      # Testes de integração do app
├── 🔄 test_integration.py              # Testes end-to-end
├── ⚙️  conftest.py                     # Configurações CLI
└── 📖 README.md                        # Documentação dos testes
```

### 🎯 Cobertura de Testes

| Categoria | Testes | Cobertura | Status |
|-----------|--------|-----------|--------|
| **🌐 API** | 104 | 94% | ✅ Completa |
| **🛠️ CLI Services** | 20 | 100% | ✅ Completa |
| **🎮 CLI Commands** | 25 | 100% | ✅ Completa |
| **🔄 CLI Integration** | 26 | 100% | ✅ Completa |
| **📊 Total** | **175** | **94%** | ✅ **Excelente** |

## 📚 Documentação da API

### 🌐 Acessando a Documentação

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI JSON**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

### 🗺️ Mapa de Endpoints

| Método | Endpoint | Descrição | Auth | Permissões |
|--------|----------|-----------|------|------------|
| **🔐 Autenticação** |
| `POST` | `/api/v1/token` | Gerar token JWT | ❌ | Público |
| **👥 Usuários** |
| `GET` | `/api/v1/users` | Listar usuários | ✅ | Admin |
| `GET` | `/api/v1/users/{id}` | Obter usuário | ✅ | Admin |
| `POST` | `/api/v1/users` | Criar usuário | ✅ | Admin |
| `PATCH` | `/api/v1/users/{id}` | Atualizar usuário | ✅ | Admin |
| `DELETE` | `/api/v1/users/{id}` | Deletar usuário | ✅ | Admin |
| **🍔 Produtos** |
| `GET` | `/api/v1/products` | Listar produtos | ✅ | Todos |
| `GET` | `/api/v1/products/{id}` | Obter produto | ✅ | Todos |
| `POST` | `/api/v1/products` | Criar produto | ✅ | Admin |
| `PUT` | `/api/v1/products/{id}` | Atualizar produto | ✅ | Admin |
| `PATCH` | `/api/v1/products/{id}` | Atualizar parcialmente | ✅ | Admin |
| `DELETE` | `/api/v1/products/{id}` | Deletar produto | ✅ | Admin |
| **🛍️ Pedidos** |
| `GET` | `/api/v1/orders` | Listar pedidos | ✅ | Todos |
| `GET` | `/api/v1/orders/{id}` | Obter pedido | ✅ | Todos |
| `GET` | `/api/v1/orders/{id}/items` | Listar itens | ✅ | Todos |
| `POST` | `/api/v1/orders` | Criar pedido | ✅ | Admin, Atendente |
| `PATCH` | `/api/v1/orders/{id}` | Atualizar pedido | ✅ | Admin, Atendente, Cozinha |
| `DELETE` | `/api/v1/orders/{id}` | Deletar pedido | ✅ | Admin, Atendente |

### 🔑 Autenticação

#### Obter Token

```http
POST /api/v1/token
Content-Type: application/x-www-form-urlencoded

username=admin@foodtruck.com&password=admin123
```

**Resposta:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

#### Usar Token

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 📄 Exemplos de Uso

#### 🍔 Criar Produto

```http
POST /api/v1/products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "X-Burger Especial",
  "description": "Hambúrguer artesanal com queijo coalho",
  "price": 28.90,
    "category": "burger",
  "image_url": "https://example.com/x-burger.jpg",
    "is_available": true
}
```

#### 🛍️ Criar Pedido

```http
POST /api/v1/orders
Authorization: Bearer <token>
Content-Type: application/json

{
    "items": [
        {
      "product_id": "01HXAMPLE1234567890",
      "quantity": 2
    },
    {
      "product_id": "01HXAMPLE0987654321", 
      "quantity": 1
    }
  ],
  "notes": "Sem cebola no primeiro burger"
}
```

### 📊 Códigos de Status

| Código | Significado | Descrição |
|--------|-------------|-----------|
| `200` | ✅ OK | Requisição bem-sucedida |
| `201` | ✅ Created | Recurso criado com sucesso |
| `400` | ❌ Bad Request | Dados inválidos na requisição |
| `401` | 🔒 Unauthorized | Token de autenticação inválido |
| `403` | 🚫 Forbidden | Usuário sem permissão |
| `404` | 🔍 Not Found | Recurso não encontrado |
| `409` | ⚠️ Conflict | Conflito de dados (ex: email já existe) |
| `422` | 📝 Unprocessable Entity | Erro de validação |
| `429` | 🐌 Too Many Requests | Limite de requisições excedido |
| `500` | 💥 Internal Server Error | Erro interno do servidor |

## 🔒 Segurança

### 🛡️ Medidas Implementadas

- **Hash de Senhas**: Argon2ID com salt automático
- **JWT Tokens**: Assinatura HMAC com chave secreta
- **Validação de Entrada**: Pydantic para todos os DTOs
- **CORS Configurado**: Proteção contra requisições cross-origin
- **Rate Limiting**: *Planejado* para versões futuras
- **SQL Injection**: Proteção via SQLModel/SQLAlchemy

### ⚠️ Avisos de Segurança

> **🚨 IMPORTANTE**: Esta configuração é para desenvolvimento. Em produção:
>
> - [ ] Altere `SECRET_KEY` para um valor criptograficamente seguro
> - [ ] Configure CORS adequadamente (remova `allow_origins=['*']`)
> - [ ] Use HTTPS em produção
> - [ ] Implemente rate limiting
> - [ ] Configure logs de auditoria

## 🤝 Contribuição

### 📋 Como Contribuir

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/projeto_aplicado_foodtruck.git`
3. **Crie** uma branch: `git checkout -b feature/minha-feature`
4. **Implemente** suas mudanças
5. **Teste**: `uv run task test`
6. **Commit**: `git commit -m "feat: adiciona nova feature"`
7. **Push**: `git push origin feature/minha-feature`
8. **Abra** um Pull Request

### 🧪 Testes Obrigatórios

- ✅ Todos os novos recursos devem ter testes
- ✅ Cobertura de código > 85%
- ✅ Testes de integração para APIs
- ✅ Testes unitários para business logic

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais detalhes.

---

## 🏗️ Arquitetura CLI (Clean Architecture)

O CLI foi completamente refatorado seguindo princípios de **Clean Architecture** e **SOLID**:

### 🎯 Princípios SOLID Implementados

- **🔧 S**ingle Responsibility: Cada classe tem uma responsabilidade específica
  - `DatabaseService`: Apenas operações de banco de dados
  - `UserService`: Apenas operações de usuário
  - `HealthService`: Apenas verificações de saúde

- **📖 O**pen/Closed: Fácil extensão sem modificação
  - Novos comandos: herdam de `BaseCommand`
  - Novos serviços: herdam de `BaseService`

- **🔄 L**iskov Substitution: Interfaces substituíveis
  - Todos os serviços são intercambiáveis
  - Todos os comandos seguem a mesma interface

- **⚙️ I**nterface Segregation: Interfaces específicas e focadas
  - `BaseService`: Interface mínima para serviços
  - `BaseCommand`: Interface específica para comandos

- **🔀 D**ependency Inversion: Injeção de dependência
  - Commands recebem services via construtor
  - Services recebem dependencies via construtor

### 📚 Benefícios da Nova Arquitetura

| Antes (Monolítico) | Depois (Clean Architecture) |
|---------------------|------------------------------|
| ❌ Código duplicado | ✅ DRY (Don't Repeat Yourself) |
| ❌ Difícil de testar | ✅ 100% de cobertura de testes |
| ❌ Acoplamento forte | ✅ Baixo acoplamento |
| ❌ Difícil de estender | ✅ Fácil extensão |
| ❌ Responsabilidades misturadas | ✅ Separação clara de responsabilidades |

### 🧪 Qualidade dos Testes

- **71 testes dedicados** ao CLI
- **Unit Tests**: Serviços testados isoladamente
- **Integration Tests**: Workflows completos testados
- **Mocking Strategy**: Dependencies mockadas adequadamente
- **Error Handling**: Cenários de erro cobertos

---

## 🔗 Links Úteis

### 📚 Documentação Externa

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLModel Docs](https://sqlmodel.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Cyclopts Docs](https://github.com/BrianPugh/cyclopts) (CLI Framework)
- [pytest Docs](https://docs.pytest.org/)
- [uv Documentation](https://github.com/astral-sh/uv)
- [CLI Tests Documentation](projeto_aplicado/cli/tests/README.md) (Arquitetura CLI)

---

<div align="center">

**Feito com ❤️ pelos alunos do SENAI SC - Florianópolis**

[🐛 Reportar Bug](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues) • 
[💡 Solicitar Feature](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues) • 
[📖 Documentação](https://github.com/bentoluizv/projeto_aplicado_foodtruck/wiki)

</div>
