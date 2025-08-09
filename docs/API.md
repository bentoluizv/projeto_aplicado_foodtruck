# 🚀 Food Truck API Documentation

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-blue.svg)](https://spec.openapis.org/oas/v3.1.0)
[![JWT](https://img.shields.io/badge/auth-JWT-orange.svg)](https://jwt.io/)

> **Complete REST API documentation for the Food Truck Management System**

## 📋 Table of Contents

- [🎯 API Overview](#-api-overview)
- [🔐 Authentication](#-authentication)
- [📊 API Reference](#-api-reference)
- [🔄 Request/Response Examples](#-requestresponse-examples)
- [📝 Data Models](#-data-models)
- [🎭 User Roles & Permissions](#-user-roles--permissions)
- [⚡ Rate Limiting](#-rate-limiting)
- [🛠️ Error Handling](#️-error-handling)
- [🧪 Testing the API](#-testing-the-api)
- [📚 SDKs & Clients](#-sdks--clients)

## 🎯 API Overview

The Food Truck Management System provides a comprehensive REST API built with **FastAPI**, featuring:

- 🚀 **High Performance** - Built on ASGI with async/await support
- 📖 **Interactive Docs** - Automatic OpenAPI/Swagger documentation
- 🔒 **Secure** - JWT authentication with role-based access control
- ✅ **Validated** - Automatic request/response validation with Pydantic
- 🎯 **Type Safe** - Full TypeScript-style type hints
- 📊 **Monitored** - Built-in health checks and metrics

### API Information

| Property | Value |
|----------|-------|
| **Base URL** | `http://localhost:8000` |
| **API Version** | v1 |
| **API Prefix** | `/api/v1` |
| **Documentation** | `/docs` (Swagger UI) |
| **ReDoc** | `/redoc` (Alternative docs) |
| **OpenAPI Schema** | `/openapi.json` |

### Quick Links

- **🌐 Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **📖 ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **📊 OpenAPI Schema**: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- **🔍 Health Check**: `foodtruck-cli health` (CLI command)

## 🔐 Authentication

The API uses **JWT (JSON Web Tokens)** for authentication with role-based authorization.



### Getting Access Token

**Endpoint**: `POST /api/v1/token/`

```bash
curl -X POST "http://localhost:8000/api/v1/token/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@foodtruck.com&password=admin123"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
    "username": "admin",
    "email": "admin@foodtruck.com",
    "full_name": "System Administrator",
    "role": "admin",
    "is_active": true
  }
}
```

### Using Access Token

Include the token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     http://localhost:8000/api/v1/users
```

### Token Information

| Property | Value |
|----------|-------|
| **Algorithm** | HS256 |
| **Expiration** | 1 hour (3600 seconds) |
| **Refresh** | Not implemented (planned) |
| **Claims** | sub (user_id), email, role, exp, iat |

## 📊 API Reference

### 🏥 Health & Status

#### System Health Check

**Note**: Health endpoint is planned for future implementation. Currently, health checks are available through the CLI:

```bash
# CLI health check
foodtruck-cli health
```

**Planned endpoint**: `GET /health` (not yet implemented)

---

### 🔐 Authentication Endpoints

#### Login

**`POST /api/v1/token/`**

Authenticate user and receive JWT token.

**Request**:
```http
Content-Type: application/x-www-form-urlencoded

username=admin@foodtruck.com&password=admin123
```

**Response**: [See Authentication section](#-authentication)

---

### 👥 User Management

#### List Users

**`GET /api/v1/users/`**

Get paginated list of users.

**Authorization**: Admin only

**Query Parameters**:
- `skip` (int): Records to skip (default: 0)
- `limit` (int): Records to return (default: 100, max: 100)

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/users/?skip=0&limit=10"
```

**Response**:
```json
{
  "items": [
    {
      "id": "01HX8P9G6J8K7Q9M5N3P2R1S0T",
      "username": "admin",
      "email": "admin@foodtruck.com",
      "full_name": "System Administrator",
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

#### Get User by ID

**`GET /api/v1/users/{user_id}`**

Get specific user by ID.

**Authorization**: Admin only

```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/users/01HX8P9G6J8K7Q9M5N3P2R1S0T
```

#### Create User

**`POST /api/v1/users/`**

Create new user.

**Authorization**: Admin only

**Request**:
```json
{
  "username": "johndoe",
  "email": "john@foodtruck.com",
  "full_name": "John Doe",
  "password": "secure123",
  "role": "atendente"
}
```

**Response**:
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

#### Update User

**`PATCH /api/v1/users/{user_id}`**

Update user information.

**Authorization**: Admin only

**Request**:
```json
{
  "full_name": "John Smith",
  "is_active": false
}
```

#### Delete User

**`DELETE /api/v1/users/{user_id}`**

Delete user.

**Authorization**: Admin only

**Response**: `204 No Content`

---

### 🍔 Product Management

#### List Products

**`GET /api/v1/products/`**

Get paginated list of products.

**Authorization**: All authenticated users

**Query Parameters**:
- `skip` (int): Records to skip
- `limit` (int): Records to return
- `category` (str): Filter by category
- `is_available` (bool): Filter by availability

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/products/?category=burger&is_available=true"
```

**Response**:
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

#### Get Product by ID

**`GET /api/v1/products/{product_id}`**

Get specific product.

**Authorization**: All authenticated users

#### Create Product

**`POST /api/v1/products/`**

Create new product.

**Authorization**: Admin only

**Request**:
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

#### Update Product

**`PUT /api/v1/products/{product_id}`**

Update entire product.

**Authorization**: Admin only

#### Partial Update Product

**`PATCH /api/v1/products/{product_id}`**

Update specific product fields.

**Authorization**: Admin only

**Request**:
```json
{
  "price": 32.90,
  "is_available": false
}
```

#### Delete Product

**`DELETE /api/v1/products/{product_id}`**

Delete product.

**Authorization**: Admin only

---

### 🛍️ Order Management

#### List Orders

**`GET /api/v1/orders/`**

Get paginated list of orders.

**Authorization**: All authenticated users

**Query Parameters**:
- `skip` (int): Records to skip
- `limit` (int): Records to return
- `status` (str): Filter by status
- `customer_name` (str): Filter by customer name

```bash
curl -H "Authorization: Bearer $TOKEN" \
     "http://localhost:8000/api/v1/orders/?status=pending"
```

**Response**:
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

#### Get Order by ID

**`GET /api/v1/orders/{order_id}`**

Get specific order with all details.

**Authorization**: All authenticated users

#### Create Order

**`POST /api/v1/orders/`**

Create new order.

**Authorization**: Admin, Atendente

**Request**:
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

**Response**:
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

#### Update Order Status

**`PATCH /api/v1/orders/{order_id}`**

Update order status and other fields.

**Authorization**: Admin, Atendente, Cozinha (status only)

**Request**:
```json
{
  "status": "preparing"
}
```

#### Get Order Items

**`GET /api/v1/orders/{order_id}/items`**

Get all items for a specific order.

**Authorization**: All authenticated users

#### Delete Order

**`DELETE /api/v1/orders/{order_id}`**

Delete order (only if status is pending).

**Authorization**: Admin, Atendente

---

## 🔄 Request/Response Examples

### Complete Order Workflow

#### 1. Create Order

```bash
# Create new order
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

#### 2. Update Order Status (Kitchen)

```bash
# Mark as preparing
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "preparing"}'
```

#### 3. Complete Order

```bash
# Mark as ready
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "ready"}'
```

#### 4. Deliver Order

```bash
# Mark as delivered
curl -X PATCH "http://localhost:8000/api/v1/orders/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"status": "delivered"}'
```

### Product Management Example

```bash
# Create product
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

# Update product price
curl -X PATCH "http://localhost:8000/api/v1/products/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"price": 17.90}'

# Disable product
curl -X PATCH "http://localhost:8000/api/v1/products/01HX8P9G6J8K7Q9M5N3P2R1S0T" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"is_available": false}'
```

## 📝 Data Models

### User Model

```json
{
  "id": "string (ULID)",
  "username": "string (unique)",
  "email": "string (unique, email format)",
  "full_name": "string",
  "role": "admin | atendente | cozinha",
  "is_active": "boolean",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Product Model

```json
{
  "id": "string (ULID)",
  "name": "string",
  "description": "string",
  "price": "number (decimal, >= 0)",
  "category": "burger | drink | side | dessert",
  "image_url": "string (URL, optional)",
  "is_available": "boolean",
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Order Model

```json
{
  "id": "string (ULID)",
  "localizador": "string (unique, auto-generated)",
  "customer_name": "string",
  "status": "pending | preparing | ready | delivered | cancelled",
  "total": "number (decimal, calculated)",
  "notes": "string (optional)",
  "rating": "integer (1-5, optional)",
  "items": [
    {
      "id": "string (ULID)",
      "product_id": "string (ULID)",
      "product_name": "string",
      "quantity": "integer (> 0)",
      "price": "number (decimal)",
      "subtotal": "number (decimal, calculated)"
    }
  ],
  "created_at": "datetime (ISO 8601)",
  "updated_at": "datetime (ISO 8601)"
}
```

### Error Model

```json
{
  "detail": "string (error message)",
  "type": "string (error type)",
  "code": "string (error code, optional)",
  "field": "string (field name for validation errors, optional)"
}
```

## 🎭 User Roles & Permissions

### Role Definitions

| Role | Description | Permissions |
|------|-------------|-------------|
| **👑 admin** | System administrator | Full access to all resources |
| **👥 atendente** | Sales attendant | Orders, products (read), customers |
| **👨‍🍳 cozinha** | Kitchen staff | Orders (status updates only) |

### Permission Matrix

| Resource | Admin | Atendente | Cozinha |
|----------|-------|-----------|---------|
| **Users** | CRUD | - | - |
| **Products** | CRUD | Read | Read |
| **Orders** | CRUD | CRUD | Update (status) |
| **Order Items** | CRUD | CRUD | Read |

### Role-Based Access Examples

```bash
# Admin: Create user
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{"username": "newuser", ...}'

# Atendente: Create order
curl -X POST "http://localhost:8000/api/v1/orders/" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN" \
     -d '{"customer_name": "Cliente", ...}'

# Cozinha: Update order status only
curl -X PATCH "http://localhost:8000/api/v1/orders/123" \
     -H "Authorization: Bearer $KITCHEN_TOKEN" \
     -d '{"status": "preparing"}'
```

## ⚡ Rate Limiting

**Note**: Rate limiting is planned for future implementation.

### Planned Limits

| User Type | Requests/Minute | Burst |
|-----------|-----------------|-------|
| **Admin** | 1000 | 100 |
| **Atendente** | 300 | 50 |
| **Cozinha** | 100 | 20 |
| **Unauthenticated** | 10 | 5 |

### Rate Limit Headers (Planned)

```http
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 299
X-RateLimit-Reset: 1640995200
```

## 🛠️ Error Handling

### HTTP Status Codes

| Status | Meaning | When |
|--------|---------|------|
| **200** | OK | Successful GET, PATCH |
| **201** | Created | Successful POST |
| **204** | No Content | Successful DELETE |
| **400** | Bad Request | Invalid request data |
| **401** | Unauthorized | Missing/invalid auth token |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource not found |
| **409** | Conflict | Duplicate data (email, username) |
| **422** | Unprocessable Entity | Validation errors |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Email already registered",
  "type": "validation_error",
  "code": "EMAIL_DUPLICATE"
}
```

### Validation Errors

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "price"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt",
      "ctx": {"limit_value": 0}
    }
  ]
}
```

### Common Error Scenarios

#### Authentication Errors

```bash
# Missing token
curl http://localhost:8000/api/v1/users
# Response: 401 {"detail": "Not authenticated"}

# Invalid token
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/v1/users
# Response: 401 {"detail": "Could not validate credentials"}

# Expired token
curl -H "Authorization: Bearer expired-token" http://localhost:8000/api/v1/users
# Response: 401 {"detail": "Token has expired"}
```

#### Permission Errors

```bash
# Atendente trying to create user
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ATTENDANT_TOKEN"
# Response: 403 {"detail": "Insufficient permissions"}
```

#### Validation Errors

```bash
# Invalid email format
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Authorization: Bearer $ADMIN_TOKEN" \
     -d '{"email": "invalid-email"}'
# Response: 422 with validation details
```

## 🧪 Testing the API

### Using curl

```bash
# Set base URL and token
BASE_URL="http://localhost:8000"
TOKEN="your-jwt-token"

# Test authentication
curl -X POST "$BASE_URL/api/v1/token/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@foodtruck.com&password=admin123"

# Test protected endpoint
curl -H "Authorization: Bearer $TOKEN" "$BASE_URL/api/v1/users/"
```

### Using HTTPie

```bash
# Install HTTPie
pip install httpie

# Login
http POST localhost:8000/api/v1/token/ username=admin@foodtruck.com password=admin123

# Use token
http GET localhost:8000/api/v1/users/ Authorization:"Bearer $TOKEN"

# Create order
http POST localhost:8000/api/v1/orders/ \
     Authorization:"Bearer $TOKEN" \
     customer_name="Test Customer" \
     items:='[{"product_id":"01HX8P9G6J8K7Q9M5N3P2R1S0T","quantity":1}]'
```

### Using Postman

1. **Import OpenAPI**: Use `http://localhost:8000/openapi.json`
2. **Set Environment Variables**:
   - `base_url`: `http://localhost:8000`
   - `token`: Your JWT token
3. **Authentication**: Add `Authorization: Bearer {{token}}` to headers

### Using Python Requests

```python
import requests

# Base configuration
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

# Get users
users = session.get(f"{BASE_URL}/api/v1/users").json()
print(f"Found {users['total']} users")

# Create product
product = session.post(f"{BASE_URL}/api/v1/products", json={
    "name": "Test Product",
    "description": "A test product",
    "price": 10.99,
    "category": "burger",
    "is_available": True
}).json()
print(f"Created product: {product['id']}")
```

## 📚 SDKs & Clients

### Generate Client Libraries

Use OpenAPI generators to create client libraries:

```bash
# Python client
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o python-client

# TypeScript/JavaScript client
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g typescript-fetch \
  -o typescript-client

# Java client
openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g java \
  -o java-client
```

### Python SDK Example

```python
# Generated client usage
from foodtruck_client import ApiClient, Configuration, UsersApi

config = Configuration(host="http://localhost:8000")
config.access_token = "your-jwt-token"

with ApiClient(config) as api_client:
    users_api = UsersApi(api_client)
    users = users_api.get_users()
    print(f"Total users: {users.total}")
```

### Frontend Integration (JavaScript)

```javascript
// Modern fetch API
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
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  }

  // Authentication
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

  // Products
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

  // Orders
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

// Usage
const api = new FoodTruckAPI('http://localhost:8000');

// Login
await api.login('admin@foodtruck.com', 'admin123');

// Get products
const products = await api.getProducts({ category: 'burger' });
console.log(`Found ${products.total} burgers`);

// Create order
const order = await api.createOrder({
  customer_name: 'John Doe',
  items: [
    { product_id: 'product-123', quantity: 2 }
  ]
});
console.log(`Order created: ${order.localizador}`);
```

---

## 🔗 Related Documentation

- **🚀 [Installation Guide](INSTALL.md)** - API setup and configuration
- **🛠️ [Development Guide](DEVELOPMENT.md)** - API development workflows
- **🧪 [Testing Guide](../projeto_aplicado/cli/tests/README.md)** - API testing strategies
- **🚀 [Deployment Guide](DEPLOYMENT.md)** - Production API deployment

---

<div align="center">

**🚀 Powerful REST API for Food Truck Management**

[🏠 Documentation Index](README.md) • [🌐 Interactive Docs](http://localhost:8000/docs) • [🐛 Report Issue](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)

</div>
