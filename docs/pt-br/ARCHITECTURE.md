# 🏗️ Visão Geral da Arquitetura do Sistema

## 📋 **Filosofia da Arquitetura**

O Sistema de Gerenciamento de Food Truck segue uma **arquitetura em camadas** com princípios de **design orientado a domínio**, construído em FastAPI com separação clara de responsabilidades entre camadas de apresentação, negócio e dados.

### **🎯 Padrões Arquiteturais**

- **Arquitetura em Camadas**: Separação clara entre camadas de apresentação, negócio e dados
- **Padrão Repository**: Abstração de acesso a dados
- **Design Orientado a Domínio**: Lógica de negócio organizada em torno de entidades de domínio
- **Influências da Arquitetura Limpa**: Inversão de dependência para isolamento da lógica de negócio

---

## 🏛️ **Diagrama da Arquitetura do Sistema**

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                       │
├─────────────────────────────────────────────────────────────────┤
│  Controladores FastAPI  │  Autenticação  │  Validação de Entrada │
│  (endpoints HTTP)       │  (middleware JWT) │  (schemas Pydantic) │
├─────────────────────────────────────────────────────────────────┤
│                        CAMADA DE NEGÓCIO                        │
├─────────────────────────────────────────────────────────────────┤
│   Entidades de Domínio  │   Lógica de Negócio │   Serviços de Domínio │
│   (User, Order,         │   (workflow de pedido,│   (Cálculos,    │
│   Product models)       │   Validações)    │   Notificações)    │
├─────────────────────────────────────────────────────────────────┤
│                          CAMADA DE DADOS                        │
├─────────────────────────────────────────────────────────────────┤
│    Repositórios         │    ORM do Banco    │    APIs Externas    │
│    (Acesso a dados)     │    (SQLModel)     │    (Futuro: Pagamento,│
│                         │                   │     Notificações)  │
├─────────────────────────────────────────────────────────────────┤
│                    CAMADA DE INFRAESTRUTURA                     │
├─────────────────────────────────────────────────────────────────┤
│  Banco PostgreSQL  │  Cache Redis      │  Containers Docker  │
│  Migrações Alembic   │  CORS & Segurança  │  Config de Ambiente │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 **Estrutura Atual do Projeto**

```
projeto_aplicado/
├── app.py                    # 🚀 Ponto de entrada da aplicação FastAPI
├── settings.py               # ⚙️  Gerenciamento de configuração  
├── utils.py                  # 🛠️  Funções utilitárias
├── auth/                     # 🔐 Autenticação e Segurança
│   ├── security.py          #     Funções de segurança JWT
│   ├── token.py             #     Endpoints de geração de token
│   └── password.py          #     Utilitários de hash de senha
├── ext/                      # 🔌 Integrações externas
│   ├── database/            #     Conexões de banco de dados
│   │   └── db.py           #     Configuração SQLModel e sessões
│   └── cache/               #     Cache Redis (planejado)
│       └── redis.py        #     Configuração de cache
└── resources/               # 🏢 Recursos de Domínio (abordagem DDD)
    ├── user/                #     Domínio de usuário
    │   ├── controller.py   #     Endpoints HTTP
    │   ├── model.py        #     Entidade User
    │   ├── repository.py   #     Acesso a dados
    │   └── schemas.py      #     DTOs e validação
    ├── product/             #     Domínio de produto
    │   ├── controller.py   #     Endpoints de produto
    │   ├── model.py        #     Entidade Product
    │   ├── repository.py   #     Acesso a dados de produto
    │   ├── schemas.py      #     DTOs de produto
    │   └── enums.py        #     Categorias de produto
    ├── order/               #     Domínio de pedido
    │   ├── controller.py   #     Endpoints de pedido
    │   ├── model.py        #     Entidades Order e OrderItem
    │   ├── repository.py   #     Acesso a dados de pedido
    │   ├── schemas.py      #     DTOs de pedido
    │   └── enums.py        #     Workflow de status de pedido
    └── shared/              #     Componentes compartilhados
        ├── model.py        #     Modelo de entidade base
        ├── repository.py   #     Padrão repository base
        └── schemas.py      #     DTOs comuns
```

---

## 🌐 **Arquitetura de Componentes**

