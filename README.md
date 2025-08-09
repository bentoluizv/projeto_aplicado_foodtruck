# 🚚 Food Truck Management System

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Test Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](https://github.com/bentoluizv/projeto_aplicado_foodtruck)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🎓 Projeto Aplicado SENAI 2025** - Modern food truck management system with clean architecture, auto-configuring CLI, and robust API.

## 📚 **[📖 Complete Documentation Center →](docs/README.md)**

**All guides, tutorials, and references organized by role and purpose**

### 🚀 Quick Links

| Need | Guide |
|------|-------|
| **Get Started** | [Installation Guide](docs/INSTALL.md) |
| **Use the API** | [API Reference](docs/API.md) |
| **Use the CLI** | [CLI Documentation](docs/CLI.md) |
| **Deploy to Production** | [Deployment Guide](docs/DEPLOYMENT.md) |

## 🎯 What is this?

Modern food truck management system with **FastAPI** API, **auto-configuring CLI**, and **clean architecture**.

**Key highlights**: JWT auth • Self-configuring CLI • 94% test coverage • Docker ready

## 🚀 Quick Start

```bash
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck
uv venv --python 3.13 && source .venv/bin/activate
uv sync --group dev --group test
docker run -d --name foodtruck-postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=foodtruck postgres:16
uv run python -m projeto_aplicado.cli.app database init
uv run task dev
```

**🎉 Running at**: http://localhost:8000/docs

---

## 📚 **[📖 Full Documentation →](docs/README.md)**

---

**🏠 [Documentation Index](docs/README.md)** • **🐛 [Report Issues](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)** • **💡 [Request Features](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)**