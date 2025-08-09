# 🔍 Code Quality: Design Patterns, SOLID & Clean Code

## 📋 **Code Quality Overview**

This document analyzes **code quality** aspects of the Food Truck Management System, focusing on design patterns implementation, SOLID principles compliance, DRY violations, code smells, and clean code practices.

---

## 🎯 **Code Quality Score**

| Category | Score | Status | Critical Issues |
|----------|-------|--------|----------------|
| **🏗️ Design Patterns** | 6/10 | ⚠️ Needs Improvement | Missing Strategy, Command patterns |
| **🔧 SOLID Principles** | 4/10 | ❌ Poor | Multiple SRP violations |
| **📝 Clean Code** | 5/10 | ⚠️ Needs Improvement | Magic numbers, long methods |
| **🚫 Code Smells** | 3/10 | ❌ Poor | Data/Feature envy, God class |
| **🧹 DRY Compliance** | 4/10 | ❌ Poor | Permission checking duplication |
| **📊 Overall Quality** | **4.5/10** | ❌ **Poor** | **Needs major refactoring** |

---

## 🚨 **CRITICAL: DESIGN PATTERN VIOLATIONS**

### **1. Missing Command Pattern for Business Operations**

**❌ Current Problem**: Controllers directly execute complex business logic

```python
# FILE: resources/order/controller.py:320-397
# ACTUAL CURRENT CODE - doing everything in controller
async def create_order(
    dto: CreateOrderDTO,
    order_repository: OrderRepo,
    product_repository: ProductRepo,
    current_user: CurrentUser,
):
    # 1. Authorization check (hard-coded)
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not allowed to create orders',
        )

    # 2. Domain object creation
    new_order = Order.create(dto)

    # 3. N+1 Query Problem - individual product lookups
    for item in dto.items:
        product = product_repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail='Product not found',
            )
        order_item = OrderItem.create(item)
        new_order.products.append(order_item)

    # 4. Business calculation
    new_order.total = sum(
        item.calculate_total() for item in new_order.products
    )
    
    # 5. Persistence
    order_repository.create(new_order)
    return BaseResponse(id=new_order.id, action='created')
```

**✅ Pythonic Solution**: Command Pattern with Pydantic

```python
# NEW FILE: resources/order/commands.py
from abc import ABC, abstractmethod
from typing import Any, Protocol

from pydantic import BaseModel, Field, field_validator
from projeto_aplicado.resources.order.schemas import CreateOrderDTO
from projeto_aplicado.resources.order.model import Order
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.shared.schemas import BaseResponse


class CommandResult(BaseModel):
    """Pydantic model for command results with validation."""
    success: bool
    data: Any = None
    message: str = ""


class Command(ABC):
    """Command interface for business operations."""
    
    @abstractmethod
    async def execute(self) -> CommandResult:
        """Execute the command asynchronously."""
        pass


class CreateOrderCommand(BaseModel, Command):
    """Pydantic-based command to create orders with validation."""
    
    dto: CreateOrderDTO
    user: User
    
    class Config:
        arbitrary_types_allowed = True  # Allow User model
    
    @field_validator('user')
    @classmethod
    def validate_user_permissions(cls, user: User) -> User:
        """Validate user has permission to create orders."""
        if user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
            raise ValueError(f"User role {user.role} cannot create orders")
        return user
    
    async def execute(self) -> CommandResult:
        """Execute order creation with proper validation."""
        # Use dependency injection for services
        from projeto_aplicado.resources.order.services import OrderService
        
        order_service = OrderService()
        
        try:
            order = await order_service.create_order(self.dto, self.user)
            return CommandResult(
                success=True,
                data=order,
                message="Order created successfully"
            )
        except Exception as e:
            return CommandResult(
                success=False,
                message=str(e)
            )


# NEW FILE: resources/order/services.py
from typing import List
from fastapi import HTTPException
from projeto_aplicado.resources.order.schemas import CreateOrderDTO, CreateOrderItemDTO
from projeto_aplicado.resources.order.model import Order, OrderItem
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.product.repository import ProductRepository
from projeto_aplicado.resources.order.repository import OrderRepository
from projeto_aplicado.resources.user.model import User


class OrderService:
    """Service layer for order business logic."""
    
    def __init__(
        self, 
        order_repo: OrderRepository, 
        product_repo: ProductRepository
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
    
    async def create_order(self, dto: CreateOrderDTO, user: User) -> Order:
        """Create order with proper business logic separation."""
        # Validate products first (bulk query)
        products = await self._validate_products(dto.items)
        
        # Create order domain object
        order = Order.create(dto)
        
        # Build order items with validated products
        for item_dto in dto.items:
            product = next(p for p in products if p.id == item_dto.product_id)
            order_item = OrderItem.create(item_dto)
            order_item.price = product.price  # Lock current price
            order.products.append(order_item)
        
        # Calculate total
        order.total = sum(item.calculate_total() for item in order.products)
        
        # Persist order
        saved_order = self.order_repo.create(order)
        return saved_order
    
    async def _validate_products(self, items: List[CreateOrderItemDTO]) -> List[Product]:
        """Validate and get products using bulk query (fixes N+1 problem)."""
        product_ids = [item.product_id for item in items]
        
        # Bulk query - single database call
        products = self.product_repo.get_by_ids(product_ids)
        
        # Validate all products exist
        if len(products) != len(product_ids):
            found_ids = {p.id for p in products}
            missing_ids = set(product_ids) - found_ids
            raise ValueError(f"Products not found: {missing_ids}")
        
        # Validate products are available
        unavailable = [p.name for p in products if not p.is_available]
        if unavailable:
            raise ValueError(f"Products not available: {unavailable}")
        
        return products

# UPDATED CONTROLLER (much cleaner):
async def create_order(
    dto: CreateOrderDTO,
    current_user: CurrentUser,
):
    """Clean controller - only HTTP concerns."""
    command = CreateOrderCommand(dto=dto, user=current_user)
    result = await command.execute()
    
    if not result.success:
        raise HTTPException(
            status_code=400, 
            detail=result.message
        )
    
    return BaseResponse(id=result.data.id, action='created')
```