### **1. Camada de Apresentação (Controladores FastAPI)**

**Propósito**: Lidar com requisições/respostas HTTP, validação de entrada, autenticação

```python
# Responsabilidades:
- Definição de rotas e tratamento de métodos HTTP
- Serialização de requisição/resposta (Pydantic)
- Autenticação/autorização via dependências
- Tratamento de erros e gerenciamento de códigos de status
- Lógica de negócio mínima (delegação para serviços)
```

**Arquivos Principais**: `*/controller.py`, `auth/token.py`

### **2. Camada de Negócio (Modelos de Domínio e Lógica)**

**Propósito**: Regras de negócio principais, entidades de domínio, gerenciamento de workflow

```python
# Responsabilidades:
- Definições de entidades de domínio (User, Order, Product)
- Validação de regras de negócio
- Cálculos específicos do domínio
- Gerenciamento de estado (workflow de pedido)
- Lógica de negócio entre domínios
```

**Arquivos Principais**: `*/model.py`, `*/enums.py`, serviços de negócio (futuro)

### **3. Camada de Dados (Repositórios e ORM)**

**Propósito**: Persistência de dados, otimização de consultas, fontes de dados externas

```python
# Responsabilidades:
- Operações CRUD do banco de dados
- Otimização de consultas e cache
- Mapeamento de dados entre domínio e persistência
- Gerenciamento de transações
- Tratamento de migrações (Alembic)
```

**Arquivos Principais**: `*/repository.py`, `ext/database/db.py`, `migrations/`

### **4. Camada de Infraestrutura**

**Propósito**: Preocupações externas, configuração, implantação

```python
# Responsabilidades:
- Gerenciamento de conexões de banco de dados
- Infraestrutura de autenticação (JWT)
- CORS e middleware de segurança
- Configuração de ambiente
- Logging e monitoramento
- Orquestração de containers
```

**Arquivos Principais**: `settings.py`, `app.py`, `docker-compose.yaml`

---

## 🔄 **Arquitetura de Fluxo de Dados**

### **Fluxo de Processamento de Requisição**
```
1. Requisição HTTP → Router FastAPI
2. Middleware → Autenticação e CORS
3. Controlador → Validação de entrada (Pydantic)
4. Controlador → Delegação de lógica de negócio
5. Repositório → Consultas de banco (SQLModel)
6. Banco → Operações PostgreSQL
7. Resposta → Serialização JSON
8. Resposta HTTP → Cliente
```

### **Padrões de Interação de Domínio**

```
Domínio User ←→ Camada de Autenticação
     ↓
Domínio Order ←→ Domínio Product
     ↓
Order Items ←→ Cálculos de Preço
     ↓
Camada de Banco ←→ PostgreSQL
```

---

## 🗄️ **Arquitetura do Banco de Dados**

### **Visão Geral do Relacionamento de Entidades**
```sql
Users (1) ────────── (N) Orders
               │
Orders (1) ─────── (N) OrderItems  
               │
OrderItems (N) ── (1) Products
```

### **Princípios de Design do Banco de Dados**
- **SQLModel ORM**: Operações de banco type-safe
- **Chaves Primárias ULID**: Identificadores globalmente únicos e ordenáveis
- **Soft Deletes**: Preservação de trilha de auditoria (planejado)
- **Locking Otimista**: Tratamento de atualizações concorrentes (planejado)
- **Migrações de Banco**: Controle de versão Alembic

### **Considerações de Performance**
- **Connection Pooling**: Gerenciado por SQLModel/SQLAlchemy
- **Otimização de Consultas**: Padrão repository para consultas complexas
- **Estratégia de Cache**: Redis para dados frequentemente acessados (planejado)
- **Read Replicas**: Suporte a escalabilidade horizontal (planejado)

---

## 🔐 **Arquitetura de Segurança**

### **Fluxo de Autenticação**
```
1. Credenciais do Usuário → Validação de Senha (Argon2)
2. Usuário Válido → Geração de Token JWT (HS256)
3. Requisições Subsequentes → Validação de Middleware JWT
4. Token Válido → Injeção de Contexto do Usuário
5. Acesso ao Endpoint → Autorização baseada em função
```

