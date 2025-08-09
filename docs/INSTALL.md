# 🚀 Food Truck Installation Guide

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **Installation guide - uv for Python dependencies, Docker for services**

## 📋 Prerequisites

Both uv and Docker are required:
- **uv** - Python package manager
- **Docker** - For PostgreSQL and other services

## 🛠️ Installation Steps

### 1. Install Prerequisites
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installations
uv --version
docker --version
```

### 2. Project Setup
```bash
# Clone project
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Create Python environment
uv venv --python 3.13
source .venv/bin/activate

# Install dependencies
uv sync --group dev --group test
```

### 3. Environment Configuration
Create a `.env` file:
```bash
# Database
POSTGRES_HOSTNAME=localhost
POSTGRES_DB=foodtruck
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Application
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Optional
DEBUG=true
```

### 4. Start Services with Docker
```bash
# Start PostgreSQL
docker run -d --name foodtruck-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=foodtruck \
  -p 5432:5432 postgres:16

# Initialize database (auto-configures CLI aliases)
uv run python -m projeto_aplicado.cli.app database init
source ~/.zshrc  # reload shell for aliases (could be .bashrc if using bash)
# Create admin user
ft-admin create admin admin@foodtruck.com admin123 "Admin"

# Verify setup
ft-health
```

### 5. Run Application
```bash
# Start development server
uv run task dev
# Or: uvicorn projeto_aplicado.app:app --reload
```

**🎉 Access at**: http://localhost:8000/docs

---

## 🚀 Quick Start (Full Stack)
For complete setup with all services:
```bash
# Clone and enter project
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Start all services with Docker Compose
docker-compose up --build -d

# Initialize from within container
docker-compose exec api uv run python -m projeto_aplicado.cli.app database init
docker-compose exec api uv run python -m projeto_aplicado.cli.app admin create admin admin@foodtruck.com admin123 "Admin"
```

**Access at**: http://localhost:8000/docs

---

## ✅ Verification

After installation, verify everything works:

```bash
# Check system health
ft-health

# Test API
curl http://localhost:8000/docs

# List admin users
ft-admin list-admins
```

## 🔧 Common Issues

### Database Connection
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart if needed
docker restart foodtruck-postgres
```

### Port Already in Use
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process or use different port
kill -9 <PID>
# Or: uvicorn projeto_aplicado.app:app --port 8001
```

### Python Version
```bash
# Install Python 3.13 with uv
uv python install 3.13
uv venv --python 3.13
```

## 📚 Next Steps

After installation:
- **[Dependencies Guide](DEPENDENCIES.md)** - Manage dependencies with uv
- **[CLI Documentation](CLI.md)** - Use the command-line tools
- **[API Documentation](API.md)** - Learn the REST API

---

**🏠 [Documentation Index](README.md)** • **🐛 [Report Issues](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)**
