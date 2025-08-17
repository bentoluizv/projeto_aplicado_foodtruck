# 🚚 Documentação CLI do Food Truck

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![CLI Framework](https://img.shields.io/badge/CLI-Cyclopts-green.svg)](https://github.com/BrianPugh/cyclopts)
[![Architecture](https://img.shields.io/badge/architecture-Clean%20Architecture-orange.svg)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

> **CLI Moderno para Sistema de Gerenciamento de Food Truck** - Construído com Arquitetura Limpa, princípios SOLID e testes abrangentes.

## 📋 Índice

- [🎯 Visão Geral](#-visão-geral)
- [🚀 Início Rápido](#-início-rápido)
- [📦 Instalação](#-instalação)
- [🛠️ Referência de Comandos](#️-referência-de-comandos)
- [🏗️ Arquitetura](#️-arquitetura)
- [💡 Exemplos](#-exemplos)
- [🧪 Testes](#-testes)
- [📚 Solução de Problemas](#-solução-de-problemas)

## 🎯 Visão Geral

O CLI do Food Truck é uma interface de linha de comando abrangente para gerenciar o Sistema de Gerenciamento de Food Truck. Ele fornece ferramentas para:

- **Monitoramento de Saúde do Sistema** - Verificar conexões de banco de dados e status do sistema
- **Gerenciamento de Usuários** - Criar e gerenciar usuários administradores
- **Operações de Banco de Dados** - Lidar com migrações, mudanças de esquema e configuração de banco de dados
- **Configuração de Shell** - Configuração fácil para acesso direto ao CLI
- **Suporte a Completions** - Completamento com Tab para shells bash, zsh e fish

### ✨ Características Principais

- 🏗️ **Arquitetura Limpa** - Segue princípios SOLID com separação clara de responsabilidades
- 🧪 **100% Testado** - Cobertura abrangente de testes para todos os componentes
- 🎨 **Saída Rica** - Saída de console bonita e colorida com emojis e formatação
- 🐚 **Integração com Shell** - Suporte nativo a completamento para shells principais
- 🔒 **Seguro** - Operações seguras de banco de dados com validação e tratamento de erros
- ⚡ **Rápido** - Otimizado para operações rápidas e tempo mínimo de inicialização
- 🎯 **Auto-Configuração** - Configura automaticamente aliases convenientes no primeiro uso

## 🚀 Início Rápido

### Pré-requisitos

- Python 3.13+
- PostgreSQL (para operações de banco de dados)
- Ambiente virtual ativado

### Uso Básico

```bash
# Primeira vez: Auto-configura aliases convenientes
uv run python -m projeto_aplicado.cli.app

# Após configuração, use aliases curtos
source ~/.zshrc  # ou ~/.bashrc
ftcli health
ft-admin list-admins
ft-db status

# Ou continue usando comandos completos
uv run python -m projeto_aplicado.cli.app health
uv run python -m projeto_aplicado.cli.app database init
uv run python -m projeto_aplicado.cli.app admin create admin admin@foodtruck.com admin123 "Administrador do Sistema"
```

## 📦 Instalação

### 🚀 Configuração Rápida (Recomendado)

```bash
# 1. Da raiz do projeto
cd /caminho/para/foodtruck
source .venv/bin/activate

# 2. Primeira execução auto-configura aliases
uv run python -m projeto_aplicado.cli.app

# 3. Recarregar shell para usar comandos curtos
source ~/.zshrc  # ou ~/.bashrc

# 4. Agora use aliases convenientes
ftcli health
ft-admin list-admins
```

### 🔧 Alternativa: Acesso Global CLI

```bash
# Instalar globalmente com uv tool
uv tool install --editable .

# Agora disponível globalmente
foodtruck-cli --help

# Auto-configurar seu shell (se necessário)
foodtruck-cli setup install
```

## 🎯 Recurso de Auto-Configuração

O CLI configura automaticamente aliases convenientes no primeiro uso para melhorar sua produtividade:

### O que Acontece no Primeiro Uso

1. **Detecção** - Verifica se aliases já estão configurados
2. **Detecção de Shell** - Identifica seu shell (bash, zsh, fish)
3. **Auto-Configuração** - Adiciona aliases ao seu arquivo de configuração do shell
4. **Feedback de Sucesso** - Mostra o que foi configurado

### Aliases Auto-Gerados

| Alias | Comando Completo | Descrição |
|-------|------------------|-----------|
| `ftcli` | `cd /projeto && uv run python -m projeto_aplicado.cli.app` | CLI Principal |
| `ft-health` | `ftcli health` | Verificação rápida de saúde |
| `ft-admin` | `ftcli admin` | Comandos de admin |
| `ft-db` | `ftcli database` | Operações de banco de dados |
| `ft-setup` | `ftcli setup` | Comandos de configuração |
| `ft-completions` | `ftcli completions` | Gerenciamento de completamento |

### Benefícios

- ✅ **Funciona de qualquer lugar** - Aliases incluem `cd` para o diretório do projeto
- ✅ **Sem configuração manual** - Configurado automaticamente no primeiro uso
- ✅ **Consciente do shell** - Detecta e configura o shell correto
- ✅ **Apenas uma vez** - Não duplica configuração em usos subsequentes
- ✅ **Fluxo de trabalho uv puro** - Usa `uv run` para máxima compatibilidade

### Controle Manual

```bash
# Pular auto-configuração usando comandos de setup diretamente
uv run python -m projeto_aplicado.cli.app setup install --help
uv run python -m projeto_aplicado.cli.app setup alias

# Remover aliases (manual)
# Editar ~/.zshrc ou ~/.bashrc e remover seção "Food Truck CLI aliases"
```

## 🛠️ Referência de Comandos

### 🏥 Comando Health

Verificar saúde do sistema e conectividade.

```bash
# Verificação básica de saúde (com aliases)
ft-health

# Usando comando completo
uv run python -m projeto_aplicado.cli.app health

# Verificar com host de banco de dados personalizado
ftcli health --db-host mydb.example.com
```

**O que verifica:**
- ✅ Conectividade do banco de dados
- ✅ Presença de usuários admin
- ✅ Configurações da aplicação
- ✅ Configuração do sistema

**Exemplo de Saída:**
```
🏥 Verificação de Saúde do Sistema
✓ Conexão com banco de dados: OK
✓ Usuários admin: 2 encontrados
✓ Configurações carregadas: OK
  Banco de dados: foodtruck
  Host: localhost:5432
🎉 Todas as 3 verificações de saúde passaram!
```

### 👥 Comandos Admin

Gerenciar usuários administrativos no sistema.

#### Criar Usuário Admin

```bash
foodtruck-cli admin create <username> <email> <password> <full_name> [--force]
```

**Exemplos:**
```bash
# Criar admin básico (com aliases)
ft-admin create admin admin@foodtruck.com admin123 "Administrador do Sistema"

# Forçar criação (sobrescrever existente)
ft-admin create superadmin admin@empresa.com secret123 "Super Admin" --force

# Usando comando completo
uv run python -m projeto_aplicado.cli.app admin create admin admin@foodtruck.com admin123 "Administrador do Sistema"
```

#### Verificar Usuário Admin

```bash
foodtruck-cli admin check <email>
```

**Exemplo:**
```bash
foodtruck-cli admin check admin@foodtruck.com
# Saída: ✓ Usuário encontrado: admin (admin@foodtruck.com) - Administrador do Sistema
```

#### Listar Usuários Admin

```bash
foodtruck-cli admin list-admins
```

**Exemplo de Saída:**
```
✓ Encontrados 2 usuário(s) admin:
  • admin (admin@foodtruck.com) - Administrador do Sistema
  • superadmin (admin@empresa.com) - Super Administrador
```

### 💾 Comandos de Banco de Dados

Lidar com migrações de banco de dados e gerenciamento de esquema.

#### Inicializar Banco de Dados

```bash
foodtruck-cli database init
```

Configura o esquema do banco de dados e executa todas as migrações.

#### Status do Banco de Dados

```bash
foodtruck-cli database status
```

**Exemplo de Saída:**
```
📊 Status do Banco de Dados
✓ Conexão com banco de dados: OK
✓ Configuração Alembic: OK
✓ Diretório de migrações: Encontrado
ℹ Migração atual: ca713c51cd3c (head)
```

#### Gerenciamento de Migrações

```bash
# Atualizar para a mais recente
foodtruck-cli database upgrade

# Atualizar para revisão específica
foodtruck-cli database upgrade abc123

# Fazer downgrade uma revisão
foodtruck-cli database downgrade -1

# Mostrar revisão atual
foodtruck-cli database current

# Mostrar histórico de migrações
foodtruck-cli database history
```

#### Criar Migração

```bash
foodtruck-cli database create "adicionar tabela de perfil de usuário"
```

#### Resetar Banco de Dados (⚠️ Destrutivo)

```bash
foodtruck-cli database reset --confirm
```

### ⚙️ Comandos de Setup

Configurar ambiente de shell para uso otimizado do CLI.

#### Mostrar Configuração PATH

```bash
foodtruck-cli setup path
```

Mostra a configuração PATH atual e fornece instruções de instalação manual.

#### Gerar Aliases de Shell

```bash
# Auto-detectar shell
foodtruck-cli setup alias

# Shell específico
foodtruck-cli setup alias zsh
```

**Aliases gerados:**
- `ftcli` → `foodtruck-cli`
- `ft-health` → `foodtruck-cli health`
- `ft-admin` → `foodtruck-cli admin`
- `ft-db` → `foodtruck-cli database`

#### Auto-Instalar Configuração de Shell

```bash
# Auto-configurar shell atual
foodtruck-cli setup install

# Forçar sobrescrever configuração existente
foodtruck-cli setup install --force

# Shell específico
foodtruck-cli setup install zsh
```

#### Verificar Configuração de Shell

```bash
foodtruck-cli setup check
```

Mostra o status atual da configuração do shell e acessibilidade.

### 🔧 Comandos de Completions

Gerenciar completamentos de tab do shell.

#### Instalar Completions

```bash
# Auto-instalar para shell atual
foodtruck-cli completions install

# Shell específico
foodtruck-cli completions install bash
foodtruck-cli completions install zsh
foodtruck-cli completions install fish
```

#### Gerar Scripts de Completamento

```bash
# Saída para stdout
foodtruck-cli completions generate bash

# Salvar em arquivo
foodtruck-cli completions generate zsh --output foodtruck-cli.zsh
```

#### Verificar Status de Completamento

```bash
foodtruck-cli completions status
```

**Exemplo de Saída:**
```
📊 Status de Completamentos
Informações do Shell:
ℹ Shell atual: zsh
ℹ Suporte a completamento: True

Status de Instalação:
✅ zsh: Instalado em /home/user/.zsh/completion/_foodtruck-cli
⚠️ bash: Não instalado
⚠️ fish: Não instalado

Teste:
💡 Testar completamentos: foodtruck-cli <TAB><TAB>
```

#### Desinstalar Completions

```bash
# Remover do shell atual
foodtruck-cli completions uninstall

# Remover de todos os shells
foodtruck-cli completions uninstall all
```

### ℹ️ Comando Version

```bash
foodtruck-cli version
```

**Saída:**
```
🚚 Sistema de Gerenciamento de Food Truck
Versão: 1.0.0
Framework CLI Python: Cyclopts
Banco de Dados: PostgreSQL com SQLModel
Framework Web: FastAPI
```

## 🏗️ Arquitetura

O CLI é construído usando princípios de **Arquitetura Limpa** com separação clara de responsabilidades:

### 📁 Estrutura de Diretórios

```
projeto_aplicado/cli/
├── 📱 app.py                   # Fábrica da aplicação CLI principal
├── 🏛️ base/                    # Classes base abstratas (SOLID)
│   ├── command.py             # BaseCommand (SRP + OCP)
│   └── service.py             # BaseService (SRP + ISP)
├── 🎮 commands/                # Comandos CLI (SRP)
│   ├── admin.py               # Gerenciamento de usuários admin
│   ├── completions.py         # Gerenciamento de completamento de shell
│   ├── database.py            # Comandos de banco de dados e migração
│   ├── health.py              # Verificações de saúde do sistema
│   └── setup.py               # Configuração e setup de shell
├── ⚙️ services/                # Serviços de lógica de negócio (SRP + DIP)
│   ├── completions.py         # Geração de scripts de completamento
│   ├── database.py            # Operações de banco de dados
│   ├── health.py              # Lógica de verificação de saúde
│   ├── migration.py           # Gerenciamento de migrações
│   ├── shell.py               # Configuração de shell
│   └── user.py                # Operações de usuário
└── 🧪 tests/                   # Suite abrangente de testes
    ├── test_app.py            # Testes de integração
    ├── test_commands.py       # Testes unitários de comandos
    ├── test_services.py       # Testes unitários de serviços
    └── test_integration.py    # Testes end-to-end
```

### 🎯 Implementação dos Princípios SOLID

- **🔧 Responsabilidade Única**: Cada comando e serviço tem um propósito claro
- **📖 Aberto/Fechado**: Fácil de estender com novos comandos sem modificar código existente
- **🔄 Substituição de Liskov**: Todos os comandos e serviços seguem interfaces consistentes
- **⚙️ Segregação de Interface**: Interfaces focadas e mínimas para comandos e serviços
- **🔀 Inversão de Dependência**: Comandos dependem de abstrações de serviço, não implementações

### 🧪 Estratégia de Testes

- **Testes Unitários**: 100% de cobertura para todos os serviços e comandos
- **Testes de Integração**: Execução end-to-end de comandos
- **Mocking**: Isolamento adequado de dependências externas
- **Cenários de Erro**: Cobertura abrangente de tratamento de erros

## 💡 Exemplos

### Fluxo de Configuração Completo

```bash
# 1. Primeira execução (auto-configura aliases)
uv run python -m projeto_aplicado.cli.app

# 2. Recarregar shell
source ~/.zshrc  # ou ~/.bashrc

# 3. Verificar saúde do sistema (usando aliases)
ft-health

# 4. Inicializar banco de dados
ft-db init

# 5. Criar usuário admin
ft-admin create admin admin@foodtruck.com admin123 "Administrador do Sistema"

# 6. Verificar criação do admin
ft-admin check admin@foodtruck.com

# 7. Instalar completamentos de shell (opcional)
ft-completions install
```

### Fluxo de Migração de Banco de Dados

```bash
# Verificar status atual
foodtruck-cli database status

# Criar nova migração
foodtruck-cli database create "adicionar campos de perfil de usuário"

# Revisar histórico de migrações
foodtruck-cli database history

# Aplicar migrações
foodtruck-cli database upgrade

# Verificar estado atual
foodtruck-cli database current
```

### Configuração de Ambiente de Desenvolvimento

```bash
# Instalar dependências do projeto
uv pip install -e .[dev]

# Configurar acesso ao shell
foodtruck-cli setup install

# Instalar completamentos
foodtruck-cli completions install

# Verificar se tudo funciona
foodtruck-cli health
```

### Implantação de Produção

```bash
# Verificar saúde com banco de dados de produção
foodtruck-cli health --db-host prod-db.empresa.com

# Inicializar banco de dados de produção
foodtruck-cli database init --db-host prod-db.empresa.com

# Criar admin de produção
foodtruck-cli admin create prod_admin admin@empresa.com senha_segura "Administrador de Produção"

# Verificar configuração
foodtruck-cli admin list-admins
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes CLI
uv run pytest projeto_aplicado/cli/tests/ -v

# Categorias específicas de teste
uv run pytest projeto_aplicado/cli/tests/test_commands.py -v
uv run pytest projeto_aplicado/cli/tests/test_services.py -v
uv run pytest projeto_aplicado/cli/tests/test_integration.py -v

# Com cobertura
uv run pytest projeto_aplicado/cli/tests/ --cov=projeto_aplicado.cli --cov-report=html
```

### Estrutura de Testes

- **71 testes CLI dedicados** com 100% de cobertura
- **Testes unitários** para componentes individuais
- **Testes de integração** para fluxos completos
- **Estratégias de mock** para dependências externas

## 📚 Solução de Problemas

### Problemas Comuns

#### Comando Não Encontrado

```bash
# Problema: foodtruck-cli: comando não encontrado
# Solução: Ativar ambiente virtual
source .venv/bin/activate

# Ou configurar acesso permanente
foodtruck-cli setup install
```

#### Problemas de Conexão com Banco de Dados

```bash
# Problema: Falha na conexão com banco de dados
# Verificar: PostgreSQL está rodando?
sudo systemctl status postgresql

# Verificar: Credenciais estão corretas?
foodtruck-cli health --db-host localhost

# Verificar: Variáveis de ambiente
echo $POSTGRES_HOSTNAME
echo $POSTGRES_DB
```

#### Problemas de Migração

```bash
# Problema: Conflitos de migração
# Solução: Verificar estado atual
foodtruck-cli database status
foodtruck-cli database history

# Resetar se necessário (⚠️ destrutivo)
foodtruck-cli database reset --confirm
foodtruck-cli database init
```

#### Problemas de Permissão

```bash
# Problema: Permissão negada ao instalar completamentos
# Solução: Verificar permissões de diretório
ls -la ~/.zsh/completion/
chmod 755 ~/.zsh/completion/

# Ou tentar instalação específica do usuário
foodtruck-cli completions install --shell zsh
```

### Modo Debug

Para informações detalhadas de erro, use o modo verbose do Python:

```bash
uv run python -v -m projeto_aplicado.cli.app <comando>
```

### Obtendo Ajuda

- **Ajuda do comando**: `foodtruck-cli <comando> --help`
- **Ajuda geral**: `foodtruck-cli --help`
- **Informações de versão**: `foodtruck-cli version`
- **Verificação de saúde**: `foodtruck-cli health`

### Variáveis de Ambiente

O CLI respeita estas variáveis de ambiente:

```bash
# Configuração do banco de dados
POSTGRES_HOSTNAME=localhost     # Host do banco de dados
POSTGRES_DB=foodtruck          # Nome do banco de dados
POSTGRES_USER=postgres         # Usuário do banco de dados
POSTGRES_PASSWORD=password     # Senha do banco de dados

# Configurações da aplicação
SECRET_KEY=sua-chave-secreta   # Chave secreta JWT
```

---

## 🤝 Contribuindo

O CLI segue princípios arquiteturais rigorosos. Ao contribuir:

1. **Siga a Arquitetura Limpa** - Mantenha comandos finos, coloque lógica em serviços
2. **Escreva Testes** - Todos os novos recursos devem ter 100% de cobertura de testes
3. **Use Type Hints** - Anotação completa de tipos é obrigatória
4. **Siga SOLID** - Cada classe deve ter uma única responsabilidade
5. **Saída Rica** - Use o console Rich para saída bonita e informativa

### Adicionando Novos Comandos

1. Criar classe de comando em `commands/`
2. Criar serviço correspondente em `services/`
3. Registrar em `app.py`
4. Adicionar testes abrangentes
5. Atualizar esta documentação

---

<div align="center">

**Construído com ❤️ usando Arquitetura Limpa e princípios SOLID**

[🐛 Reportar Bug](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues) • 
[💡 Solicitar Recurso](https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues) • 
[📖 Documentação Principal](../README.md)

</div>