### **Camadas de Segurança**
- **Segurança de Transporte**: Aplicação de HTTPS
- **Autenticação**: JWT com gerenciamento seguro de segredos
- **Autorização**: Controle de acesso baseado em função (RBAC)
- **Validação de Entrada**: Validação de schema Pydantic
- **Proteção CORS**: Restrições de origem específicas do ambiente
- **Segurança de Senha**: Algoritmo de hash Argon2

---

## 🚀 **Arquitetura de Implantação**

### **Ambiente de Desenvolvimento**
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   FastAPI   │  │ PostgreSQL  │  │    Redis    │
│  (Local)    │  │  (Docker)   │  │  (Docker)   │
│ Porta: 8000 │  │ Porta: 5432 │  │ Porta: 6379 │
└─────────────┘  └─────────────┘  └─────────────┘
```

### **Arquitetura de Produção**
```
┌─────────────────────────────────────────────────────┐
│                    Load Balancer                    │
│                (Traefik/Nginx/Caddy)                │
├─────────────────────────────────────────────────────┤
│  App FastAPI    │  App FastAPI    │  App FastAPI    │
│  (Container 1)  │  (Container 2)  │  (Container 3)  │
├─────────────────────────────────────────────────────┤
│            Cluster de Banco (PostgreSQL)            │
│                 Primário + Réplicas                 │
├─────────────────────────────────────────────────────┤
│            Camada de Cache (Cluster Redis)          │
│              Sessão + Cache da Aplicação            │
└─────────────────────────────────────────────────────┘
```

### **Arquitetura de Containers**
- **Containers de Aplicação**: Builds Docker multi-estágio
- **Container de Banco**: PostgreSQL com volumes persistentes
- **Container de Cache**: Redis para cache de sessão e aplicação
- **Proxy Reverso**: Traefik para load balancing e terminação SSL
- **Monitoramento**: Prometheus + Grafana (planejado)

---

## 🔧 **Justificativa da Stack Tecnológica**

### **Framework Backend: FastAPI**
- **Suporte Async**: Alto desempenho async/await
- **Type Safety**: Type hints nativos do Python
- **Documentação Automática**: Geração OpenAPI/Swagger
- **Validação**: Validação automática de requisição/resposta
- **Python Moderno**: Recursos Python 3.11+

### **Banco de Dados: PostgreSQL + SQLModel**
- **Conformidade ACID**: Consistência e confiabilidade de dados
- **Suporte JSON**: Evolução de schema flexível
- **Performance**: Performance comprovada de nível empresarial
- **Type Safety**: SQLModel conecta Pydantic e SQLAlchemy
- **Suporte a Migrações**: Controle de versão Alembic

### **Autenticação: JWT**
- **Stateless**: Autenticação escalável
- **Baseado em Padrões**: Conformidade RFC 7519
- **Baseado em Função**: Autorização granular
- **Seguro**: Algoritmo HS256 com rotação de segredos

### **Infraestrutura: Docker + Docker Compose**
- **Consistência**: Paridade desenvolvimento/produção
- **Isolamento**: Isolamento de serviço e gerenciamento de dependências
- **Escalabilidade**: Pronto para orquestração de containers
- **Portabilidade**: Implantação agnóstica à nuvem

---

## 🔮 **Evolução Futura da Arquitetura**

### **Fase 1: Estado Atual (MVP)**
- ✅ Operações CRUD básicas
- ✅ Autenticação JWT
- ✅ Autorização baseada em função
- ✅ Persistência de banco de dados

### **Fase 2: Aprimoramento de Serviços (3-6 meses)**
- 🔄 Extração de camada de serviço
- 🔄 Arquitetura orientada a eventos
- 🔄 Cache avançado
- 🔄 Processamento de jobs em background

---

## 🔗 **Documentação Relacionada**

- **[Análise de Qualidade de Código](CODE_QUALITY.md)** - Padrões de design, princípios SOLID, code smells
- **[Guia de Desenvolvimento](DEVELOPMENT.md)** - Configuração e fluxos de trabalho de desenvolvimento
- **[Guia de Implantação](DEPLOYMENT.md)** - Estratégias de implantação em produção
- **[Guia de Testes](../projeto_aplicado/cli/tests/README.md)** - Arquitetura de testes e estratégias
