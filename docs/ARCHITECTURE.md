# 🏗️ System Architecture Overview

## 📋 **Architecture Philosophy**

The Food Truck Management System follows a **layered architecture** with **domain-driven design** principles, built on FastAPI with a clear separation of concerns across presentation, business, and data layers.

### **🎯 Architectural Patterns**

- **Layered Architecture**: Clear separation between presentation, business, and data layers
- **Repository Pattern**: Data access abstraction
- **Domain-Driven Design**: Business logic organized around domain entities
- **Clean Architecture Influences**: Dependency inversion for business logic isolation

---

## 🏛️ **System Architecture Diagram**

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI Controllers  │  Authentication  │  Input Validation    │
│  (HTTP endpoints)     │  (JWT middleware) │  (Pydantic schemas) │
├─────────────────────────────────────────────────────────────────┤
│                         BUSINESS LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│   Domain Entities     │   Business Logic │   Domain Services    │
│   (User, Order,       │   (Order workflow,│   (Calculations,    │
│   Product models)     │   Validations)    │   Notifications)    │
├─────────────────────────────────────────────────────────────────┤
│                           DATA LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│    Repositories       │    Database ORM   │    External APIs    │
│    (Data access)      │    (SQLModel)     │    (Future: Payment,│
│                       │                   │     Notifications)  │
├─────────────────────────────────────────────────────────────────┤
│                      INFRASTRUCTURE LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│  PostgreSQL Database  │  Redis Cache      │  Docker Containers  │
│  Alembic Migrations   │  CORS & Security  │  Environment Config │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📂 **Current Project Structure**

```
projeto_aplicado/
├── app.py                    # 🚀 FastAPI application entry point
├── settings.py               # ⚙️  Configuration management  
├── utils.py                  # 🛠️  Utility functions
├── auth/                     # 🔐 Authentication & Security
│   ├── security.py          #     JWT security functions
│   ├── token.py             #     Token generation endpoints
│   └── password.py          #     Password hashing utilities
├── ext/                      # 🔌 External integrations
│   ├── database/            #     Database connections
│   │   └── db.py           #     SQLModel setup & sessions
│   └── cache/               #     Redis caching (planned)
│       └── redis.py        #     Cache configuration
└── resources/               # 🏢 Domain Resources (DDD approach)
    ├── user/                #     User domain
    │   ├── controller.py   #     HTTP endpoints
    │   ├── model.py        #     User entity
    │   ├── repository.py   #     Data access
    │   └── schemas.py      #     DTOs & validation
    ├── product/             #     Product domain
    │   ├── controller.py   #     Product endpoints
    │   ├── model.py        #     Product entity
    │   ├── repository.py   #     Product data access
    │   ├── schemas.py      #     Product DTOs
    │   └── enums.py        #     Product categories
    ├── order/               #     Order domain
    │   ├── controller.py   #     Order endpoints
    │   ├── model.py        #     Order & OrderItem entities
    │   ├── repository.py   #     Order data access
    │   ├── schemas.py      #     Order DTOs
    │   └── enums.py        #     Order status workflow
    └── shared/              #     Shared components
        ├── model.py        #     Base entity model
        ├── repository.py   #     Base repository pattern
        └── schemas.py      #     Common DTOs
```

---

## 🌐 **Component Architecture**

### **1. Presentation Layer (FastAPI Controllers)**

**Purpose**: Handle HTTP requests/responses, input validation, authentication

```python
# Responsibilities:
- Route definition and HTTP method handling
- Request/response serialization (Pydantic)
- Authentication/authorization via dependencies
- Error handling and status code management
- Minimal business logic (delegation to services)
```

**Key Files**: `*/controller.py`, `auth/token.py`

### **2. Business Layer (Domain Models & Logic)**

**Purpose**: Core business rules, domain entities, workflow management

```python
# Responsibilities:
- Domain entity definitions (User, Order, Product)
- Business rule validation
- Domain-specific calculations
- State management (order workflow)
- Cross-domain business logic
```

**Key Files**: `*/model.py`, `*/enums.py`, business services (future)

### **3. Data Layer (Repositories & ORM)**

**Purpose**: Data persistence, query optimization, external data sources

```python
# Responsibilities:
- Database CRUD operations
- Query optimization and caching
- Data mapping between domain and persistence
- Transaction management
- Migration handling (Alembic)
```

**Key Files**: `*/repository.py`, `ext/database/db.py`, `migrations/`

### **4. Infrastructure Layer**

**Purpose**: External concerns, configuration, deployment

```python
# Responsibilities:
- Database connection management
- Authentication infrastructure (JWT)
- CORS and security middleware
- Environment configuration
- Logging and monitoring
- Container orchestration
```

**Key Files**: `settings.py`, `app.py`, `docker-compose.yaml`

---

## 🔄 **Data Flow Architecture**

### **Request Processing Flow**
```
1. HTTP Request → FastAPI Router
2. Middleware → Authentication & CORS
3. Controller → Input validation (Pydantic)
4. Controller → Business logic delegation
5. Repository → Database queries (SQLModel)
6. Database → PostgreSQL operations
7. Response → JSON serialization
8. HTTP Response → Client
```