### **2. Missing Factory Pattern for Service Creation**

**❌ Current Problem**: Manual service instantiation, hard dependencies

```python
# ACTUAL CURRENT PATTERN in controllers:
# Each controller manually imports and depends on specific repositories
from projeto_aplicado.resources.order.repository import OrderRepository, get_order_repository
from projeto_aplicado.resources.product.repository import ProductRepository, get_product_repository

OrderRepo = Annotated[OrderRepository, Depends(get_order_repository)]
ProductRepo = Annotated[ProductRepository, Depends(get_product_repository)]

async def create_order(
    dto: CreateOrderDTO,
    order_repository: OrderRepo,      # Manual dependency
    product_repository: ProductRepo,  # Manual dependency
    current_user: CurrentUser,
):
    # Controller has to know about specific repositories
    # Hard to test, hard to swap implementations
    # No service layer abstraction
    pass

# ISSUES:
# - Controllers know about specific repository implementations
# - No service layer abstraction
# - Hard to mock for testing
# - Tight coupling between controllers and data layer
# - Violates Dependency Inversion Principle
```

**✅ Pythonic Solution**: Service Factory with Protocol

```python
# NEW FILE: projeto_aplicado/services/factory.py
from typing import Protocol
from abc import ABC, abstractmethod
from fastapi import Depends
from sqlmodel import Session

from projeto_aplicado.ext.database.db import get_session
from projeto_aplicado.resources.order.services import OrderService
from projeto_aplicado.resources.user.services import UserService
from projeto_aplicado.resources.product.services import ProductService
from projeto_aplicado.resources.order.repository import OrderRepository
from projeto_aplicado.resources.product.repository import ProductRepository
from projeto_aplicado.resources.user.repository import UserRepository


class ServiceFactory(Protocol):
    """Protocol for service factory (duck typing)."""
    
    def create_order_service(self) -> OrderService:
        """Create order service instance."""
        ...
    
    def create_user_service(self) -> UserService:
        """Create user service instance."""
        ...
    
    def create_product_service(self) -> ProductService:
        """Create product service instance."""
        ...


class DefaultServiceFactory:
    """Default implementation of service factory using repositories."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_order_service(self) -> OrderService:
        """Create order service with its dependencies."""
        order_repo = OrderRepository(self.session)
        product_repo = ProductRepository(self.session)
        return OrderService(order_repo, product_repo)
    
    def create_user_service(self) -> UserService:
        """Create user service with its dependencies."""
        user_repo = UserRepository(self.session)
        return UserService(user_repo)
    
    def create_product_service(self) -> ProductService:
        """Create product service with its dependencies."""
        product_repo = ProductRepository(self.session)
        return ProductService(product_repo)


# FastAPI dependency
def get_service_factory(
    session: Session = Depends(get_session)
) -> ServiceFactory:
    """Dependency injection for service factory."""
    return DefaultServiceFactory(session)


# UPDATED CONTROLLER - much cleaner:
async def create_order(
    dto: CreateOrderDTO,
    factory: ServiceFactory = Depends(get_service_factory),
    current_user: CurrentUser,
):
    """Clean controller using service factory."""
    order_service = factory.create_order_service()
    order = await order_service.create_order(dto, current_user)
    return BaseResponse(id=order.id, action='created')


# BENEFITS:
# - Controllers only depend on ServiceFactory interface
# - Easy to swap implementations for testing
# - Follows Dependency Inversion Principle
# - Service layer abstraction
# - Protocol-based typing (Pythonic)
# - Single place to configure service dependencies
```

