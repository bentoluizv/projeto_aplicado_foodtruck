# 🚀 Documentação da API do Food Truck

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-blue.svg)](https://spec.openapis.org/oas/v3.1.0)
[![JWT](https://img.shields.io/badge/auth-JWT-orange.svg)](https://jwt.io/)

> **Documentação completa da API REST para o Sistema de Gerenciamento de Food Truck**

## 📋 Índice

- [🎯 Visão Geral da API](#-visão-geral-da-api)
- [🔐 Autenticação](#-autenticação)
- [📊 Referência da API](#-referência-da-api)
- [🔄 Exemplos de Requisição/Resposta](#-exemplos-de-requisiçãoresposta)
- [📝 Modelos de Dados](#-modelos-de-dados)
- [🎭 Funções de Usuário e Permissões](#-funções-de-usuário-e-permissões)
- [⚡ Limitação de Taxa](#-limitação-de-taxa)
- [🛠️ Tratamento de Erros](#️-tratamento-de-erros)
- [🧪 Testando a API](#-testando-a-api)
- [📚 SDKs e Clientes](#-sdks-e-clientes)

## 🎯 Visão Geral da API

O Sistema de Gerenciamento de Food Truck fornece uma API REST abrangente construída com **FastAPI**, apresentando:

- 🚀 **Alto Desempenho** - Construído em ASGI com suporte a async/await
- 📖 **Documentação Interativa** - Documentação automática OpenAPI/Swagger
- 🔒 **Seguro** - Autenticação JWT com controle de acesso baseado em funções
- ✅ **Validado** - Validação automática de requisição/resposta com Pydantic
- 🎯 **Type Safe** - Type hints completos estilo TypeScript
- 📊 **Monitorado** - Verificações de saúde e métricas integradas

### Informações da API

| Propriedade | Valor |
|-------------|-------|
| **URL Base** | `http://localhost:8000` |
| **Versão da API** | v1 |
| **Prefixo da API** | `/api/v1` |
| **Documentação** | `/docs` (Swagger UI) |
| **ReDoc** | `/redoc` (Documentação alternativa) |
| **Schema OpenAPI** | `/openapi.json` |

### Links Rápidos

- **🌐 Documentação Interativa**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **📖 ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **📊 Schema OpenAPI**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- **🔍 Verificação de Saúde**: `foodtruck-cli health` (comando CLI)

## 🔐 Autenticação

A API usa **JWT (JSON Web Tokens)** para autenticação com autorização baseada em funções.

### Obtendo Token de Acesso

**Endpoint**: `POST /api/v1/token/`

```bash
curl -X POST "http://localhost:8000/api/v1/token/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@foodtruck.com&password=admin123"
```

**Resposta**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
    "username": "admin",
    "email": "admin@foodtruck.com",
    "full_name": "Administrador do Sistema",
    "role": "admin",
    "is_active": true
  }
}
```

### Usando Token de Acesso

Inclua o token no cabeçalho `Authorization`:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://localhost:8000/api/v1/users
```

### Informações do Token

| Propriedade | Valor |
|-------------|-------|
| **Algoritmo** | HS256 |
| **Expiração** | 1 hora (3600 segundos) |
| **Refresh** | Não implementado (planejado) |
| **Claims** | sub (user_id), email, role, exp, iat |

## 📊 Referência da API

### 🏥 Saúde e Status

#### Verificação de Saúde do Sistema

**Nota**: Endpoint de saúde está planejado para implementação futura. Atualmente, verificações de saúde estão disponíveis através do CLI:

```bash
# Verificação de saúde CLI
foodtruck-cli health
```

**Endpoint planejado**: `GET /health` (ainda não implementado)

---

### 🔐 Endpoints de Autenticação

#### Login

**`POST /api/v1/token/`**

Autenticar usuário e receber token JWT.

**Requisição**:
```http
Content-Type: application/x-www-form-urlencoded

username=admin@foodtruck.com&password=admin123
```

**Resposta**: [Ver seção Autenticação](#-autenticação)

---

### 👥 Gerenciamento de Usuários

#### Listar Usuários

**`GET /api/v1/users/`**

Obter lista paginada de usuários.

**Autorização**: Apenas admin

**Parâmetros de Query**:
- `skip` (int): Registros para pular (padrão: 0)
- `limit` (int): Registros para retornar (padrão: 100, máximo: 100)

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/users/?skip=0&limit=10"
```

**Resposta**:
```json
{
  "items": [
    {
      "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "username": "admin",
      "email": "admin@foodtruck.com",
      "full_name": "Administrador do Sistema",
      "role": "admin",
      "is_active": true,
      "created_at": "2025-01-09T10:00:00Z",
      "updated_at": "2025-01-09T10:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

#### Obter Usuário por ID

**`GET /api/v1/users/{user_id}`**

Obter usuário específico por ID.

**Autorização**: Apenas admin

```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/users/01HX8P9G6J8K7Q9M5N3P2R1S0T
```

#### Criar Usuário

**`POST /api/v1/users/`**

Criar novo usuário.

**Autorização**: Apenas admin

**Requisição**:
```json
{
  "username": "johndoe",
  "email": "john@foodtruck.com",
  "full_name": "John Doe",
  "password": "secure123",
  "role": "atendente"
}
```

**Resposta**:
```json
{
  "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
  "username": "johndoe",
  "email": "john@foodtruck.com",
  "full_name": "John Doe",
  "role": "atendente",
  "is_active": true,
  "created_at": "2025-01-09T15:30:00Z",
  "updated_at": "2025-01-09T15:30:00Z"
}
```

#### Atualizar Usuário

**`PATCH /api/v1/users/{user_id}`**

Atualizar informações do usuário.

**Autorização**: Apenas admin

**Requisição**:
```json
{
  "full_name": "John Smith",
  "is_active": false
}
```

#### Deletar Usuário

**`DELETE /api/v1/users/{user_id}`**

Deletar usuário.

**Autorização**: Apenas admin

**Resposta**: `204 No Content`

---

### 🍔 Gerenciamento de Produtos

#### Listar Produtos

**`GET /api/v1/products/`**

Obter lista paginada de produtos.

**Autorização**: Todos os usuários autenticados

**Parâmetros de Query**:
- `skip` (int): Registros para pular
- `limit` (int): Registros para retornar
- `category` (str): Filtrar por categoria
- `is_available` (bool): Filtrar por disponibilidade

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/products/?category=burger&is_available=true"
```

**Resposta**:
```json
{
  "items": [
    {
      "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "name": "X-Burger Especial",
      "description": "Hambúrguer artesanal com queijo coalho",
      "price": 28.90,
      "category": "burger",
      "image_url": "https://example.com/x-burger.jpg",
      "is_available": true,
      "created_at": "2025-01-09T10:00:00Z",
      "updated_at": "2025-01-09T10:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Obter Produto por ID

**`GET /api/v1/products/{product_id}`**

Obter produto específico.

**Autorização**: Todos os usuários autenticados

#### Criar Produto

**`POST /api/v1/products/`**

Criar novo produto.

**Autorização**: Apenas admin

**Requisição**:
```json
{
  "name": "X-Burger Especial",
  "description": "Hambúrguer artesanal com queijo coalho",
  "price": 28.90,
  "category": "burger",
  "image_url": "https://example.com/x-burger.jpg",
  "is_available": true
}
```

#### Atualizar Produto

**`PUT /api/v1/products/{product_id}`**

Atualizar produto inteiro.

**Autorização**: Apenas admin

#### Atualização Parcial de Produto

**`PATCH /api/v1/products/{product_id}`**

Atualizar campos específicos do produto.

**Autorização**: Apenas admin

**Requisição**:
```json
{
  "price": 32.90,
  "is_available": false
}
```

#### Deletar Produto

**`DELETE /api/v1/products/{product_id}`**

Deletar produto.

**Autorização**: Apenas admin

---

### 🛍️ Gerenciamento de Pedidos

#### Listar Pedidos

**`GET /api/v1/orders/`**

Obter lista paginada de pedidos.

**Autorização**: Todos os usuários autenticados

**Parâmetros de Query**:
- `skip` (int): Registros para pular
- `limit` (int): Registros para retornar
- `status` (str): Filtrar por status
- `customer_name` (str): Filtrar por nome do cliente

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/orders/?status=pending"
```

**Resposta**:
```json
{
  "items": [
    {
      "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "localizador": "A123",
      "customer_name": "João Silva",
      "status": "pending",
      "total": 57.80,
      "notes": "Sem cebola no primeiro burger",
      "rating": null,
      "items": [
        {
          "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
          "product_id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
          "product_name": "X-Burger Especial",
          "quantity": 2,
          "price": 28.90,
          "subtotal": 57.80
        }
      ],
      "created_at": "2025-01-09T14:00:00Z",
      "updated_at": "2025-01-09T14:00:00Z"
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 100
}
```

#### Obter Pedido por ID

**`GET /api/v1/orders/{order_id}`**

Obter pedido específico com todos os detalhes.

**Autorização**: Todos os usuários autenticados

#### Criar Pedido

**`POST /api/v1/orders/`**

Criar novo pedido.

**Autorização**: Admin, Atendente

**Requisição**:
```json
{
  "customer_name": "João Silva",
  "items": [
    {
      "product_id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "quantity": 2
    },
    {
      "product_id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "quantity": 1
    }
  ],
  "notes": "Sem cebola no primeiro burger"
}
```

**Resposta**:
```json
{
  "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
  "localizador": "A123",
  "customer_name": "João Silva",
  "status": "pending",
  "total": 57.80,
  "notes": "Sem cebola no primeiro burger",
  "items": [
    {
      "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "product_id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "product_name": "X-Burger Especial",
      "quantity": 2,
      "price": 28.90,
      "subtotal": 57.80
    }
  ],
  "created_at": "2025-01-09T14:00:00Z",
  "updated_at": "2025-01-09T14:00:00Z"
}
```

#### Atualizar Status do Pedido

**`PATCH /api/v1/orders/{order_id}`**

Atualizar status do pedido e outros campos.

**Autorização**: Admin, Atendente, Cozinha (apenas status)

**Requisição**:
```json
{
  "status": "preparing"
}
```

#### Obter Itens do Pedido

**`GET /api/v1/orders/{order_id}/items`**

Obter todos os itens para um pedido específico.

**Autorização**: Todos os usuários autenticados

#### Deletar Pedido

**`DELETE /api/v1/orders/{order_id}`**

Deletar pedido (apenas se status for pending).

**Autorização**: Admin, Atendente

---

## 🔄 Exemplos de Requisição/Resposta

### Fluxo Completo de Pedido

#### 1. Criar Pedido

```bash
# Criar novo pedido
curl -X POST "http://localhost:8000/api/v1/orders/" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_name": "Maria Santos",
       "items": [
         {"product_id": "01HX8P9G6J8K7Q9M5N3P2R1S0T", "quantity": 1},
         {"product_id": "01HY9Q0H7K9L8R0N6O4Q3S2T1U", "quantity": 2}
       ],
       "notes": "Entrega balcão 2"
     }'
```

#### 2. Atualizar Status do Pedido (Cozinha)

```bash
# Marcar como preparando
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "preparing"}'
```

#### 3. Completar Pedido

```bash
# Marcar como pronto
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "ready"}'
```

#### 4. Entregar Pedido

```bash
# Marcar como entregue
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "delivered"}'
```

### Exemplo de Gerenciamento de Produto

```bash
# Criar produto
curl -X POST "http://localhost:8000/api/v1/products/" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Batata Frita Premium",
       "description": "Batata frita crocante com temperos especiais",
       "price": 15.90,
       "category": "side",
       "is_available": true
     }'

# Atualizar preço do produto
curl -X PATCH "http://localhost:8000/api/v1/products/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"price": 17.90}'

# Desabilitar produto
curl -X PATCH "http://localhost:8000/api/v1/products/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"is_available": false}'
```

## 📝 Modelos de Dados

### Modelo de Usuário

```json
{
  "id": "string (ULID)",
  "username": "string (único)",
  "email": "string (único, formato email)",
  "full_name": "string",
  "role": "admin | atendente | cozinha",
  "is_active": "boolean",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Modelo de Produto

```json
{
  "id": "string (ULID)",
  "name": "string",
  "description": "string",
  "price": "number (decimal, >= 0)",
  "category": "burger | drink | side | dessert",
  "image_url": "string (URL, opcional)",
  "is_available": "boolean",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Modelo de Pedido

```json
{
  "id": "string (ULID)",
  "localizador": "string (único, auto-gerado)",
  "customer_name": "string",
  "status": "pending | preparing | ready | delivered | cancelled",
  "total": "number (decimal, calculado)",
  "notes": "string (opcional)",
  "rating": "integer (1-5, opcional)",
  "items": [
    {
      "id": "string (ULID)",
      "product_id": "string (ULID)",
      "product_name": "string",
      "quantity": "integer (> 0)",
      "price": "number (decimal)",
      "subtotal": "number (decimal, calculado)"
    }
  ],
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Modelo de Erro

```json
{
  "detail": "string (mensagem de erro)",
  "type": "string (tipo de erro)",
  "code": "string (código de erro, opcional)",
  "field": "string (nome do campo para erros de validação, opcional)"
}
```

## 🎭 Funções de Usuário e Permissões

### Definições de Função

| Função | Descrição | Permissões |
|--------|-----------|------------|
| **👑 admin** | Administrador do sistema | Acesso completo a todos os recursos |
| **👥 atendente** | Atendente de vendas | Pedidos, produtos (leitura), clientes |
| **👨‍🍳 cozinha** | Equipe da cozinha | Pedidos (apenas atualizações de status) |

### Matriz de Permissões

| Recurso | Admin | Atendente | Cozinha |
|---------|-------|-----------|---------|
| **Usuários** | CRUD | - | - |
| **Produtos** | CRUD | Leitura | Leitura |
| **Pedidos** | CRUD | CRUD | Atualizar (status) |
| **Itens do Pedido** | CRUD | CRUD | Leitura |

### Exemplos de Acesso Baseado em Função

```bash
# Admin: Criar usuário
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{"username": "newuser", ...}'

# Atendente: Criar pedido
curl -X POST "http://localhost:8000/api/v1/orders/" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN" \
     -d '{"customer_name": "Cliente", ...}'

# Cozinha: Atualizar apenas status do pedido
curl -X PATCH "http://localhost:8000/api/v1/orders/123" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -d '{"status": "preparing"}'
```

## ⚡ Limitação de Taxa

**Nota**: Limitação de taxa está planejada para implementação futura.

### Limites Planejados

| Tipo de Usuário | Requisições/Minuto | Burst |
|-----------------|-------------------|-------|
| **Admin** | 1000 | 100 |
| **Atendente** | 300 | 50 |
| **Cozinha** | 100 | 20 |
| **Não Autenticado** | 10 | 5 |

### Cabeçalhos de Limite de Taxa (Planejado)

```http
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1640995200
```

## 🛠️ Tratamento de Erros

### Códigos de Status HTTP

| Status | Significado | Quando |
|--------|-------------|--------|
| **200** | OK | GET, PATCH bem-sucedidos |
| **201** | Created | POST bem-sucedido |
| **204** | No Content | DELETE bem-sucedido |
| **400** | Bad Request | Dados de requisição inválidos |
| **401** | Unauthorized | Token de autenticação ausente/inválido |
| **403** | Forbidden | Permissões insuficientes |
| **404** | Not Found | Recurso não encontrado |
| **409** | Conflict | Dados duplicados (email, username) |
| **422** | Unprocessable Entity | Erros de validação |
| **429** | Too Many Requests | Limite de taxa excedido |
| **500** | Internal Server Error | Erro do servidor |

### Formato de Resposta de Erro

```json
{
  "detail": "Email já registrado",
  "type": "validation_error",
  "code": "EMAIL_DUPLICATE"
}
```

### Erros de Validação

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "campo obrigatório",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "price"],
      "msg": "garantir que este valor seja maior que 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

### Cenários de Erro Comuns

#### Erros de Autenticação

```bash
# Token ausente
curl http://localhost:8000/api/v1/users
# Resposta: 401 {"detail": "Não autenticado"}

# Token inválido
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/v1/users
# Resposta: 401 {"detail": "Não foi possível validar credenciais"}

# Token expirado
curl -H "Authorization: Bearer expired-token" http://localhost:8000/api/v1/users
# Resposta: 401 {"detail": "Token expirado"}
```

#### Erros de Permissão

```bash
# Atendente tentando criar usuário
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN"
# Resposta: 403 {"detail": "Permissões insuficientes"}
```

#### Erros de Validação

```bash
# Formato de email inválido
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{"email": "invalid-email"}'
# Resposta: 422 com detalhes de validação
```

## 🧪 Testando a API

### Usando curl

```bash
# Definir URL base e token
BASE_URL="http://localhost:8000"
TOKEN="seu-jwt-token"

# Testar autenticação
curl -X POST "$BASE_URL/api/v1/token/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@foodtruck.com&password=admin123"

# Testar endpoint protegido
curl -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/users/"
```

### Usando HTTPie

```bash
# Instalar HTTPie
pip install httpie

# Login
http POST localhost:8000/api/v1/token/ username=admin@foodtruck.com password=admin123

# Usar token
http GET localhost:8000/api/v1/users/ Authorization:"Bearer $TOKEN"

# Criar pedido
http POST localhost:8000/api/v1/orders/ \
     Authorization:"Bearer $TOKEN" \
     customer_name="Cliente Teste" \
     items:='[{"product_id":"01HX8P9G6J8K7Q9M5N3P2R1S0T","quantity":1}]'
```

### Usando Postman

1. **Importar OpenAPI**: Use `http://localhost:8000/openapi.json`
2. **Definir Variáveis de Ambiente**:
   - `base_url`: `http://localhost:8000`
   - `token`: Seu token JWT
3. **Autenticação**: Adicionar `Authorization: Bearer {{token}}` aos cabeçalhos

### Usando Python Requests

```python
import requests

# Configuração base
BASE_URL = "http://localhost:8000"
session = requests.Session()

# Login
response = session.post(f"{BASE_URL}/api/v1/token", data={
    "username": "admin@foodtruck.com",
    "password": "admin123"
})
token_data = response.json()
session.headers.update({
    "Authorization": f"Bearer {token_data['access_token']}"
})

# Obter usuários
users = session.get(f"{BASE_URL}/api/v1/users").json()
print(f"Encontrados {users['total']} usuários")

# Criar produto
product = session.post(f"{BASE_URL}/api/v1/products", json={
    "name": "Produto Teste",
    "description": "Um produto de teste",
    "price": 10.99,
    "category": "burger",
    "is_available": True
}).json()
print(f"Produto criado: {product['id']}")
```

## 📚 SDKs e Clientes

### Gerar Bibliotecas Cliente

Use geradores OpenAPI para criar bibliotecas cliente:

```bash
# Cliente Python
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o python-client

# Cliente TypeScript/JavaScript
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-fetch \
  -o typescript-client

# Cliente Java
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g java \
  -o java-client
```

### Exemplo de SDK Python

```python
# Uso do cliente gerado
from foodtruck_client import ApiClient, Configuration, UsersApi

config = Configuration(host="http://localhost:8000")
config.access_token = "seu-jwt-token"

with ApiClient(config) as api_client:
    users_api = UsersApi(api_client)
    users = users_api.get_users()
    print(f"Total de usuários: {users.total}")
```

### Integração Frontend (JavaScript)

```javascript
// API fetch moderna
class FoodTruckAPI {
  constructor(baseURL, token) {
    this.baseURL = baseURL;
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.token}`,
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);
    
    if (!response.ok) {
      throw new Error(`Erro da API: ${response.status}`);
    }
    
    return response.json();
  }

  // Autenticação
  async login(username, password) {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch(`${this.baseURL}/api/v1/token`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    this.token = data.access_token;
    return data;
  }

  // Produtos
  async getProducts(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/api/v1/products?${query}`);
  }

  async createProduct(product) {
    return this.request('/api/v1/products', {
      method: 'POST',
      body: JSON.stringify(product),
    });
  }

  // Pedidos
  async getOrders(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/api/v1/orders?${query}`);
  }

  async createOrder(order) {
    return this.request('/api/v1/orders', {
      method: 'POST',
      body: JSON.stringify(order),
    });
  }

  async updateOrderStatus(orderId, status) {
    return this.request(`/api/v1/orders/${orderId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  }
}

// Uso
const api = new FoodTruckAPI('http://localhost:8000');

// Login
await api.login('admin@foodtruck.com', 'admin123');

// Obter produtos
const products = await api.getProducts({ category: 'burger' });
console.log(`Encontrados ${products.total} hambúrgueres`);

// Criar pedido
const order = await api.createOrder({
  customer_name: 'João Doe',
  items: [
    { product_id: 'product-123', quantity: 2 }
  ]
});
console.log(`Pedido criado: ${order.localizador}`);
```

---

## 🔗 Documentação Relacionada

- **🚀 [Guia de Instalação](INSTALL.md)** - Configuração e setup da API
- **🛠️ [Guia de Desenvolvimento](DEVELOPMENT.md)** - Fluxos de trabalho de desenvolvimento da API
- **🧪 [Guia de Testes](../projeto_aplicado/cli/tests/README.md)** - Estratégias de teste da API
- **🚀 [Guia de Implantação](DEPLOYMENT.md)** - Implantação da API em produção

---

<div align="center">

**🚀 API REST Poderosa para Gerenciamento de Food Truck**

[🏠 Índice da Documentação](README.md) • [🌐 Documentação Interativa](http://localhost:8000/docs) • [🐛 Reportar Problema](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)

</div>
