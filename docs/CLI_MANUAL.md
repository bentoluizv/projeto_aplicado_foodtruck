# FOODTRUCK-CLI(1) Manual Page

## NAME

**foodtruck-cli** - Food Truck Management System Command Line Interface

## SYNOPSIS

**foodtruck-cli** [*GLOBAL-OPTIONS*] *COMMAND* [*COMMAND-OPTIONS*] [*ARGS*]

## DESCRIPTION

The **foodtruck-cli** is a comprehensive command-line interface for the Food Truck Management System. It provides administrative tools for system health monitoring, user management, database operations, and shell configuration.

Built with Clean Architecture principles using Python and the Cyclopts framework, it offers a modern, type-safe, and well-tested CLI experience.

## GLOBAL OPTIONS

**--help**, **-h**
: Display help information and exit

**--version**
: Display version information and exit

## COMMANDS

### health [--db-host HOST]

Perform comprehensive system health checks including database connectivity, admin user presence, and configuration validation.

**Options:**
- **--db-host** *HOST* : Database hostname (default: localhost)

**Exit Status:**
- 0: All health checks passed
- 1: One or more health checks failed

**Example:**
```bash
foodtruck-cli health --db-host production.db.com
```

### admin SUBCOMMAND [OPTIONS]

Manage administrative users in the system.

**Subcommands:**

**create** *USERNAME* *EMAIL* *PASSWORD* *FULL_NAME* [**--force**]
: Create a new admin user with specified credentials

**check** *EMAIL*
: Verify if an admin user exists with the given email

**list-admins**
: Display all admin users in the system

**Options:**
- **--force** : Overwrite existing user if present
- **--db-host** *HOST* : Database hostname

**Examples:**
```bash
foodtruck-cli admin create admin admin@company.com secret123 "System Admin"
foodtruck-cli admin check admin@company.com
foodtruck-cli admin list-admins
```

### database SUBCOMMAND [OPTIONS]

Handle database schema management and migrations using Alembic.

**Subcommands:**

**init**
: Initialize database schema and run all migrations

**status**
: Show current database and migration status

**upgrade** [*REVISION*]
: Upgrade database to latest or specified revision

**downgrade** *REVISION*
: Downgrade database to specified revision

**current**
: Display current migration revision

**history**
: Show migration history

**create** *MESSAGE*
: Create new migration with descriptive message

**reset** **--confirm**
: Reset database (destructive operation)

**Options:**
- **--db-host** *HOST* : Database hostname
- **--confirm** : Required for destructive operations

**Examples:**
```bash
foodtruck-cli database init
foodtruck-cli database upgrade
foodtruck-cli database create "add user profile table"
foodtruck-cli database reset --confirm
```

### setup SUBCOMMAND [OPTIONS]

Configure shell environment for optimal CLI usage.

**Subcommands:**

**path**
: Display PATH configuration and manual setup instructions

**alias** [*SHELL*]
: Generate shell aliases for convenience commands

**install** [**--shell** *SHELL*] [**--force**]
: Auto-configure shell with PATH and aliases

**check**
: Verify current shell configuration status

**Options:**
- **--shell** *SHELL* : Target shell (bash|zsh|fish|auto)
- **--force** : Overwrite existing configuration

**Examples:**
```bash
foodtruck-cli setup install --shell zsh
foodtruck-cli setup alias bash
foodtruck-cli setup check
```

### completions SUBCOMMAND [OPTIONS]

Manage shell tab completion scripts for enhanced usability.

**Subcommands:**

**generate** *SHELL* [**--output** *FILE*]
: Generate completion script for specified shell

**install** [**--shell** *SHELL*] [**--force**]
: Install completion script to appropriate location

**status**
: Check completion installation status across shells

**uninstall** [*SHELL*]
: Remove completion scripts

**Options:**
- **--shell** *SHELL* : Target shell (bash|zsh|fish|auto)
- **--output** *FILE* : Output file path (default: stdout)
- **--force** : Overwrite existing installations

**Examples:**
```bash
foodtruck-cli completions install
foodtruck-cli completions generate zsh --output foodtruck.zsh
foodtruck-cli completions status
```

### version

Display comprehensive version and system information.

**Output includes:**
- Application version
- CLI framework information
- Database system details
- Web framework version