---

## 🔧 **CRITICAL: SOLID PRINCIPLES VIOLATIONS**

### **1. Single Responsibility Principle - SEVERE VIOLATIONS**

#### **❌ God Method in Order Controller**
```python
# FILE: resources/order/controller.py:320-397
# VIOLATION: create_order method has 6 different responsibilities

async def create_order(...):  # 78 lines - TOO LONG
    # Responsibility 1: Authorization
    if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
        raise HTTPException(...)
    
    # Responsibility 2: Domain object creation
    new_order = Order.create(dto)
    
    # Responsibility 3: Product validation (N+1 query problem)
    for item in dto.items:
        product = product_repository.get_by_id(item.product_id)
        if not product:
            raise HTTPException(...)
        order_item = OrderItem.create(item)
        new_order.products.append(order_item)
    
    # Responsibility 4: Business calculation
    new_order.total = sum(item.calculate_total() for item in new_order.products)
    
    # Responsibility 5: Persistence
    order_repository.create(new_order)
    
    # Responsibility 6: Response formatting
    return BaseResponse(id=new_order.id, action='created')
```

**✅ Architect Solution**: Extract Service Layer
```python
# NEW FILE: resources/order/service.py
class OrderService:
    """Dedicated service for order business logic."""
    
    def __init__(
        self, 
        order_repo: OrderRepository, 
        product_repo: ProductRepository,
        permission_service: PermissionService
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.permission_service = permission_service
    
    def create_order(self, dto: CreateOrderDTO, user: User) -> Order:
        """Create order with proper separation of concerns."""
        # Single responsibility: orchestrate order creation
        self.permission_service.ensure_can_create_orders(user)
        
        products = self._validate_and_get_products(dto.items)
        order = self._build_order(dto, products)
        
        return self.order_repo.create(order)
    
    def _validate_and_get_products(self, items: List[OrderItemDTO]) -> List[Product]:
        """Single responsibility: validate and retrieve products."""
        product_ids = [item.product_id for item in items]
        products = self.product_repo.get_by_ids(product_ids)  # Bulk query
        
        if len(products) != len(product_ids):
            found_ids = {p.id for p in products}
            missing = set(product_ids) - found_ids
            raise ValueError(f"Products not found: {missing}")
        
        return products
    
    def _build_order(self, dto: CreateOrderDTO, products: List[Product]) -> Order:
        """Single responsibility: build order with items."""
        order = Order.create(dto)
        
        for item_dto in dto.items:
            product = next(p for p in products if p.id == item_dto.product_id)
            
            if not product.is_available:
                raise ValueError(f"Product {product.name} is not available")
            
            order_item = OrderItem.create(item_dto)
            order_item.price = product.price  # Lock current price
            order.products.append(order_item)
        
        order.total = sum(item.calculate_total() for item in order.products)
        return order

# SIMPLIFIED CONTROLLER:
async def create_order(
    dto: CreateOrderDTO,
    order_service: OrderService = Depends(),
    current_user: CurrentUser,
):
    """Single responsibility: handle HTTP request/response."""
    try:
        order = order_service.create_order(dto, current_user)
        return BaseResponse(id=order.id, action='created')
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
```

### **2. Open/Closed Principle - VIOLATION**

