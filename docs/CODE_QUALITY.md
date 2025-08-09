# 🔍 Code Quality Analysis & Fixes

## 📋 **Overview**

This document analyzes code quality issues in the main FastAPI application and provides specific fixes with priority levels.

---

## 🎯 **Quality Metrics Summary**

| Metric | Current Status | Target |
|--------|---------------|--------|
| **Test Coverage** | 94% | 95%+ |
| **Linting Issues** | ~50 warnings | <10 |
| **Code Duplication** | ~15% | <10% |
| **Magic Numbers** | 8 identified | 0 |
| **Security Issues** | 3 critical | 0 |

---

## 🔴 **CRITICAL Issues**

### **1. Security Vulnerabilities**

#### **CORS Misconfiguration (app.py:62)**
```python
# CURRENT ISSUE:
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],        # ❌ DANGEROUS: Allows ALL origins
    allow_credentials=True,     # ❌ DANGEROUS: Combined with * creates CSRF risk
    allow_methods=['*'],
    allow_headers=['*'],
)

# SECURITY IMPACT: 
# - Cross-Site Request Forgery (CSRF) attacks
# - Data theft from authenticated users
# - Cookie hijacking

# FIX:
class BaseAppSettings(BaseSettings):
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    CORS_METHODS: str = "GET,POST,PUT,DELETE,PATCH"
    CORS_HEADERS: str = "Accept,Authorization,Content-Type"

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS.split(','), 
    allow_headers=settings.CORS_HEADERS.split(','),
)
```

#### **Missing Input Sanitization**
```python
# FILE: resources/order/model.py:22
# ISSUE: No input sanitization for notes field

notes: str | None = Field(default=None, nullable=True, max_length=255)

# VULNERABILITY: XSS if notes displayed in frontend without escaping

# FIX: Add input validation
from pydantic import field_validator
import html

class Order(BaseModel, table=True):
    notes: str | None = Field(default=None, nullable=True, max_length=255)
    
    @field_validator('notes')
    @classmethod 
    def sanitize_notes(cls, v):
        if v is not None:
            # Remove potentially dangerous characters
            v = html.escape(v.strip())
            # Remove control characters
            v = ''.join(char for char in v if ord(char) >= 32)
        return v
```

#### **Weak JWT Secret Validation**
```python
# FILE: settings.py:37
# ISSUE: No validation of JWT secret strength

JWT_SECRET_KEY: str  # ❌ Could be weak or default

# SECURITY IMPACT:
# - Token forgery if secret is weak
# - Session hijacking
# - Privilege escalation

# FIX:
from pydantic import field_validator
import secrets

class SensitiveSettings(BaseSettings):
    JWT_SECRET_KEY: str
    
    @field_validator('JWT_SECRET_KEY')
    @classmethod
    def validate_jwt_secret(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError('JWT secret must be at least 32 characters')
        
        # Check for common weak secrets
        weak_secrets = [
            'secret', 'dev-secret-key-change-in-production',
            'your-secret-key-here', '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
        ]
        if v in weak_secrets:
            raise ValueError('Cannot use default or common JWT secret')
        
        # Check entropy (basic)
        if len(set(v)) < 16:  # Should have at least 16 unique characters
            raise ValueError('JWT secret has insufficient entropy')
            
        return v

# HELPER: Generate secure secret
def generate_secure_secret() -> str:
    return secrets.token_urlsafe(64)  # 64 bytes = 512 bits
```

### **2. Error Handling Vulnerabilities**

#### **Information Disclosure**
```python
# CURRENT ISSUE: No global exception handling
# Raw exceptions leak implementation details

# EXAMPLE LEAKED INFO:
# - Database schema details
# - File paths 
# - Internal function names
# - Stack traces

# FIX: Global exception handlers
import logging
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors without leaking details."""
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "type": "validation_error"
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors securely."""
    error_id = str(uuid.uuid4())
    logger.error(f"Unhandled exception {error_id}: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error_id": error_id,  # For support tracking
            "type": "internal_error"
        }
    )
```

---

## 🟡 **HIGH Priority Issues**

### **1. Code Duplication**

