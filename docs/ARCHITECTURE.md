# 🏗️ Architecture Analysis & TODOs

## 📋 **Current Architecture Overview**

The Food Truck Management System follows a **layered architecture** with FastAPI at its core. This analysis covers the main application structure (excluding CLI components).

### **🎯 Current Project Structure**
```
projeto_aplicado/
├── app.py                    # FastAPI application entry point
├── settings.py               # Configuration management  
├── utils.py                  # Utility functions
├── auth/                     # Authentication layer
│   ├── security.py          # JWT security functions
│   ├── token.py             # Token endpoints
│   └── password.py          # Password hashing
├── ext/
│   └── database/
│       └── db.py            # Database connection management
└── resources/               # Domain resources (Clean Architecture style)
    ├── user/                # User domain
    ├── product/             # Product domain
    ├── order/               # Order domain
    └── shared/              # Shared components
        ├── model.py         # Base model
        ├── repository.py    # Base repository
        └── schemas.py       # Shared DTOs
```

---

## ✅ **Architecture Strengths**

### **1. Domain Organization**
- ✅ **Resource-based structure** with clear domain separation
- ✅ **Consistent patterns** across domains (controller, model, repository, schemas)
- ✅ **Repository pattern** for data access abstraction
- ✅ **DTO pattern** with Pydantic for data validation

### **2. Security Implementation** 
- ✅ **JWT authentication** properly implemented
- ✅ **Role-based access control** (Admin, Attendant, Kitchen)
- ✅ **Password hashing** with secure algorithms
- ✅ **Token validation** in security layer

### **3. Database Layer**
- ✅ **SQLModel ORM** for type safety
- ✅ **Base repository** with common CRUD operations
- ✅ **Connection management** with session handling
- ✅ **Migration support** via Alembic

---

## ❌ **Architecture Issues & TODOs**

### **🔴 CRITICAL: Security Configuration**

> **Note**: For detailed security fixes and code solutions, see [`CODE_QUALITY.md`](./CODE_QUALITY.md)

#### **Critical Security Issues Identified**
- **CORS Misconfiguration**: `allow_origins=['*']` with `allow_credentials=True` creates CSRF vulnerability
- **JWT Secret Validation**: No validation for secret strength or default values  
- **Input Sanitization**: Missing XSS protection for user inputs
- **Global Error Handling**: Implementation details leaked in error responses

### **🔴 CRITICAL: Missing Error Handling**

#### **No Global Exception Handlers**
```python
# FILE: app.py
# ISSUE: No global error handling, errors leak implementation details

# TODO: Add global exception handlers
from fastapi.exceptions import RequestValidationError
from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
```

### **🟡 HIGH: Architecture Violations**

#### **Single Responsibility Principle Violations**

**Order Controller Doing Too Much**
```python
# FILE: resources/order/controller.py (Lines 320-397)
# ISSUE: create_order method handles multiple responsibilities

async def create_order(...):
    # 1. Permission checking
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    
    # 2. Business logic (order creation)
    new_order = Order.create(dto)
    
    # 3. Product validation
    for item in dto.items:
        product = product_repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(...)
    
    # 4. Price calculation
    new_order.total = sum(item.calculate_total() for item in new_order.products)
    
    # 5. Persistence
    order_repository.create(new_order)

# TODO: Extract to Service Layer
# See ARCHITECT_REVIEW.md for complete service layer implementation
```

#### **Code Duplication: Permission Checking**
```python
# DUPLICATED PATTERN across controllers:

# resources/user/controller.py
if current_user.role != UserRole.ADMIN:
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, ...)

# resources/product/controller.py  
if current_user.role != UserRole.ADMIN:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, ...)

# resources/order/controller.py
if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
    raise HTTPException(status_code=403, ...)

# TODO: Permission Decorator Pattern
from functools import wraps
from typing import Set

def require_roles(*allowed_roles: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user or current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Requires one of: {[role.value for role in allowed_roles]}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage:
@require_roles(UserRole.ADMIN, UserRole.ATTENDANT)
async def create_order(dto: CreateOrderDTO, current_user: CurrentUser):
    # Permission checking handled by decorator
    pass
```

### **🟡 HIGH: Missing Business Logic Validation**