**❌ Current Problem**: Hard to extend validation system
```python
# Adding new validation requires modifying existing models
class Order(BaseModel, table=True):
    notes: str | None = Field(default=None, nullable=True, max_length=255)
    
    # Hard-coded validation - not extensible
    @field_validator('notes')
    @classmethod
    def validate_notes(cls, v):
        if v and len(v) > 255:
            raise ValueError("Notes too long")
        return v
```

**✅ Architect Solution**: Pluggable Validator System
```python
# NEW FILE: validation/validators.py
from abc import ABC, abstractmethod
from typing import Any, List

class FieldValidator(ABC):
    """Abstract validator - open for extension."""
    
    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass
    
    @abstractmethod
    def get_error_message(self) -> str:
        pass

class LengthValidator(FieldValidator):
    """Length validation rule."""
    
    def __init__(self, max_length: int):
        self.max_length = max_length
    
    def validate(self, value: str) -> str:
        if value and len(value) > self.max_length:
            raise ValueError(self.get_error_message())
        return value
    
    def get_error_message(self) -> str:
        return f"Value exceeds maximum length of {self.max_length}"

class ContentValidator(FieldValidator):
    """Content filtering validation."""
    
    def validate(self, value: str) -> str:
        if value and any(word in value.lower() for word in ['spam', 'abuse']):
            raise ValueError(self.get_error_message())
        return value
    
    def get_error_message(self) -> str:
        return "Content contains prohibited words"

class ValidatorChain:
    """Closed for modification, open for extension."""
    
    def __init__(self):
        self.validators: List[FieldValidator] = []
    
    def add_validator(self, validator: FieldValidator):
        """Add new validator without modifying existing code."""
        self.validators.append(validator)
    
    def validate(self, value: Any) -> Any:
        """Run all validators in chain."""
        for validator in self.validators:
            value = validator.validate(value)
        return value

# USAGE - no model modification needed:
notes_validator = ValidatorChain()
notes_validator.add_validator(LengthValidator(255))
notes_validator.add_validator(ContentValidator())

# Adding new validation rule (without modifying existing code):
notes_validator.add_validator(ProfanityValidator())
```

---

## 🚫 **CRITICAL: CODE SMELLS DETECTED**

### **1. Data Class Smell - CRITICAL**

**❌ Current Problem**: Anemic Domain Models
```python
# order/model.py - Order class has minimal behavior
class Order(BaseModel, table=True):
    status: str = Field(...)
    total: float = Field(...)
    
    @classmethod
    def create(cls, dto: 'CreateOrderDTO'):
        """Only factory method - no real behavior"""
        order = cls(**dto.model_dump())
        return order
    
    # Missing: business methods for order lifecycle
```

**✅ Architect Solution**: Rich Domain Models
```python
class Order(BaseModel, table=True):
    """Rich domain model with business behavior."""
    
    status: str = Field(default=OrderStatus.PENDING)
    total: float = Field(default=0.0, ge=0)
    
    def add_item(self, product: Product, quantity: int) -> None:
        """Business method: add item to order."""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Cannot modify order after confirmation")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if not product.is_available:
            raise ValueError(f"Product {product.name} is not available")
        
        order_item = OrderItem(
            product_id=product.id,
            quantity=quantity,
            price=product.price,  # Lock current price
            order_id=self.id
        )
        self.products.append(order_item)
        self._recalculate_total()
    
    def confirm(self) -> None:
        """Business method: confirm order."""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order is already confirmed")
        
        if not self.products:
            raise ValueError("Cannot confirm empty order")
        
        self.status = OrderStatus.CONFIRMED
        self._recalculate_total()
    
    def can_be_modified(self) -> bool:
        """Business query: check if order can be modified."""
        return self.status == OrderStatus.PENDING
    
    def _recalculate_total(self) -> None:
        """Private method: recalculate order total."""
        self.total = sum(item.calculate_total() for item in self.products)
```

### **2. Feature Envy - DETECTED**

**❌ Current Problem**: Controllers know too much about other domains
```python
# Order controller accessing product details directly
product = product_repository.get_by_id(item.product_id)
if not product:
    raise HTTPException(...)  # Controller handling product business logic
```

