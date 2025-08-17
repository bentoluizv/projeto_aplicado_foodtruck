# 🚀 Guia de Instalação do Food Truck

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

> **Guia de instalação - uv para dependências Python, Docker para serviços**

## 📋 Pré-requisitos

Tanto uv quanto Docker são necessários:
- **uv** - Gerenciador de pacotes Python
- **Docker** - Para PostgreSQL e outros serviços

## 🛠️ Passos de Instalação

### 1. Instalar Pré-requisitos
```bash
# Instalar uv (gerenciador de pacotes Python)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verificar instalações
uv --version
docker --version
```

### 2. Configuração do Projeto
```bash
# Clonar projeto
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Criar ambiente Python
uv venv --python 3.13
source .venv/bin/activate

# Instalar dependências
uv sync --group dev --group test
```

### 3. Configuração do Ambiente
Criar um arquivo `.env`:
```bash
# Banco de dados
POSTGRES_HOSTNAME=localhost
POSTGRES_DB=foodtruck
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Aplicação
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Opcional
DEBUG=true
```

### 4. Iniciar Serviços com Docker
```bash
# Iniciar PostgreSQL
docker run -d --name foodtruck-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=foodtruck \
  -p 5432:5432 postgres:16

# Inicializar banco de dados (auto-configura aliases CLI)
uv run python -m projeto_aplicado.cli.app database init
source ~/.zshrc  # recarregar shell para aliases (pode ser .bashrc se usar bash)
# Criar usuário admin
ft-admin create admin admin@foodtruck.com admin123 "Admin"

# Verificar configuração
ft-health
```

### 5. Executar Aplicação
```bash
# Iniciar servidor de desenvolvimento
uv run task dev
# Ou: uvicorn projeto_aplicado.app:app --reload
```

**🎉 Acesse em**: http://localhost:8000/docs

---

## 🚀 Início Rápido (Stack Completo)
Para configuração completa com todos os serviços:
```bash
# Clonar e entrar no projeto
git clone https://github.com/bentoluizv/projeto_aplicado_foodtruck.git
cd projeto_aplicado_foodtruck

# Iniciar todos os serviços com Docker Compose
docker-compose up --build -d

# Inicializar de dentro do container
docker-compose exec api uv run python -m projeto_aplicado.cli.app database init
docker-compose exec api uv run python -m projeto_aplicado.cli.app admin create admin admin@foodtruck.com admin123 "Admin"
```

**Acesse em**: http://localhost:8000/docs

---

## ✅ Verificação

Após a instalação, verifique se tudo funciona:

```bash
# Verificar saúde do sistema
ft-health

# Testar API
curl http://localhost:8000/docs

# Listar usuários admin
ft-admin list-admins
```

## 🔧 Problemas Comuns

### Conexão com Banco de Dados
```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Reiniciar se necessário
docker restart foodtruck-postgres
```

### Porta Já em Uso
```bash
# Verificar o que está usando a porta 8000
lsof -i :8000

# Matar processo ou usar porta diferente
kill -9 <PID>
# Ou: uvicorn projeto_aplicado.app:app --port 8001
```

### Versão Python
```bash
# Instalar Python 3.13 com uv
uv python install 3.13
uv venv --python 3.13
```

## 📚 Próximos Passos

Após a instalação:
- **[Guia de Dependências](DEPENDENCIES.md)** - Gerenciar dependências com uv
- **[Documentação CLI](CLI.md)** - Usar as ferramentas de linha de comando
- **[Documentação API](API.md)** - Aprender a API REST

---

**🏠 [Índice da Documentação](README.md)** • **🐛 [Reportar Problemas](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues)**