#### **Permission Checking Duplication**
```python
# DUPLICATED 15+ times across controllers:

# user/controller.py:144
if current_user.role != UserRole.ADMIN:
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Admin required")

# product/controller.py:33  
if current_user.role != UserRole.ADMIN:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

# order/controller.py:373
if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
    raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="You are not allowed")

# ISSUES:
# - Inconsistent error messages
# - Inconsistent status codes
# - Hard to maintain
# - Easy to miss in new endpoints

# FIX: Permission Decorator System
from functools import wraps
from typing import Set, Callable

class PermissionError(Exception):
    """Custom exception for permission denials."""
    def __init__(self, required_roles: Set[UserRole], user_role: UserRole):
        self.required_roles = required_roles
        self.user_role = user_role
        super().__init__(f"Access denied. Required: {required_roles}, Got: {user_role}")

def require_roles(*roles: UserRole):
    """Decorator that enforces role-based permissions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if current_user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {[r.value for r in roles]}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# USAGE:
@require_roles(UserRole.ADMIN)
async def create_user(...): pass

@require_roles(UserRole.ADMIN, UserRole.ATTENDANT) 
async def create_order(...): pass
```

#### **Repository Pattern Inconsistencies**
```python
# ISSUE: Each repository reimplements similar methods

# user/repository.py
def get_by_username(self, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return self.session.exec(stmt).first()

# user/repository.py  
def get_by_email(self, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return self.session.exec(stmt).first()

# product/repository.py
def get_by_name(self, name: str) -> Optional[Product]:
    stmt = select(Product).where(Product.name == name)
    return self.session.exec(stmt).first()

# FIX: Generic field-based queries in BaseRepository
class BaseRepository(Generic[T]):
    def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """Generic method to get entity by any field."""
        field = getattr(self.model, field_name)
        stmt = select(self.model).where(field == value)
        return self.session.exec(stmt).first()
    
    def get_all_by_field(self, field_name: str, value: Any) -> List[T]:
        """Generic method to get all entities by field value."""
        field = getattr(self.model, field_name)
        stmt = select(self.model).where(field == value)
        return list(self.session.exec(stmt).all())

# USAGE:
user = user_repository.get_by_field('username', 'john')
products = product_repository.get_all_by_field('category', 'burger')
```

### **2. Magic Numbers and Constants**

#### **Hard-coded Values Scattered**
```python
# utils.py:63
numbers = ''.join(random.choices(string.digits, k=3))  # Why 3?

# order/model.py:18
total: float = Field(nullable=False, gt=0.0, default=0.0)  # Why 0.0?

# order/model.py:22
notes: str | None = Field(default=None, nullable=True, max_length=255)  # Why 255?

# order/model.py:24
rating: int | None = Field(default=None, nullable=True, ge=1, le=5)  # Why 1-5?

# FIX: Constants Configuration
class BusinessConstants:
    # Order configuration
    LOCATOR_DIGITS_COUNT = 3
    LOCATOR_RETRY_ATTEMPTS = 5
    MIN_ORDER_TOTAL = 0.01
    MAX_ORDER_ITEMS = 50
    
    # Validation limits
    MAX_NOTES_LENGTH = 255
    MIN_RATING = 1
    MAX_RATING = 5
    MIN_PASSWORD_LENGTH = 8
    MAX_USERNAME_LENGTH = 50
    
    # Business rules
    ORDER_CANCELLATION_WINDOW_MINUTES = 30
    ORDER_PREPARATION_TIMEOUT_MINUTES = 60

# Updated implementations:
def generate_locator():
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(
        string.digits, 
        k=BusinessConstants.LOCATOR_DIGITS_COUNT
    ))
    return f'{letter}{numbers}'

class Order(BaseModel, table=True):
    total: float = Field(
        nullable=False, 
        ge=BusinessConstants.MIN_ORDER_TOTAL, 
        default=BusinessConstants.MIN_ORDER_TOTAL
    )
    notes: str | None = Field(
        default=None, 
        nullable=True, 
        max_length=BusinessConstants.MAX_NOTES_LENGTH
    )
    rating: int | None = Field(
        default=None, 
        nullable=True, 
        ge=BusinessConstants.MIN_RATING, 
        le=BusinessConstants.MAX_RATING
    )
```

### **3. Inconsistent Error Handling**

#### **Mixed Exception Types**
```python
# CURRENT ISSUES:

# order/controller.py:374
raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You are not allowed to create orders')

# order/controller.py:385  
raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail='Product not found')

# Different status codes for similar errors
# Inconsistent detail message formats
# No error categorization

# FIX: Standardized Exception System
class APIException(HTTPException):
    """Base API exception with consistent formatting."""
    def __init__(self, status_code: int, error_code: str, message: str, details: dict = None):
        self.error_code = error_code
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details or {}
            }
        )

class ValidationError(APIException):
    def __init__(self, message: str, field: str = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            message=message,
            details={"field": field} if field else None
        )

class PermissionDeniedError(APIException):
    def __init__(self, required_roles: List[str]):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="PERMISSION_DENIED",
            message="Insufficient permissions",
            details={"required_roles": required_roles}
        )

class ResourceNotFoundError(APIException):
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
            message=f"{resource_type} not found",
            details={"resource_type": resource_type, "resource_id": resource_id}
        )

# USAGE:
if not product:
    raise ResourceNotFoundError("Product", item.product_id)

if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
    raise PermissionDeniedError(["admin", "attendant"])
```