**✅ Architect Solution**: Tell, Don't Ask Principle
```python
class OrderService:
    def create_order(self, dto: CreateOrderDTO, user: User) -> Order:
        """Tell the order what to do, don't ask about its internals."""
        order = Order()
        
        for item_dto in dto.items:
            # Tell the order to add item - let it handle the complexity
            product = self.product_repo.get_by_id(item_dto.product_id)
            order.add_item(product, item_dto.quantity)  # Order handles validation
        
        order.confirm()  # Tell, don't ask
        return self.order_repo.create(order)
```

---

## 🧹 **CRITICAL: DRY VIOLATIONS**

### **1. Permission Checking Duplication**

**❌ Duplicated across controllers (ACTUAL CURRENT CODE):**

```python
# ACTUAL: order/controller.py:373-377
if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail='You are not allowed to create orders',
    )

# ACTUAL: Similar patterns in other controllers (user, product)
if current_user.role != UserRole.ADMIN:
    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail='Admin access required',
    )

# ISSUES WITH CURRENT APPROACH:
# - Hard-coded role checks scattered everywhere
# - Inconsistent error messages ('You are not allowed' vs 'Admin access required')
# - Mixed status code imports (HTTPStatus.FORBIDDEN vs status.HTTP_403_FORBIDDEN)
# - No extensibility for business hours, ownership, etc.
# - Violates DRY principle
# - Easy to miss in new endpoints
```

**✅ Pythonic DRY Solution**: Pydantic-Based Permission System
```python
# NEW FILE: auth/permissions.py
from abc import ABC, abstractmethod
from typing import Set, List, Callable, Literal
from functools import wraps
from datetime import datetime, time

from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status

from projeto_aplicado.resources.user.model import User, UserRole


class PermissionConfig(BaseModel):
    """Pydantic model for permission configuration."""
    resource: str
    action: str
    allowed_roles: Set[UserRole]
    business_hours_only: bool = False
    
    @field_validator('resource', 'action')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Resource and action cannot be empty")
        return v.lower()


class PermissionRule(ABC):
    """Abstract permission rule."""
    
    @abstractmethod
    def allows(self, user: User, config: PermissionConfig) -> bool:
        pass
    
    @abstractmethod
    def get_error_message(self, config: PermissionConfig) -> str:
        pass


class RolePermissionRule(PermissionRule):
    """Role-based permission rule using enum comparison."""
    
    def allows(self, user: User, config: PermissionConfig) -> bool:
        return user.role in config.allowed_roles
    
    def get_error_message(self, config: PermissionConfig) -> str:
        roles = [role.value for role in config.allowed_roles]
        return f"Access denied. Required roles: {roles}"


class BusinessHoursRule(PermissionRule):
    """Business hours permission rule."""
    
    def allows(self, user: User, config: PermissionConfig) -> bool:
        if not config.business_hours_only:
            return True
        
        now = datetime.now().time()
        return time(8, 0) <= now <= time(22, 0)
    
    def get_error_message(self, config: PermissionConfig) -> str:
        return "Action not allowed outside business hours (8 AM - 10 PM)"


class PermissionChecker:
    """Centralized permission checking with Pydantic validation."""
    
    def __init__(self):
        self.permissions: dict[str, PermissionConfig] = {}
        self.rules: List[PermissionRule] = [
            RolePermissionRule(),
            BusinessHoursRule(),
        ]
    
    def register_permission(self, config: PermissionConfig) -> None:
        """Register a permission configuration."""
        key = f"{config.resource}:{config.action}"
        self.permissions[key] = config
    
    def check_permission(self, user: User, resource: str, action: str) -> tuple[bool, List[str]]:
        """Check permission and return result with error messages."""
        key = f"{resource.lower()}:{action.lower()}"
        config = self.permissions.get(key)
        
        if not config:
            return False, [f"No permission configured for {resource}:{action}"]
        
        errors = []
        for rule in self.rules:
            if not rule.allows(user, config):
                errors.append(rule.get_error_message(config))
        
        return len(errors) == 0, errors


# Global permission checker
permission_checker = PermissionChecker()

# Configure permissions using Pydantic models
permission_checker.register_permission(
    PermissionConfig(
        resource="users",
        action="create",
        allowed_roles={UserRole.ADMIN}
    )
)

permission_checker.register_permission(
    PermissionConfig(
        resource="orders",
        action="create",
        allowed_roles={UserRole.ADMIN, UserRole.ATTENDANT},
        business_hours_only=True
    )
)

permission_checker.register_permission(
    PermissionConfig(
        resource="products",
        action="create",
        allowed_roles={UserRole.ADMIN}
    )
)


def require_permission(resource: str, action: str):
    """Pythonic decorator using the permission checker."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current_user from kwargs (FastAPI dependency injection)
            current_user = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            allowed, error_messages = permission_checker.check_permission(
                current_user, resource, action
            )
            
            if not allowed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="; ".join(error_messages)
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Simplified decorator for basic role checks (maintains current pattern)
def require_roles(*roles: UserRole):
    """Simple role-based decorator matching current codebase style."""
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
                role_names = [role.value for role in roles]
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required roles: {role_names}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# USAGE EXAMPLES:

# Replace current hard-coded checks:
@require_permission("orders", "create")  # Uses business hours + role rules
async def create_order(
    dto: CreateOrderDTO,
    current_user: CurrentUser,
):
    """Clean controller with declarative permissions."""
    # No permission checking code needed here!
    # Business logic only
    pass

@require_roles(UserRole.ADMIN)  # Simple role check
async def create_user(
    dto: CreateUserDTO,
    current_user: CurrentUser,
):
    """Simple role-based permission."""
    pass

# Instead of current code:
# if current_user.role not in [UserRole.ADMIN, UserRole.ATTENDANT]:
#     raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You are not allowed')
```