### **Domain Interaction Patterns**

```
User Domain ←→ Authentication Layer
     ↓
Order Domain ←→ Product Domain
     ↓
Order Items ←→ Price Calculations
     ↓
Database Layer ←→ PostgreSQL
```

---

## 🗄️ **Database Architecture**

### **Entity Relationship Overview**
```sql
Users (1) ────────── (N) Orders
               │
Orders (1) ─────── (N) OrderItems  
               │
OrderItems (N) ── (1) Products
```

### **Database Design Principles**
- **SQLModel ORM**: Type-safe database operations
- **ULID Primary Keys**: Globally unique, sortable identifiers
- **Soft Deletes**: Audit trail preservation (planned)
- **Optimistic Locking**: Concurrent update handling (planned)
- **Database Migrations**: Alembic version control

### **Performance Considerations**
- **Connection Pooling**: SQLModel/SQLAlchemy managed
- **Query Optimization**: Repository pattern for complex queries
- **Caching Strategy**: Redis for frequently accessed data (planned)
- **Read Replicas**: Horizontal scaling support (planned)

---

## 🔐 **Security Architecture**

### **Authentication Flow**
```
1. User Credentials → Password Validation (Argon2)
2. Valid User → JWT Token Generation (HS256)
3. Subsequent Requests → JWT Middleware Validation
4. Valid Token → User Context Injection
5. Endpoint Access → Role-based Authorization
```

### **Security Layers**
- **Transport Security**: HTTPS enforcement
- **Authentication**: JWT with secure secret management
- **Authorization**: Role-based access control (RBAC)
- **Input Validation**: Pydantic schema validation
- **CORS Protection**: Environment-specific origin restrictions
- **Password Security**: Argon2 hashing algorithm

---

## 🚀 **Deployment Architecture**

### **Development Environment**
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   FastAPI   │  │ PostgreSQL  │  │    Redis    │
│  (Local)    │  │  (Docker)   │  │  (Docker)   │
│ Port: 8000  │  │ Port: 5432  │  │ Port: 6379  │
└─────────────┘  └─────────────┘  └─────────────┘
```

### **Production Architecture**
```
┌─────────────────────────────────────────────────────┐
│                    Load Balancer                    │
│                (Traefik/Nginx/Caddy)                │
├─────────────────────────────────────────────────────┤
│  FastAPI App    │  FastAPI App    │  FastAPI App    │
│  (Container 1)  │  (Container 2)  │  (Container 3)  │
├─────────────────────────────────────────────────────┤
│            Database Cluster (PostgreSQL)            │
│                 Primary + Replicas                  │
├─────────────────────────────────────────────────────┤
│            Cache Layer (Redis Cluster)              │
│              Session + Application Cache            │
└─────────────────────────────────────────────────────┘
```

### **Container Architecture**
- **Application Containers**: Multi-stage Docker builds
- **Database Container**: PostgreSQL with persistent volumes
- **Cache Container**: Redis for session and application caching
- **Reverse Proxy**: Traefik for load balancing and SSL termination
- **Monitoring**: Prometheus + Grafana (planned)

---

## 🔧 **Technology Stack Rationale**

### **Backend Framework: FastAPI**
- **Async Support**: High-performance async/await
- **Type Safety**: Native Python type hints
- **Auto Documentation**: OpenAPI/Swagger generation
- **Validation**: Automatic request/response validation
- **Modern Python**: Python 3.11+ features

### **Database: PostgreSQL + SQLModel**
- **ACID Compliance**: Data consistency and reliability
- **JSON Support**: Flexible schema evolution
- **Performance**: Proven enterprise-grade performance
- **Type Safety**: SQLModel bridges Pydantic and SQLAlchemy
- **Migration Support**: Alembic version control

### **Authentication: JWT**
- **Stateless**: Scalable authentication
- **Standards-Based**: RFC 7519 compliance
- **Role-Based**: Fine-grained authorization
- **Secure**: HS256 algorithm with secret rotation

### **Infrastructure: Docker + Docker Compose**
- **Consistency**: Development/production parity
- **Isolation**: Service isolation and dependency management
- **Scalability**: Container orchestration ready
- **Portability**: Cloud-agnostic deployment

---

## 🔮 **Future Architecture Evolution**

### **Phase 1: Current State (MVP)**
- ✅ Basic CRUD operations
- ✅ JWT authentication
- ✅ Role-based authorization
- ✅ Database persistence

### **Phase 2: Service Enhancement (3-6 months)**
- 🔄 Service layer extraction
- 🔄 Event-driven architecture
- 🔄 Advanced caching
- 🔄 Background job processing

---

## 🔗 **Related Documentation**

- **[Code Quality Analysis](CODE_QUALITY.md)** - Design patterns, SOLID principles, code smells
- **[Development Guide](DEVELOPMENT.md)** - Setup and development workflows
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment strategies
- **[Testing Guide](../projeto_aplicado/cli/tests/README.md)** - Testing architecture and strategies