## EXIT STATUS

**0**
: Successful operation

**1**
: Operation failed or validation error

**2**
: Invalid command or arguments

## ENVIRONMENT VARIABLES

**POSTGRES_HOSTNAME**
: Database server hostname (default: localhost)

**POSTGRES_DB**
: Database name (default: foodtruck)

**POSTGRES_USER**
: Database username (default: postgres)

**POSTGRES_PASSWORD**
: Database password

**SECRET_KEY**
: Application secret key for JWT tokens

## FILES

**~/.zshrc**, **~/.bashrc**
: Shell configuration files modified by setup commands

**~/.zsh/completion/_foodtruck-cli**
: Zsh completion script location

**~/.bash_completion**
: Bash completion script location

**~/.config/fish/completions/foodtruck-cli.fish**
: Fish completion script location

**.venv/bin/foodtruck-cli**
: Main CLI executable in virtual environment

## EXAMPLES

### Initial System Setup
```bash
# Check system prerequisites
foodtruck-cli health

# Initialize database schema
foodtruck-cli database init

# Create administrative user
foodtruck-cli admin create admin admin@foodtruck.com secure123 "System Administrator"

# Configure shell for direct access
foodtruck-cli setup install

# Enable tab completions
foodtruck-cli completions install
```

### Database Migration Workflow
```bash
# Check current migration state
foodtruck-cli database status

# Create new migration
foodtruck-cli database create "add user preferences table"

# Apply pending migrations
foodtruck-cli database upgrade

# Verify final state
foodtruck-cli database current
```

### Development Environment Setup
```bash
# Install project in development mode
uv pip install -e .[dev]

# Configure development shell
foodtruck-cli setup install --force

# Install completions for productivity
foodtruck-cli completions install --shell zsh

# Verify everything works
foodtruck-cli health
```

### Production Deployment
```bash
# Health check with production database
foodtruck-cli health --db-host prod-db.company.com

# Initialize production schema
foodtruck-cli database init --db-host prod-db.company.com

# Create production admin
foodtruck-cli admin create prod_admin admin@company.com $(openssl rand -base64 32) "Production Admin"

# Verify deployment
foodtruck-cli admin list-admins --db-host prod-db.company.com
```

## DIAGNOSTICS

### Common Error Scenarios

**Database Connection Failed**
: Verify PostgreSQL service status and connection parameters

**Admin User Already Exists**
: Use `--force` flag or check existing users with `admin list-admins`

**Migration Conflict**
: Review migration history and resolve conflicts manually

**Permission Denied**
: Check file permissions for completion directories

**Command Not Found**
: Ensure virtual environment is activated or shell is properly configured

### Debug Information

For detailed error tracing, use Python's verbose mode:
```bash
uv run python -v -m projeto_aplicado.cli.app COMMAND
```

## ARCHITECTURE

The CLI follows Clean Architecture with SOLID principles:

- **Commands**: Thin presentation layer handling user interaction
- **Services**: Business logic layer with domain-specific operations  
- **Base Classes**: Abstract interfaces ensuring consistency
- **Dependency Injection**: Loose coupling through constructor injection

### Testing
- 71 dedicated test cases with 100% coverage
- Unit tests for isolated component verification
- Integration tests for end-to-end workflows
- Mock strategies for external dependency isolation

## STANDARDS COMPLIANCE

- **PEP 8**: Python coding style guidelines
- **PEP 484**: Type hints for static analysis
- **SOLID Principles**: Object-oriented design principles
- **Clean Architecture**: Dependency rule and separation of concerns

## SECURITY CONSIDERATIONS

- Passwords are hashed using Argon2ID algorithm
- Database connections use parameterized queries
- Input validation prevents injection attacks
- Sensitive operations require explicit confirmation

## BUGS

Report bugs at: https://github.com/bentoluizv/projeto_aplicado_foodtruck/issues

## AUTHORS

Developed by SENAI SC students as part of the Applied Project 2025.

## SEE ALSO

**alembic(1)**, **psql(1)**, **python(1)**

Project documentation: https://github.com/bentoluizv/projeto_aplicado_foodtruck

## COPYRIGHT

This software is released under the MIT License.

---

Food Truck CLI 1.0.0                    January 2025                    FOODTRUCK-CLI(1)