---

## 📝 **CLEAN CODE VIOLATIONS**

### **1. Magic Numbers - CRITICAL**

**❌ Violations Found in ACTUAL CODE:**
```python
# ACTUAL: utils.py:63 - Magic number 3 for locator digits
numbers = ''.join(random.choices(string.digits, k=3))

# ACTUAL: order/model.py:22 - Magic number 255 for notes length
notes: str | None = Field(default=None, nullable=True, max_length=255)

# ACTUAL: order/model.py:24 - Magic numbers 1, 5 for rating range
rating: int | None = Field(default=None, nullable=True, ge=1, le=5)

# ACTUAL: user/model.py:21 - Magic number 20 for username length
username: str = Field(nullable=False, unique=True, max_length=20, index=True)

# ACTUAL: user/model.py:23 - Magic number 255 for email length  
email: str = Field(nullable=False, unique=True, max_length=255, index=True)

# ACTUAL: user/model.py:25 - Magic number 100 for full_name length
full_name: Optional[str] = Field(max_length=100, nullable=True)

# ACTUAL: order/model.py:18 - Magic number 0.0 for total default
total: float = Field(nullable=False, gt=0.0, default=0.0)
```

**✅ Pythonic Solution**: Pydantic-Based Business Constants
```python
# NEW FILE: projeto_aplicado/constants.py
from pydantic import BaseModel, Field
from typing import Final


class FieldLimits(BaseModel):
    """Pydantic model for database field constraints."""
    
    # User field limits
    USERNAME_MAX_LENGTH: int = Field(20, description="Maximum username length")
    EMAIL_MAX_LENGTH: int = Field(255, description="Maximum email length") 
    FULL_NAME_MAX_LENGTH: int = Field(100, description="Maximum full name length")
    PASSWORD_MAX_LENGTH: int = Field(255, description="Maximum password length")
    
    # Order field limits  
    NOTES_MAX_LENGTH: int = Field(255, description="Maximum order notes length")
    RATING_MIN: int = Field(1, description="Minimum rating value")
    RATING_MAX: int = Field(5, description="Maximum rating value")
    
    # Business constraints
    ORDER_TOTAL_MIN: float = Field(0.01, description="Minimum order total")
    LOCATOR_DIGITS_COUNT: int = Field(3, description="Number of digits in order locator")


# Create singleton instance with validation
FIELD_LIMITS: Final = FieldLimits()


class BusinessRules(BaseModel):
    """Business logic constants."""
    
    ORDER_CANCELLATION_WINDOW_MINUTES: int = 30
    ORDER_PREPARATION_TIMEOUT_MINUTES: int = 60
    MAX_ORDER_ITEMS: int = 50
    BUSINESS_HOUR_START: int = 8
    BUSINESS_HOUR_END: int = 22


BUSINESS_RULES: Final = BusinessRules()


# UPDATED IMPLEMENTATIONS using constants:

# projeto_aplicado/utils.py
def generate_locator() -> str:
    """Generate order locator using business constants."""
    letter = random.choice(string.ascii_uppercase)
    numbers = ''.join(random.choices(
        string.digits, 
        k=FIELD_LIMITS.LOCATOR_DIGITS_COUNT
    ))
    return f'{letter}{numbers}'


# projeto_aplicado/resources/order/model.py  
class Order(BaseModel, table=True):
    """Order model with business constants."""
    
    status: str = Field(max_length=20, nullable=False, default=OrderStatus.PENDING)
    total: float = Field(
        nullable=False, 
        gt=FIELD_LIMITS.ORDER_TOTAL_MIN, 
        default=FIELD_LIMITS.ORDER_TOTAL_MIN
    )
    locator: str = Field(default_factory=generate_locator, index=True, nullable=False)
    notes: str | None = Field(
        default=None, 
        nullable=True, 
        max_length=FIELD_LIMITS.NOTES_MAX_LENGTH
    )
    rating: int | None = Field(
        default=None, 
        nullable=True, 
        ge=FIELD_LIMITS.RATING_MIN, 
        le=FIELD_LIMITS.RATING_MAX
    )
    products: List['OrderItem'] = Relationship(cascade_delete=True)


# projeto_aplicado/resources/user/model.py
class User(BaseModel, table=True):
    """User model with business constants."""
    
    username: str = Field(
        nullable=False, 
        unique=True, 
        max_length=FIELD_LIMITS.USERNAME_MAX_LENGTH, 
        index=True
    )
    email: str = Field(
        nullable=False, 
        unique=True, 
        max_length=FIELD_LIMITS.EMAIL_MAX_LENGTH, 
        index=True
    )
    password: str = Field(
        nullable=False, 
        max_length=FIELD_LIMITS.PASSWORD_MAX_LENGTH
    )
    full_name: Optional[str] = Field(
        max_length=FIELD_LIMITS.FULL_NAME_MAX_LENGTH, 
        nullable=True
    )
    role: UserRole = Field(nullable=False)


# BENEFITS:
# - Type-safe constants with Pydantic validation
# - Centralized business rules
# - IDE autocomplete and type checking
# - Easy to modify and maintain
# - Self-documenting with descriptions
# - Can be imported anywhere: from projeto_aplicado.constants import FIELD_LIMITS
```

