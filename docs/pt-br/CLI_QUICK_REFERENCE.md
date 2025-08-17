# 🚚 Food Truck CLI - Referência Rápida

> **Referência rápida de comandos para o CLI do Sistema de Gerenciamento de Food Truck**

## 📋 Visão Geral dos Comandos

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `health` | Verificação de saúde do sistema | `foodtruck-cli health` |
| `admin` | Gerenciamento de usuários | `foodtruck-cli admin create <user> <email> <pass> <name>` |
| `database` | Operações de banco de dados | `foodtruck-cli database init` |
| `setup` | Configuração de shell | `foodtruck-cli setup install` |
| `completions` | Completamentos com tab | `foodtruck-cli completions install` |
| `version` | Mostrar informações de versão | `foodtruck-cli version` |

## 🚀 Início Rápido

```bash
# 1. Verificar saúde do sistema
foodtruck-cli health

# 2. Inicializar banco de dados
foodtruck-cli database init

# 3. Criar usuário admin
foodtruck-cli admin create admin admin@foodtruck.com admin123 "Administrador do Sistema"

# 4. Configurar acesso ao shell
foodtruck-cli setup install

# 5. Instalar completamentos
foodtruck-cli completions install
```

## 🏥 Comandos Health

```bash
# Verificação básica de saúde
foodtruck-cli health

# Host de banco de dados personalizado
foodtruck-cli health --db-host meuservidor.com
```

## 👥 Comandos Admin

```bash
# Criar usuário admin
foodtruck-cli admin create <username> <email> <password> <full_name>

# Verificar se admin existe
foodtruck-cli admin check <email>

# Listar todos os admins
foodtruck-cli admin list-admins

# Forçar criação (sobrescrever)
foodtruck-cli admin create admin admin@test.com pass123 "Admin" --force
```

## 💾 Comandos de Banco de Dados

```bash
# Inicializar banco de dados
foodtruck-cli database init

# Verificar status do banco de dados
foodtruck-cli database status

# Gerenciamento de migrações
foodtruck-cli database upgrade           # Atualizar para a mais recente
foodtruck-cli database upgrade abc123    # Atualizar para revisão específica
foodtruck-cli database downgrade -1      # Fazer downgrade uma revisão
foodtruck-cli database current           # Mostrar revisão atual
foodtruck-cli database history           # Mostrar histórico de migrações

# Criar nova migração
foodtruck-cli database create "descrição"

# Resetar banco de dados (⚠️ destrutivo)
foodtruck-cli database reset --confirm
```

## ⚙️ Comandos Setup

```bash
# Mostrar configuração PATH
foodtruck-cli setup path

# Gerar aliases de shell
foodtruck-cli setup alias [bash|zsh|fish]

# Auto-configurar shell
foodtruck-cli setup install [--shell bash|zsh|fish] [--force]

# Verificar configuração atual
foodtruck-cli setup check
```

## 🔧 Comandos de Completamento

```bash
# Instalar completamentos para shell atual
foodtruck-cli completions install

# Instalar para shell específico
foodtruck-cli completions install bash
foodtruck-cli completions install zsh
foodtruck-cli completions install fish

# Gerar script de completamento
foodtruck-cli completions generate bash --output script.bash

# Verificar status de completamento
foodtruck-cli completions status

# Remover completamentos
foodtruck-cli completions uninstall [bash|zsh|fish|all]
```

## 🎯 Fluxos de Trabalho Comuns

### Configuração Inicial
```bash
foodtruck-cli health
foodtruck-cli database init
foodtruck-cli admin create admin admin@foodtruck.com admin123 "Admin"
foodtruck-cli setup install
foodtruck-cli completions install
```

### Migração de Banco de Dados
```bash
foodtruck-cli database status
foodtruck-cli database create "nova migração"
foodtruck-cli database upgrade
foodtruck-cli database current
```

### Ambiente de Desenvolvimento
```bash
uv pip install -e .[dev]
foodtruck-cli health
foodtruck-cli setup install
foodtruck-cli completions install
```

## 🐚 Integração com Shell

### Aliases Gerados
Após `foodtruck-cli setup install`:
- `ftcli` → `foodtruck-cli`
- `ft-health` → `foodtruck-cli health`
- `ft-admin` → `foodtruck-cli admin`
- `ft-db` → `foodtruck-cli database`

### Completamento com Tab
Após `foodtruck-cli completions install`:
```bash
foodtruck-cli <TAB><TAB>    # Mostra todos os comandos
foodtruck-cli admin <TAB>   # Mostra subcomandos admin
foodtruck-cli setup install --shell <TAB>  # Mostra opções de shell
```

## 🔍 Solução de Problemas

### Comando Não Encontrado
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Ou configurar acesso permanente
foodtruck-cli setup install
```

### Problemas de Banco de Dados
```bash
# Verificar conexão
foodtruck-cli health

# Verificar status do PostgreSQL
sudo systemctl status postgresql

# Verificar variáveis de ambiente
echo $POSTGRES_HOSTNAME $POSTGRES_DB
```

### Problemas de Permissão
```bash
# Verificar diretório de completamento
ls -la ~/.zsh/completion/

# Corrigir permissões
chmod 755 ~/.zsh/completion/
```

## 📖 Comandos de Ajuda

```bash
# Ajuda geral
foodtruck-cli --help

# Ajuda específica do comando
foodtruck-cli <command> --help

# Ajuda de subcomando
foodtruck-cli <command> <subcommand> --help
```

## 🌍 Variáveis de Ambiente

```bash
# Configuração do banco de dados
export POSTGRES_HOSTNAME=localhost
export POSTGRES_DB=foodtruck
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password

# Configurações da aplicação
export SECRET_KEY=sua-chave-secreta
```

---

📖 **[Documentação Completa](CLI.md)** | 🚚 **[Projeto Principal](../README.md)**