#### **Order State Management**
```python
# FILE: resources/order/enums.py
# ISSUE: No validation of order status transitions

# TODO: Add Order Workflow Management
class OrderWorkflow:
    VALID_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.READY, OrderStatus.CANCELLED],
        OrderStatus.READY: [OrderStatus.COMPLETED],
        OrderStatus.COMPLETED: [],
        OrderStatus.CANCELLED: []
    }
    
    @classmethod
    def can_transition(cls, from_status: OrderStatus, to_status: OrderStatus) -> bool:
        return to_status in cls.VALID_TRANSITIONS.get(from_status, [])
    
    @classmethod
    def validate_transition(cls, order: Order, new_status: OrderStatus) -> None:
        if not cls.can_transition(order.status, new_status):
            raise ValueError(f"Cannot transition from {order.status} to {new_status}")

# Usage in update_order:
def update_order(order_id: str, dto: UpdateOrderDTO, ...):
    order = repository.get_by_id(order_id)
    if dto.status:
        OrderWorkflow.validate_transition(order, dto.status)
    # ... continue with update
```

#### **Magic Numbers and Configuration**

> **Note**: For complete constants extraction solution, see [`CODE_QUALITY.md`](./CODE_QUALITY.md)

**Issues Identified**:
- 8+ magic numbers scattered across codebase (utils.py:63, order/model.py:22, etc.)
- No centralized business configuration
- Hard-coded validation limits throughout models

### **🟢 MEDIUM: Inconsistencies**

#### **Router Naming**
```python
# FILE: app.py (Line 11)
# ISSUE: Inconsistent naming
from projeto_aplicado.resources.product.controller import router as item_router

# TODO: Consistent naming
from projeto_aplicado.resources.product.controller import router as product_router
app.include_router(product_router)
```

#### **Missing Application Lifecycle**
```python
# FILE: app.py
# ISSUE: No startup/shutdown handling

# TODO: Add lifespan events
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Application starting up...")
    yield
    # Shutdown  
    logger.info("Application shutting down...")

app = FastAPI(..., lifespan=lifespan)
```

### **🟢 MEDIUM: Environment Management**

#### **No Environment-Specific Configuration**
```python
# FILE: settings.py
# ISSUE: No distinction between environments

# TODO: Environment-specific settings
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class BaseAppSettings(BaseSettings):
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    
    @computed_field
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == Environment.PRODUCTION
    
    @computed_field
    @property
    def debug_mode(self) -> bool:
        return self.ENVIRONMENT == Environment.DEVELOPMENT

# Environment-specific configurations:
class DevelopmentSettings(BaseAppSettings):
    DB_ECHO: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"

class ProductionSettings(BaseAppSettings):
    DB_ECHO: bool = False
    CORS_ORIGINS: str = "https://yourdomain.com"

def get_settings() -> BaseAppSettings:
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        return ProductionSettings()
    return DevelopmentSettings()
```

---

## 🎯 **Recommended Architecture Improvements**

### **Phase 1: Security & Foundation (Critical)**
1. **Fix CORS configuration** with environment-specific origins
2. **Add JWT secret validation** with minimum length requirements  
3. **Implement global exception handling** for consistent error responses
4. **Add application lifecycle management** for proper startup/shutdown

### **Phase 2: Service Layer Introduction (High)**
1. **Create OrderService** to extract business logic from controllers
2. **Implement permission decorators** to eliminate duplication
3. **Add order workflow validation** for state transitions
4. **Extract configuration constants** to eliminate magic numbers

### **Phase 3: Enhanced Patterns (Medium)**
1. **Implement environment-specific settings** for dev/staging/prod
2. **Add structured logging** with correlation IDs
3. **Create business exceptions** for domain-specific errors
4. **Implement caching layer** for frequently accessed data

### **Phase 4: Advanced Features (Low)**
1. **Add API versioning strategy** for future evolution
2. **Implement request/response middleware** for monitoring
3. **Create audit logging** for sensitive operations
4. **Add rate limiting** for API protection

---

## 🏛️ **Target Architecture**

```
┌─────────────────────────────────────────────┐
│                 Controllers                 │  ← HTTP layer (thin)
├─────────────────────────────────────────────┤
│                 Services                    │  ← Business logic
├─────────────────────────────────────────────┤
│               Repositories                  │  ← Data access
├─────────────────────────────────────────────┤
│                  Models                     │  ← Domain entities
├─────────────────────────────────────────────┤
│               Infrastructure                │  ← Database, external APIs
└─────────────────────────────────────────────┘
```

**Key Principles:**
- **Controllers**: Thin layer handling only HTTP concerns
- **Services**: Business logic and domain rules
- **Repositories**: Data access abstraction
- **Models**: Domain entities with behavior
- **Infrastructure**: External concerns

---

*This analysis focuses on the main FastAPI application architecture, excluding the CLI components which already follow Clean Architecture principles.*