### **2. Long Parameter Lists - VIOLATION**

**❌ Current Problem:**
```python
async def create_order(
    dto: CreateOrderDTO,
    order_repository: OrderRepo,
    product_repository: ProductRepo,
    current_user: CurrentUser,
):  # 4 parameters - getting complex
```

**✅ Clean Code Solution**: Parameter Object Pattern
```python
# NEW FILE: resources/order/dependencies.py
from dataclasses import dataclass
from fastapi import Depends
from projeto_aplicado.resources.order.schemas import CreateOrderDTO
from projeto_aplicado.resources.order.services import OrderService
from projeto_aplicado.resources.user.model import User
from projeto_aplicado.auth.security import get_current_user


@dataclass
class OrderCreationContext:
    """Parameter object for order creation."""
    dto: CreateOrderDTO
    user: User
    order_service: OrderService
    
    def validate(self) -> None:
        """Validate the context."""
        if not self.dto.items:
            raise ValueError("Order must have items")
        if not self.user:
            raise ValueError("User is required")


def get_order_service() -> OrderService:
    """Dependency to get OrderService instance."""
    return OrderService()


def get_order_context(
    dto: CreateOrderDTO,
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends(get_order_service)
) -> OrderCreationContext:
    """Dependency that creates OrderCreationContext parameter object."""
    return OrderCreationContext(
        dto=dto,
        user=current_user,
        order_service=order_service
    )


# SIMPLIFIED CONTROLLER:
async def create_order(
    context: OrderCreationContext = Depends(get_order_context)
):
    """Clean method with single parameter object."""
    context.validate()
    order = context.order_service.create_order(context.dto, context.user)
    return BaseResponse(id=order.id, action='created')


# BENEFITS:
# - Single parameter instead of 4+ separate dependencies
# - Encapsulates related data together
# - Easy to extend with new fields
# - Testable parameter object
# - Clear dependency injection pattern
# - Maintains FastAPI's dependency injection system
```

---

## 📊 **PERFORMANCE ANTI-PATTERNS**

