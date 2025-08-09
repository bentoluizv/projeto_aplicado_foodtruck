# 🛠️ CLI Development Guide

> **Developer documentation for extending and maintaining the Food Truck CLI**

## 📋 Table of Contents

- [🏗️ Architecture Overview](#️-architecture-overview)
- [🧩 Component Structure](#-component-structure)
- [🔧 Adding New Commands](#-adding-new-commands)
- [⚡ Services and Business Logic](#-services-and-business-logic)
- [🧪 Testing Strategy](#-testing-strategy)
- [📦 Dependency Management](#-dependency-management)
- [🎨 Coding Standards](#-coding-standards)
- [🔍 Debugging and Profiling](#-debugging-and-profiling)

## 🏗️ Architecture Overview

The CLI follows **Clean Architecture** with strict dependency direction and SOLID principles:

```
┌─────────────────────────────────────────┐
│                 UI Layer                │
│            (Commands)                   │
├─────────────────────────────────────────┤
│              Application                │
│              (Services)                 │
├─────────────────────────────────────────┤
│               Domain                    │
│           (Base Classes)                │
├─────────────────────────────────────────┤
│            Infrastructure               │
│        (Database, External)             │
└─────────────────────────────────────────┘
```

### Key Principles

1. **Dependency Inversion**: Commands depend on service abstractions
2. **Single Responsibility**: Each class has one reason to change
3. **Open/Closed**: Easy to extend without modifying existing code
4. **Interface Segregation**: Focused, minimal interfaces
5. **Liskov Substitution**: Consistent behavior across implementations

## 🧩 Component Structure

### Directory Layout

```
projeto_aplicado/cli/
├── app.py                 # Main application factory
├── base/                  # Abstract base classes
│   ├── command.py        # BaseCommand interface
│   └── service.py        # BaseService interface
├── commands/             # Command implementations
│   ├── admin.py         # Admin user management
│   ├── completions.py   # Shell completion management
│   ├── database.py      # Database operations
│   ├── health.py        # System health checks
│   └── setup.py         # Shell configuration
├── services/            # Business logic services
│   ├── completions.py   # Completion script generation
│   ├── database.py      # Database connectivity
│   ├── health.py        # Health check logic
│   ├── migration.py     # Migration management
│   ├── shell.py         # Shell configuration
│   └── user.py          # User operations
└── tests/               # Comprehensive test suite
    ├── test_app.py      # Application tests
    ├── test_commands.py # Command unit tests
    ├── test_services.py # Service unit tests
    └── test_integration.py # End-to-end tests
```

### Base Classes

#### BaseCommand

All commands inherit from `BaseCommand`:

```python
from abc import ABC, abstractmethod
from typing import Optional
from rich.console import Console

class BaseCommand(ABC):
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> int:
        """Execute command and return exit code."""
        pass
    
    def print_success(self, message: str) -> None:
        """Print success message with green checkmark."""
        
    def print_error(self, message: str) -> None:
        """Print error message with red X."""
        
    def print_warning(self, message: str) -> None:
        """Print warning message with yellow warning."""
        
    def print_info(self, message: str) -> None:
        """Print info message with blue info icon."""
```

#### BaseService

All services inherit from `BaseService`:

```python
from abc import ABC, abstractmethod
from typing import Any

class BaseService(ABC):
    @abstractmethod
    def validate_input(self, **kwargs) -> bool:
        """Validate service inputs."""
        pass
    
    @abstractmethod
    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute service operation."""
        pass
```

## 🔧 Adding New Commands

### Step 1: Create Command Class

Create `commands/mycommand.py`:

```python
"""My new command implementation."""

from typing import Optional
import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.myservice import MyService

class MyCommand(BaseCommand):
    """My command description."""
    
    def __init__(self, console: Optional[Console] = None):
        super().__init__(console)
        self.my_service = MyService()
    
    def execute(self, param: str = "default") -> int:
        """Execute my command.
        
        Args:
            param: Parameter description
            
        Returns:
            int: Exit code (0 for success)
        """
        self.print_header('My Command', '🎯')
        
        try:
            result = self.my_service.execute_operation('my_operation', param=param)
            
            if result['success']:
                self.print_success('✅ Operation completed successfully!')
                return 0
            else:
                self.print_error('❌ Operation failed')
                return 1
                
        except Exception as e:
            self.print_error(f'Failed to execute command: {str(e)}')
            return 1

# Create the cyclopts app
my_app = cyclopts.App(
    name='mycommand',
    help='My command description',
)

@my_app.default
def my_default(param: str = "default") -> int:
    """My command with parameter."""
    command = MyCommand()
    return command.execute(param)
```

### Step 2: Create Service

Create `services/myservice.py`:

```python
"""My service implementation."""

from typing import Any, Dict
from projeto_aplicado.cli.base.service import BaseService

class MyService(BaseService):
    """Service for my business logic."""
    
    def __init__(self):
        super().__init__()
    
    def validate_input(self, **kwargs) -> bool:
        """Validate inputs."""
        param = kwargs.get('param')
        return param is not None and len(param) > 0
    
    def execute_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation."""
        if not self.validate_input(**kwargs):
            return {'success': False, 'error': 'Invalid input'}
        
        if operation == 'my_operation':
            return self._my_operation(**kwargs)
        else:
            raise ValueError(f'Unknown operation: {operation}')
    
    def _my_operation(self, **kwargs) -> Dict[str, Any]:
        """My business logic implementation."""
        param = kwargs.get('param')
        
        # Business logic here
        result = f"Processed: {param}"
        
        return {
            'success': True,
            'result': result,
            'message': 'Operation completed',
        }
```

### Step 3: Register Command

Update `app.py`:

```python
from projeto_aplicado.cli.commands.mycommand import my_app

def create_cli_app() -> App:
    # ... existing code ...
    
    # Register new command
    app.command(my_app, name='mycommand')
    
    # Update help text
    app.console.print(
        '  • [cyan]mycommand[/cyan] - My command description'
    )
```

### Step 4: Add Tests

Create `tests/test_mycommand.py`:

```python
"""Tests for my command."""

import pytest
from unittest.mock import Mock, patch
from projeto_aplicado.cli.commands.mycommand import MyCommand
from projeto_aplicado.cli.services.myservice import MyService

class TestMyCommand:
    """Test cases for MyCommand."""
    
    def test_execute_success(self):
        """Test successful command execution."""
        command = MyCommand()
        
        with patch.object(command.my_service, 'execute_operation') as mock_service:
            mock_service.return_value = {'success': True}
            
            result = command.execute("test")
            
            assert result == 0
            mock_service.assert_called_once_with('my_operation', param="test")
    
    def test_execute_failure(self):
        """Test command execution failure."""
        command = MyCommand()
        
        with patch.object(command.my_service, 'execute_operation') as mock_service:
            mock_service.return_value = {'success': False}
            
            result = command.execute("test")
            
            assert result == 1

class TestMyService:
    """Test cases for MyService."""
    
    def test_validate_input_valid(self):
        """Test input validation with valid data."""
        service = MyService()
        
        result = service.validate_input(param="valid")
        
        assert result is True
    
    def test_validate_input_invalid(self):
        """Test input validation with invalid data."""
        service = MyService()
        
        result = service.validate_input(param="")
        
        assert result is False
    
    def test_my_operation(self):
        """Test my operation logic."""
        service = MyService()
        
        result = service.execute_operation('my_operation', param="test")
        
        assert result['success'] is True
        assert result['result'] == "Processed: test"
```

## ⚡ Services and Business Logic

### Service Patterns

#### 1. Operation Pattern

Services use an operation pattern for extensibility:

```python
def execute_operation(self, operation: str, **kwargs) -> Any:
    operations = {
        'create': self._create_operation,
        'read': self._read_operation,
        'update': self._update_operation,
        'delete': self._delete_operation,
    }
    
    if operation not in operations:
        raise ValueError(f'Unknown operation: {operation}')
        
    return operations[operation](**kwargs)
```

#### 2. Validation Pattern

Always validate inputs before processing:

```python
def validate_input(self, **kwargs) -> bool:
    required_fields = ['field1', 'field2']
    
    for field in required_fields:
        if field not in kwargs or not kwargs[field]:
            return False
    
    # Additional validation logic
    return True
```

#### 3. Error Handling Pattern

Return structured error information:

```python
def _some_operation(self, **kwargs) -> Dict[str, Any]:
    try:
        # Operation logic
        result = perform_operation()
        
        return {
            'success': True,
            'data': result,
            'message': 'Operation completed successfully',
        }
    except SpecificException as e:
        return {
            'success': False,
            'error': str(e),
            'error_type': 'SpecificException',
        }
```

### Database Services

For database operations, use the established patterns:

```python
from projeto_aplicado.ext.database.db import get_session
from sqlmodel import select

class DatabaseService(BaseService):
    def _get_database_session(self):
        """Get database session with proper error handling."""
        try:
            return next(get_session())
        except Exception as e:
            raise ConnectionError(f"Database connection failed: {str(e)}")
    
    def _execute_query(self, query, **kwargs):
        """Execute database query with session management."""
        session = self._get_database_session()
        try:
            result = session.exec(query).all()
            return result
        finally:
            session.close()
```

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_app.py              # Application integration tests
├── test_commands.py         # Command unit tests
├── test_services.py         # Service unit tests
└── test_integration.py      # End-to-end tests
```

### Testing Patterns

#### 1. Command Testing

```python
import pytest
from unittest.mock import Mock, patch
from rich.console import Console

class TestMyCommand:
    @pytest.fixture
    def mock_console(self):
        return Mock(spec=Console)
    
    @pytest.fixture
    def command(self, mock_console):
        return MyCommand(console=mock_console)
    
    def test_execute_with_mocked_service(self, command):
        with patch.object(command, 'my_service') as mock_service:
            mock_service.execute_operation.return_value = {'success': True}
            
            result = command.execute()
            
            assert result == 0
            mock_service.execute_operation.assert_called_once()
```

#### 2. Service Testing

```python
class TestMyService:
    @pytest.fixture
    def service(self):
        return MyService()
    
    def test_operation_success(self, service):
        result = service.execute_operation('my_operation', param="test")
        
        assert result['success'] is True
        assert 'data' in result
    
    def test_operation_validation_failure(self, service):
        result = service.execute_operation('my_operation', param="")
        
        assert result['success'] is False
        assert 'error' in result
```

#### 3. Integration Testing

```python
def test_full_command_workflow():
    """Test complete command execution."""
    # Setup test database
    # Execute command
    # Verify results
    # Cleanup
```

### Test Fixtures

Common fixtures in `conftest.py`:

```python
import pytest
from unittest.mock import Mock
import tempfile
import os

@pytest.fixture
def mock_database():
    """Mock database session."""
    with patch('projeto_aplicado.ext.database.db.get_session') as mock:
        yield mock

@pytest.fixture
def temp_directory():
    """Temporary directory for file operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def mock_environment():
    """Mock environment variables."""
    original_env = os.environ.copy()
    test_env = {
        'POSTGRES_HOSTNAME': 'test_host',
        'POSTGRES_DB': 'test_db',
    }
    os.environ.update(test_env)
    yield
    os.environ.clear()
    os.environ.update(original_env)
```

## 📦 Dependency Management

### Adding Dependencies

1. **Runtime dependencies**: Add to `pyproject.toml` dependencies
2. **Development dependencies**: Add to dev dependency group
3. **Optional dependencies**: Create optional dependency groups

Example:

```toml
[project]
dependencies = [
    "cyclopts>=3.22.5",
    "rich>=13.0.0",
    "sqlmodel>=0.0.24",
]

[dependency-groups]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
]
completions = [
    "argcomplete>=3.0.0",
]
```

### Dependency Injection

Use constructor injection for all dependencies:

```python
class MyCommand(BaseCommand):
    def __init__(self, console: Optional[Console] = None, my_service: Optional[MyService] = None):
        super().__init__(console)
        self.my_service = my_service or MyService()
```

This enables easy testing with mocked dependencies.

## 🎨 Coding Standards

### Code Style

- **PEP 8**: Python style guide compliance
- **Type hints**: Full type annotation required
- **Docstrings**: Google style for all public methods
- **Line length**: Maximum 79 characters
- **Import organization**: Standard library, third-party, local

### Example Formatting

```python
"""Module docstring describing the purpose."""

import os
import sys
from typing import Any, Dict, List, Optional

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand


class WellFormattedCommand(BaseCommand):
    """Command with proper formatting and documentation.
    
    This class demonstrates proper code formatting and documentation
    standards for the CLI project.
    
    Attributes:
        service: The business logic service for this command.
    """
    
    def __init__(self, console: Optional[Console] = None) -> None:
        """Initialize command with dependency injection.
        
        Args:
            console: Rich console for output formatting.
        """
        super().__init__(console)
        self.service = SomeService()
    
    def execute(self, param: str, flag: bool = False) -> int:
        """Execute the command with proper error handling.
        
        Args:
            param: Required parameter for the operation.
            flag: Optional flag to modify behavior.
            
        Returns:
            Exit code: 0 for success, 1 for failure.
            
        Raises:
            ValueError: If param is invalid.
        """
        if not param:
            raise ValueError("Parameter cannot be empty")
        
        try:
            result = self.service.execute_operation(
                'operation_name',
                param=param,
                flag=flag
            )
            
            if result['success']:
                self.print_success('✅ Operation completed')
                return 0
            else:
                self.print_error(f'❌ Operation failed: {result["error"]}')
                return 1
                
        except Exception as e:
            self.print_error(f'Unexpected error: {str(e)}')
            return 1
```

### Quality Tools

Use these tools for code quality:

```bash
# Linting
ruff check .
ruff check . --diff

# Formatting  
ruff format .

# Type checking
mypy projeto_aplicado/cli/

# Testing
pytest projeto_aplicado/cli/tests/ --cov=projeto_aplicado.cli
```

## 🔍 Debugging and Profiling

### Debug Mode

Enable verbose output for debugging:

```bash
# Python verbose mode
uv run python -v -m projeto_aplicado.cli.app command

# With debugger
uv run python -m pdb -m projeto_aplicado.cli.app command
```

### Logging

Add logging to services for debugging:

```python
import logging

logger = logging.getLogger(__name__)

class MyService(BaseService):
    def execute_operation(self, operation: str, **kwargs) -> Any:
        logger.debug(f"Executing operation: {operation} with args: {kwargs}")
        
        try:
            result = self._perform_operation(operation, **kwargs)
            logger.info(f"Operation {operation} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Operation {operation} failed: {str(e)}")
            raise
```

### Performance Profiling

Profile CLI performance:

```bash
# Time profiling
uv run python -m cProfile -s cumulative -m projeto_aplicado.cli.app command

# Memory profiling with memory_profiler
uv run python -m memory_profiler -m projeto_aplicado.cli.app command
```

### Test Coverage

Monitor test coverage:

```bash
# Generate coverage report
uv run pytest --cov=projeto_aplicado.cli --cov-report=html

# View in browser
open htmlcov/index.html
```

---

## 🤝 Contributing Guidelines

1. **Follow Clean Architecture** - Keep business logic in services
2. **Write Tests First** - TDD approach preferred
3. **Document Everything** - Clear docstrings and comments
4. **Type Everything** - Full type annotations required
5. **Test Everything** - 100% coverage goal
6. **Review Code** - Peer review before merging

### Pull Request Checklist

- [ ] Code follows style guidelines
- [ ] All tests pass with 100% coverage
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Error handling implemented
- [ ] Integration tests added
- [ ] Performance impact considered

---

**Built with ❤️ following Clean Architecture and SOLID principles**
