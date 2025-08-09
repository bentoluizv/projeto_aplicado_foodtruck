# 🚚 Food Truck CLI - Quick Reference

> **Quick command reference for the Food Truck Management System CLI**

## 📋 Command Overview

| Command | Description | Example |
|---------|-------------|---------|
| `health` | System health check | `foodtruck-cli health` |
| `admin` | User management | `foodtruck-cli admin create <user> <email> <pass> <name>` |
| `database` | Database operations | `foodtruck-cli database init` |
| `setup` | Shell configuration | `foodtruck-cli setup install` |
| `completions` | Tab completions | `foodtruck-cli completions install` |
| `version` | Show version info | `foodtruck-cli version` |

## 🚀 Quick Start

```bash
# 1. Check system health
foodtruck-cli health

# 2. Initialize database
foodtruck-cli database init

# 3. Create admin user
foodtruck-cli admin create admin admin@foodtruck.com admin123 "System Administrator"

# 4. Setup shell access
foodtruck-cli setup install

# 5. Install completions
foodtruck-cli completions install
```

## 🏥 Health Commands

```bash
# Basic health check
foodtruck-cli health

# Custom database host
foodtruck-cli health --db-host myserver.com
```

## 👥 Admin Commands

```bash
# Create admin user
foodtruck-cli admin create <username> <email> <password> <full_name>

# Check if admin exists
foodtruck-cli admin check <email>

# List all admins
foodtruck-cli admin list-admins

# Force create (overwrite)
foodtruck-cli admin create admin admin@test.com pass123 "Admin" --force
```

## 💾 Database Commands

```bash
# Initialize database
foodtruck-cli database init

# Check database status
foodtruck-cli database status

# Migration management
foodtruck-cli database upgrade           # Upgrade to latest
foodtruck-cli database upgrade abc123    # Upgrade to specific revision
foodtruck-cli database downgrade -1      # Downgrade one revision
foodtruck-cli database current           # Show current revision
foodtruck-cli database history           # Show migration history

# Create new migration
foodtruck-cli database create "description"

# Reset database (⚠️ destructive)
foodtruck-cli database reset --confirm
```

## ⚙️ Setup Commands

```bash
# Show PATH configuration
foodtruck-cli setup path

# Generate shell aliases
foodtruck-cli setup alias [bash|zsh|fish]

# Auto-configure shell
foodtruck-cli setup install [--shell bash|zsh|fish] [--force]

# Check current setup
foodtruck-cli setup check
```

## 🔧 Completion Commands

```bash
# Install completions for current shell
foodtruck-cli completions install

# Install for specific shell
foodtruck-cli completions install bash
foodtruck-cli completions install zsh
foodtruck-cli completions install fish

# Generate completion script
foodtruck-cli completions generate bash --output script.bash

# Check completion status
foodtruck-cli completions status

# Remove completions
foodtruck-cli completions uninstall [bash|zsh|fish|all]
```

## 🎯 Common Workflows

### First-Time Setup
```bash
foodtruck-cli health
foodtruck-cli database init
foodtruck-cli admin create admin admin@foodtruck.com admin123 "Admin"
foodtruck-cli setup install
foodtruck-cli completions install
```

### Database Migration
```bash
foodtruck-cli database status
foodtruck-cli database create "new migration"
foodtruck-cli database upgrade
foodtruck-cli database current
```

### Development Environment
```bash
uv pip install -e .[dev]
foodtruck-cli health
foodtruck-cli setup install
foodtruck-cli completions install
```

## 🐚 Shell Integration

### Generated Aliases
After `foodtruck-cli setup install`:
- `ftcli` → `foodtruck-cli`
- `ft-health` → `foodtruck-cli health`
- `ft-admin` → `foodtruck-cli admin`
- `ft-db` → `foodtruck-cli database`

### Tab Completion
After `foodtruck-cli completions install`:
```bash
foodtruck-cli <TAB><TAB>    # Shows all commands
foodtruck-cli admin <TAB>   # Shows admin subcommands
foodtruck-cli setup install --shell <TAB>  # Shows shell options
```

## 🔍 Troubleshooting

### Command Not Found
```bash
# Activate virtual environment
source .venv/bin/activate

# Or setup permanent access
foodtruck-cli setup install
```

### Database Issues
```bash
# Check connection
foodtruck-cli health

# Check PostgreSQL status
sudo systemctl status postgresql

# Verify environment variables
echo $POSTGRES_HOSTNAME $POSTGRES_DB
```

### Permission Issues
```bash
# Check completion directory
ls -la ~/.zsh/completion/

# Fix permissions
chmod 755 ~/.zsh/completion/
```

## 📖 Help Commands

```bash
# General help
foodtruck-cli --help

# Command-specific help
foodtruck-cli <command> --help

# Subcommand help
foodtruck-cli <command> <subcommand> --help
```

## 🌍 Environment Variables

```bash
# Database configuration
export POSTGRES_HOSTNAME=localhost
export POSTGRES_DB=foodtruck
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=password

# Application settings
export SECRET_KEY=your-secret-key
```

---

📖 **[Full Documentation](CLI.md)** | 🚚 **[Main Project](../README.md)**