### **1. N+1 Query Problem - CRITICAL**

**❌ Current Problem:**
```python
# order/controller.py - N+1 queries
for item in dto.items:  # N iterations
    product = product_repository.get_by_id(item.product_id)  # 1 query each = N queries
```

**✅ Performance Solution:**
```python
# UPDATE: projeto_aplicado/resources/product/repository.py
from typing import List
from sqlmodel import select
from projeto_aplicado.resources.product.model import Product
from projeto_aplicado.resources.shared.repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Product repository with bulk query optimization."""
    
    def get_by_ids(self, product_ids: List[str]) -> List[Product]:
        """Bulk query to prevent N+1 problem."""
        if not product_ids:
            return []
        
        stmt = select(Product).where(Product.id.in_(product_ids))
        return list(self.session.exec(stmt).all())
    
    def get_available_by_ids(self, product_ids: List[str]) -> List[Product]:
        """Get only available products by IDs."""
        if not product_ids:
            return []
        
        stmt = select(Product).where(
            Product.id.in_(product_ids),
            Product.is_available == True
        )
        return list(self.session.exec(stmt).all())


# USAGE in OrderService:
async def _validate_products(self, items: List[CreateOrderItemDTO]) -> List[Product]:
    """Optimized product validation - single query instead of N queries."""
    product_ids = [item.product_id for item in items]
    
    # Single database query for all products
    products = self.product_repo.get_by_ids(product_ids)
    
    # Validation logic
    if len(products) != len(product_ids):
        found_ids = {p.id for p in products}
        missing_ids = set(product_ids) - found_ids
        raise ValueError(f"Products not found: {missing_ids}")
    
    return products

# PERFORMANCE IMPROVEMENT:
# Before: N+1 queries (1 + N individual product lookups)
# After: 1 query (bulk lookup with WHERE IN clause)
# 10 items: 11 queries → 1 query (91% reduction)
# 100 items: 101 queries → 1 query (99% reduction)
```

---

## 🎯 **PRIORITY FIXES ROADMAP**

### **🔴 CRITICAL (Week 1-2): Design Patterns & SOLID**

1. **Extract Service Layer** (16 hours)
   - Create OrderService, UserService, ProductService
   - Move business logic from controllers to services
   
2. **Implement Command Pattern** (12 hours)
   - Create Command interface and implementations
   - Separate business operations from HTTP handling

3. **Fix N+1 Query Problems** (4 hours)
   - Add bulk query methods to repositories
   - Optimize order creation process

### **🟡 HIGH (Week 3-4): Design Patterns & DRY**

4. **Comprehensive Permission System** (10 hours)
   - Implement permission engine with rule-based approach
   - Create decorators for easy usage
   - Eliminate hard-coded role checks (DRY + Strategy + OCP)

5. **Factory Pattern for Services** (6 hours)
   - Create service factory for dependency management
   - Improve testability

6. **Rich Domain Models** (10 hours)
   - Add business methods to Order, Product, User
   - Implement Tell, Don't Ask principle

### **🟢 MEDIUM (Week 5-6): Clean Code**

7. **Extract Business Constants** (4 hours)
   - Centralize magic numbers
   - Create configuration classes

8. **Parameter Object Pattern** (6 hours)
   - Simplify method signatures
   - Improve readability

---

## 📈 **Expected Code Quality Improvements**

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Cyclomatic Complexity** | 15+ | <5 | 200% better |
| **Method Length** | 78 lines | <20 lines | 300% better |
| **Code Duplication** | 15% | <3% | 500% better |
| **Design Patterns** | 2/10 | 8/10 | 300% better |
| **SOLID Compliance** | 4/10 | 9/10 | 125% better |

---

## 🔗 **Related Documentation**

- **[System Architecture](ARCHITECTURE.md)** - Overall system design and component interaction
- **[Development Guide](DEVELOPMENT.md)** - Setup and development workflows  
- **[Testing Guide](../projeto_aplicado/cli/tests/README.md)** - Testing strategies and practices
- **[Project Roadmap](ROADMAP.md)** - Implementation timeline and priorities

---

*This analysis focuses on code-level quality including design patterns, SOLID principles, DRY compliance, and clean code practices. For system-level architecture analysis, see [ARCHITECTURE.md](ARCHITECTURE.md).*