---

## 🟢 **MEDIUM Priority Issues**

### **1. Code Organization**

#### **Inconsistent Import Organization**
```python
# CURRENT: Mixed import styles across files

# Some files:
from fastapi import Depends, HTTPException, status
from sqlmodel import Session

# Other files:  
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

# FIX: Standardized import style
# 1. Standard library imports
import os
import logging
from datetime import datetime
from typing import List, Optional

# 2. Third-party imports  
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session, select

# 3. Local imports
from projeto_aplicado.auth.security import get_current_user
from projeto_aplicado.resources.shared.schemas import BaseResponse
```

#### **Missing Type Hints**
```python
# CURRENT: Some functions missing complete type hints

# utils.py:21
def get_db_url(settings):  # ❌ Missing return type
    return url

# auth/security.py:21
def create_access_token(data: dict):  # ❌ Missing return type
    return encoded_jwt

# FIX: Complete type annotations
from typing import Dict, Any

def get_db_url(settings: Settings) -> str:
    """Return database connection URL."""
    return url

def create_access_token(data: Dict[str, Any]) -> str:
    """Create a JWT access token."""
    return encoded_jwt
```

### **2. Documentation Gaps**

#### **Missing Docstrings**
```python
# CURRENT: Many functions lack proper docstrings

# utils.py:57
def generate_locator():  # ❌ No docstring
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(string.digits, k=3))
    return f'{letter}{numbers}'

# FIX: Comprehensive docstrings
def generate_locator() -> str:
    """Generate a unique order locator.
    
    Creates a locator composed of one uppercase letter followed by
    three random digits (e.g., 'A123', 'Z456').
    
    Returns:
        str: A unique locator string in format [A-Z][0-9]{3}
        
    Examples:
        >>> generate_locator()
        'B742'
    """
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(
        string.digits, 
        k=BusinessConstants.LOCATOR_DIGITS_COUNT
    ))
    return f'{letter}{numbers}'
```

### **3. Performance Issues**

#### **N+1 Query Problems**
```python
# CURRENT: Potential N+1 queries in order/controller.py

# Gets order
order = order_repository.get_by_id(order_id)

# Then gets each item individually (N+1 problem)
for item in order.products:
    product = product_repository.get_by_id(item.product_id)

# FIX: Eager loading in repository
class OrderRepository(BaseRepository[Order]):
    def get_with_items_and_products(self, order_id: str) -> Optional[Order]:
        """Get order with eagerly loaded items and products."""
        stmt = (
            select(Order)
            .options(
                selectinload(Order.products).selectinload(OrderItem.product)
            )
            .where(Order.id == order_id)
        )
        return self.session.exec(stmt).first()
```

---

## 🔵 **LOW Priority Issues**

### **1. Code Style Inconsistencies**

#### **Variable Naming**
```python
# CURRENT: Mixed naming conventions

# app.py:11
from projeto_aplicado.resources.product.controller import router as item_router

# Should be:
from projeto_aplicado.resources.product.controller import router as product_router
```

#### **String Formatting**
```python
# CURRENT: Mixed string formatting styles

# utils.py:27
url = f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}'

# Better (more readable):
url = (
    f'postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
    f'@{settings.POSTGRES_HOSTNAME}:{settings.POSTGRES_PORT}'
    f'/{settings.POSTGRES_DB}'
)
```

---

## 🛠️ **Implementation Priority**

> **Note**: For detailed implementation roadmap with timelines, see [`ROADMAP.md`](./ROADMAP.md)

### **Fix Priority Order**
1. **🔴 Critical Security** → CORS, JWT validation, error handling, input sanitization  
2. **🟡 Code Duplication** → Permission decorators, repository patterns, exception classes
3. **🟢 Constants & Config** → Business constants, environment settings, error messages
4. **🔵 Code Polish** → Type hints, docstrings, performance, style

---

## 📊 **Quality Metrics Tracking**

| Metric | Before | Target | Validation |
|--------|--------|---------|------------|
| **Security Issues** | 3 critical | 0 | Security scan |
| **Code Duplication** | ~15% | <5% | SonarQube analysis |
| **Type Coverage** | ~70% | >95% | mypy --strict |
| **Docstring Coverage** | ~60% | >90% | interrogate |
| **Linting Issues** | ~50 | <5 | ruff check |

---

*This analysis provides specific, actionable fixes for code quality issues in the main FastAPI application.*
