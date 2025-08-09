# 📦 Food Truck Dependencies Guide

[![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![Lock File](https://img.shields.io/badge/lock%20file-uv.lock-green.svg)](https://github.com/astral-sh/uv)

> **Complete guide to dependency management using uv for the Food Truck Management System**

## 📋 Table of Contents

- [🎯 Overview](#-overview)
- [🚀 uv Introduction](#-uv-introduction)
- [📦 Project Dependencies](#-project-dependencies)
- [🔧 Dependency Management](#-dependency-management)
- [🛠️ Development Workflow](#️-development-workflow)
- [🔒 Security & Updates](#-security--updates)
- [🧪 Testing Dependencies](#-testing-dependencies)
- [🎨 Code Quality Tools](#-code-quality-tools)
- [📚 Documentation Tools](#-documentation-tools)
- [🔍 Troubleshooting](#-troubleshooting)

## 🎯 Overview

The Food Truck project uses **[uv](https://github.com/astral-sh/uv)** as its primary package manager. uv is a modern, fast Python package manager that provides:

- ⚡ **Ultra-fast** dependency resolution and installation
- 🔒 **Secure** lock file generation with integrity hashes
- 🎯 **Simple** configuration through `pyproject.toml`
- 🔄 **Reliable** reproducible builds across environments
- 🛠️ **Compatible** with pip and existing Python ecosystem

### Why uv?

| Feature | pip | poetry | uv |
|---------|-----|--------|----|
| **Speed** | Slow | Medium | Ultra-fast |
| **Lock Files** | ❌ | ✅ | ✅ |
| **Resolver** | Basic | Good | Excellent |
| **Standards** | Limited | Custom | PEP 621 |
| **Security** | Basic | Good | Excellent |

## 🚀 uv Introduction

### Installation

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: pip install
pip install uv

# Verify installation
uv --version
```

### Basic Commands

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -e ".[dev]"

# Add new dependency
uv add fastapi

# Remove dependency
uv remove package-name

# Update all dependencies
uv pip install --upgrade-eager -e ".[dev]"

# Sync with lock file
uv sync
```

## 📦 Project Dependencies

### 🎯 Clean Dependency Architecture

The project uses a **well-organized, production-ready** dependency structure:

```toml
[project]
dependencies = [
    # Pure production runtime dependencies (no testing/dev tools)
]

[dependency-groups]
dev = [
    # Development tools + testing framework
]

test = [
    # Testing infrastructure only
]
```

### 🚀 Production Dependencies (Runtime Only)

```toml
[project]
dependencies = [
    # Web Framework
    "fastapi[standard]>=0.115.12,<0.116.0",  # Modern async web framework
    "uvicorn[standard]>=0.34.2,<0.35.0",     # ASGI server
    "pydantic-settings>=2.9.1,<2.10.0",      # Configuration management
    
    # Database
    "sqlmodel>=0.0.24,<0.0.25",              # Type-safe SQL ORM
    "sqlalchemy[asyncio]>=2.0.41,<2.1.0",    # Async database toolkit
    "alembic>=1.16.1,<1.17.0",               # Database migrations
    "asyncpg>=0.30.0,<0.31.0",               # PostgreSQL async driver
    "psycopg2-binary>=2.9.10,<2.10.0",       # PostgreSQL sync driver
    
    # Authentication & Security
    "pyjwt>=2.10.1,<2.11.0",                 # JWT tokens
    "passlib[argon2]>=1.7.4,<1.8.0",         # Password hashing
    "pwdlib[argon2]>=0.2.1,<0.3.0",          # Modern password utilities
    "email-validator>=2.2.0,<2.3.0",         # Email validation
    
    # CLI Framework
    "cyclopts>=3.22.5",                       # Modern CLI framework
    "argcomplete>=3.0.0,<4.0.0",             # Shell completion
    
    # Utilities
    "python-ulid>=3.0.0,<4.0.0",             # ULID generation
    "redis>=6.1.0,<7.0.0",                   # Redis caching
]
```

### 🛠️ Development Dependencies

```toml
[dependency-groups]
dev = [
    # Development Tools
    "taskipy>=1.14.1",        # Task runner
    "ignr>=2.2",              # .gitignore generator
    
    # Code Quality
    "ruff>=0.11.11",          # Fast linting & formatting
    
    # Testing Framework
    "pytest>=8.3.5",          # Testing framework
    "pytest-cov>=6.1.1",      # Coverage reporting
    "pytest-asyncio>=1.0.0,<1.1.0",  # Async testing support
]

test = [
    # Testing Infrastructure
    "aiosqlite>=0.21.0,<0.22.0",             # SQLite for tests
    "testcontainers[postgres]>=4.10.0,<5.0.0",  # Container testing
]
```

### 🎯 Why This Organization?

| Approach | Benefit | Use Case |
|----------|---------|----------|
| **🎯 Pure Production** | Clean runtime dependencies | Docker production images |
| **🛠️ Development Group** | All dev tools together | Local development |
| **🧪 Test Group** | Heavy testing infrastructure | CI/CD environments |
| **📦 Logical Grouping** | Easy to understand and maintain | Team collaboration |

## 🔧 Essential Dependency Commands

### 🚀 Development Setup

```bash
# Simple uv approach (recommended)
uv venv --python 3.13
source .venv/bin/activate
uv sync --group dev --group test

# First run auto-configures convenient aliases
uv run python -m projeto_aplicado.cli.app

# Reload shell and use short commands
source ~/.zshrc  # or ~/.bashrc
ft-health
```

### 🔒 Production Setup

```bash
# Production only (clean runtime dependencies)
uv venv --python 3.13
source .venv/bin/activate
uv sync --no-group dev --no-group test

# Verify
uv run python -m projeto_aplicado.cli.app health
```

### 🎯 **CLI Access Methods**

**Default: Use the simplest approach**

| Method | Global Access | Live Changes | Setup | Complexity | Use Case |
|--------|---------------|-------------|--------|-----------|-----------|
| **`uv run python -m ...`** ⭐ | ❌ Project-local | ✅ Yes | None | 🟢 **Simplest** | **Default choice** |
| **`uv tool install --editable .`** | ✅ `foodtruck-cli` | ✅ Yes | One command | 🟡 Simple | Global convenience |
| **`uv sync` + `uv pip install -e .`** | ✅ `foodtruck-cli` | ✅ Yes | Two commands | 🔴 Complex | Legacy/special cases |

### 🏆 **Default Approach: Simple uv workflow with auto-aliases**

```bash
# Setup once
uv sync --group dev --group test

# First run auto-configures aliases
uv run python -m projeto_aplicado.cli.app

# Reload shell and use convenient commands
source ~/.zshrc  # or ~/.bashrc
ft-health
ft-admin list-admins
ft-db status

# Development tools (still use uv run)
uv run pytest
uv run ruff check .
uv run task test          # runs: pytest -s -x --cov=projeto_aplicado
uv run task lint          # runs: ruff check . && ruff check . --diff
```

### 🔧 **Alternative: Global CLI access (optional)**

```bash
# If you want foodtruck-cli command globally
uv tool install --editable .

# Now works from anywhere
foodtruck-cli health
foodtruck-cli admin list-admins

# Manage global tools
uv tool list                    # See installed tools
uv tool uninstall projeto-aplicado  # Remove if needed
```

## 🔧 Alternative: Understanding `uv pip install -e .` (Optional)

> **Note**: This section is for advanced users or special cases. The recommended approach is `uv sync + uv run` above.

### **What is Editable Installation?**

The `-e` (editable) flag installs the project in **development mode**, creating a live link between your source code and the installed package.

```bash
# Standard installation (copies files)
uv pip install .

# Editable installation (creates links)
uv pip install -e .
```

### **🎯 Why Do We Need This?**

1. **CLI Entry Points**: Enables `foodtruck-cli` command globally
2. **Live Code Changes**: Edits to Python files are immediately available
3. **Import Path**: Allows `import projeto_aplicado` from anywhere
4. **No Reinstallation**: Changes don't require `pip install` again

### **📦 Installation Variants Explained**

#### **1. Basic Editable Install**
```bash
uv pip install -e .
# ✅ Installs only [project] dependencies
# ✅ Enables CLI entry points
# ❌ No development tools (ruff, pytest)
# 📍 Use: Production or minimal development
```

#### **2. Editable with Groups (Modern uv)**
```bash
# This syntax doesn't work yet in uv pip install
uv pip install -e ".[dev,test]"  # ⚠️ Produces warnings

# Use this instead:
uv sync --group dev --group test  # Install dependencies
uv pip install -e .               # Enable entry points
```

#### **3. Editable with Optional Dependencies (Traditional)**
```bash
# If using [project.optional-dependencies] format:
uv pip install -e ".[dev]"      # Install with dev extras
uv pip install -e ".[test]"     # Install with test extras
uv pip install -e ".[dev,test]" # Install with multiple extras
```

#### **4. Non-Editable Production Install**
```bash
uv pip install .
# ✅ Installs package normally
# ✅ Enables CLI entry points
# ❌ No live code changes
# 📍 Use: Docker production images
```

### **🔍 What Happens During Installation?**

```bash
uv pip install -e .
```

**Behind the scenes:**
1. **Reads `pyproject.toml`** for project metadata
2. **Creates `.egg-info/`** directory with package info
3. **Installs entry points** (`foodtruck-cli` → `projeto_aplicado.cli.app:app`)
4. **Creates link** in site-packages pointing to your source code
5. **Adds to Python path** so imports work

### **📁 File System Changes**

#### **After `uv pip install -e .` (Editable)**
```bash
# In project directory
ls -la
# Creates: projeto_aplicado.egg-info/

ls projeto_aplicado.egg-info/
# Files: entry_points.txt, PKG-INFO, requires.txt, etc.

cat projeto_aplicado.egg-info/entry_points.txt
# [console_scripts]
# foodtruck-cli = projeto_aplicado.cli.app:app

# In virtual environment
ls .venv/lib/python3.13/site-packages/ | grep projeto
# __editable___projeto_aplicado_0_1_0_finder.py
# __editable__.projeto_aplicado-0.1.0.pth
# projeto_aplicado-0.1.0.dist-info

which foodtruck-cli
# /path/to/.venv/bin/foodtruck-cli
```

#### **After `uv pip install .` (Non-Editable)**
```bash
# In virtual environment
ls .venv/lib/python3.13/site-packages/
# projeto_aplicado/          <- Full copy of source code
# projeto_aplicado-0.1.0.dist-info/

# No .egg-info in project directory
ls -la | grep egg-info
# (nothing - no development files created)
```

### **🔄 Live Changes Demonstration**

#### **Editable Mode Benefits**
```bash
# Install in editable mode
uv pip install -e .

# Make a change to any Python file
echo '# Modified' >> projeto_aplicado/cli/app.py

# Change is immediately available (no reinstall needed)
foodtruck-cli health  # Uses modified code instantly
```

#### **Non-Editable Mode Limitation**
```bash
# Install in non-editable mode
uv pip install .

# Make a change to any Python file
echo '# Modified' >> projeto_aplicado/cli/app.py

# Change is NOT available until reinstall
foodtruck-cli health  # Still uses old code
uv pip install .     # Must reinstall to see changes
```

### **🚫 Common Issues & Solutions**

#### **Issue 1: CLI Not Found**
```bash
foodtruck-cli health
# error: command not found
```
**Solution:**
```bash
# Make sure you've installed in editable mode
uv pip install -e .

# Verify entry points are installed
pip show projeto-aplicado | grep "Entry-points"
```

#### **Issue 2: Import Errors**
```bash
python -c "import projeto_aplicado"
# ModuleNotFoundError: No module named 'projeto_aplicado'
```
**Solution:**
```bash
# Install in editable mode
uv pip install -e .

# Verify installation
python -c "import projeto_aplicado; print(projeto_aplicado.__file__)"
```

#### **Issue 3: uv Warnings**
```bash
uv pip install -e ".[dev,test]"
# warning: The package does not have an extra named `test`
```
**Solution:**
```bash
# Use modern dependency groups instead
uv sync --group dev --group test
uv pip install -e .
```

### **🎯 Best Practices**

#### **Development Workflow**
```bash
# 1. Install dependencies
uv sync --group dev --group test

# 2. Enable editable mode
uv pip install -e .

# 3. Verify everything works
foodtruck-cli health
uv run pytest
```

#### **Production Workflow**
```bash
# Option 1: Editable (for containers with live code)
uv sync --no-group dev --no-group test
uv pip install -e .

# Option 2: Non-editable (for packaged deployment)
uv sync --no-group dev --no-group test
uv pip install .
```

#### **CI/CD Workflow**
```bash
# Install everything for testing
uv sync --group dev --group test
uv pip install -e .

# Run tests
uv run pytest
```

### **🎯 When to Use Each Approach**

| Scenario | Command | Why |
|----------|---------|-----|
| **Local Development** | `uv pip install -e .` | Live code changes, debugging |
| **Docker Development** | `uv pip install -e .` | Mount source code, see changes |
| **Production Container** | `uv pip install .` | Immutable, no dev files |
| **Package Distribution** | `uv pip install .` | Clean installation |
| **CI/CD Testing** | `uv pip install -e .` | Better error traces |
| **Code Coverage** | `uv pip install -e .` | Accurate source mapping |

### **🚀 Quick Reference**

```bash
# Default: Simple uv workflow
uv sync --group dev --group test
uv run python -m projeto_aplicado.cli.app health

# Optional: Global CLI convenience
uv tool install --editable .
foodtruck-cli health

# Production: Clean runtime only
uv sync --no-group dev --no-group test
uv run python -m projeto_aplicado.cli.app health
```

### **🔄 When You Might Still Need uv pip install -e .**

You only need the more complex approach if:

1. **You want `foodtruck-cli` directly** (without `uv run`)
2. **Docker containers** need entry points
3. **IDE integration** requires installed package
4. **Legacy workflows** depend on pip install

```bash
# Only if you need foodtruck-cli directly
uv sync --group dev --group test
uv pip install -e .  # Now foodtruck-cli works without uv run
```

### 🛠️ Specific Environments

```bash
# Local development only (code quality tools)
uv sync --group dev --no-group test

# CI/CD testing environment (everything)
uv sync --group dev --group test

# Production (runtime only)
uv sync --no-group dev --no-group test

# Install everything (development + testing)
uv sync --all-groups
```

### 🔄 Dependency Management

```bash
# Add new runtime dependency
uv add fastapi-users
uv lock

# Add development tool
uv add --group dev black

# Add testing infrastructure
uv add --group test factory-boy

# Remove dependency
uv remove package-name
uv lock

# Update all dependencies
uv lock --upgrade
uv sync
```

> **🎯 uv Benefits:**
> - **`uv sync`**: Installs exact versions from lock file (reproducible)
> - **`--group`**: Installs specific dependency groups only
> - **`--frozen`**: Production mode - no dependency resolution
> - **`uv lock`**: Updates lock file with current constraints

## 🧪 Testing & Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=projeto_aplicado

# Run specific test
uv run pytest tests/test_api_users.py

# Run tests in parallel
uv run pytest -n auto
```

> **Why `uv run`?** Automatically uses the virtual environment and ensures consistent dependency versions.

### Code Quality

```bash
# Lint and format code
uv run ruff check .          # Check for issues
uv run ruff check . --fix    # Auto-fix issues
uv run ruff format .         # Format code

# Run all quality checks
uv run task lint    # Using taskipy
uv run task format  # Using taskipy
```

### CLI Development

```bash
# Test CLI commands
uv run foodtruck-cli health
uv run foodtruck-cli admin create test test@example.com pass123
uv run foodtruck-cli database status

# Run development server
uv run task dev  # FastAPI development server
```

## 🔒 Security & Updates

### Weekly Maintenance

```bash
# 1. Update dependencies
uv lock --upgrade
uv sync

# 2. Run tests
uv run pytest

# 3. Check for security issues
uv pip audit
```

### Version Pinning Strategy

```toml
# Conservative (recommended for production)
"fastapi>=0.115.12,<0.116.0"    # Pin minor version
"sqlmodel>=0.0.24,<0.0.25"      # Pin patch version

# Flexible (for development tools)
"pytest>=8.3.5"                 # Allow minor updates
"ruff>=0.11.11"                  # Latest features
```

## 🔍 Troubleshooting

### Quick Fixes

```bash
# Dependency conflicts
uv pip check
uv lock --upgrade

# Cache issues
uv cache clean
rm -rf .venv && uv venv && uv sync

# Lock file issues
rm uv.lock && uv lock
```

### Environment Issues

```bash
# Debug dependency tree
uv pip show --verbose package-name

# Check environment
uv pip list
uv pip list --outdated
```

---

## 🔗 Related Documentation

- **📦 [Installation Guide](INSTALL.md)** - Complete setup instructions
- **🛠️ [Development Guide](DEVELOPMENT.md)** - Development workflows
- **🚀 [Deployment Guide](DEPLOYMENT.md)** - Production deployment
- **🧪 [Testing Guide](../projeto_aplicado/cli/tests/README.md)** - Testing strategies

---

<div align="center">

**📦 Modern dependency management with uv**

[🏠 Documentation Index](README.md) • [🐛 Report Issue](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues) • [💡 Request Feature](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)

</div>
