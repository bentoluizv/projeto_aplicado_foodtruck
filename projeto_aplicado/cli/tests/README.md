# CLI Tests Documentation

## 📁 Test Structure

This directory contains comprehensive tests for the CLI clean architecture following SOLID principles.

```
projeto_aplicado/cli/tests/
├── __init__.py          # Package initialization
├── conftest.py          # Pytest configuration and fixtures
├── test_services.py     # Unit tests for services (DatabaseService, UserService, HealthService)
├── test_commands.py     # Unit tests for commands (HealthCommand, CreateAdminCommand, etc.)
├── test_app.py          # Integration tests for CLI app creation and configuration
├── test_integration.py  # End-to-end workflow and integration tests
└── README.md           # This documentation
```

## 🧪 Test Categories

### 1. Service Tests (`test_services.py`)
- **DatabaseService**: Connection management, environment handling, session context
- **UserService**: User operations, validation, CRUD operations
- **HealthService**: Health checks, dependency coordination

### 2. Command Tests (`test_commands.py`)
- **HealthCommand**: Health check execution, output formatting
- **CreateAdminCommand**: User creation, validation, confirmation
- **CheckUserCommand**: User lookup, error handling
- **ListAdminsCommand**: Admin listing, empty results
- **BaseCommand**: Common functionality (print methods, headers)

### 3. App Tests (`test_app.py`)
- **App Creation**: CLI app factory function
- **Configuration**: Environment setup, command registration
- **Integration**: Command instantiation, dependency injection

### 4. Integration Tests (`test_integration.py`)
- **Complete Workflows**: End-to-end user scenarios
- **Service Integration**: Multi-service interactions
- **Error Handling**: Exception propagation and handling
- **Dependency Injection**: Proper dependency management

## 🏗️ Test Architecture Principles

### SOLID Principles in Tests
- **Single Responsibility**: Each test class focuses on one component
- **Open/Closed**: Tests can be extended without modification
- **Liskov Substitution**: Mock objects properly substitute real ones
- **Interface Segregation**: Tests focus on specific interfaces
- **Dependency Inversion**: Tests use mocks and dependency injection

### Clean Architecture
- **Unit Tests**: Test individual services and commands in isolation
- **Integration Tests**: Test service interactions and workflows
- **Mocking Strategy**: Mock external dependencies (database, filesystem)
- **Test Isolation**: Each test is independent and can run in any order

## 🚀 Running Tests

### All CLI Tests
```bash
# Run all CLI tests
uv run pytest projeto_aplicado/cli/tests/

# Run with coverage
uv run pytest projeto_aplicado/cli/tests/ --cov=projeto_aplicado.cli

# Run with verbose output
uv run pytest projeto_aplicado/cli/tests/ -v
```

### Specific Test Categories
```bash
# Service tests only
uv run pytest projeto_aplicado/cli/tests/test_services.py

# Command tests only
uv run pytest projeto_aplicado/cli/tests/test_commands.py

# Integration tests only
uv run pytest projeto_aplicado/cli/tests/test_integration.py

# App tests only
uv run pytest projeto_aplicado/cli/tests/test_app.py
```

### Specific Test Classes
```bash
# Database service tests
uv run pytest projeto_aplicado/cli/tests/test_services.py::TestDatabaseService

# Health command tests
uv run pytest projeto_aplicado/cli/tests/test_commands.py::TestHealthCommand

# Complete workflow tests
uv run pytest projeto_aplicado/cli/tests/test_integration.py::TestCLIWorkflow
```

## 🎯 Test Coverage Goals

### Services (90%+ Coverage)
- ✅ **DatabaseService**: Connection management, session handling, environment setup
- ✅ **UserService**: CRUD operations, validation, error handling
- ✅ **HealthService**: Health checks, dependency coordination, error handling

### Commands (85%+ Coverage)
- ✅ **HealthCommand**: Execution, output formatting, error handling
- ✅ **CreateAdminCommand**: User creation, validation, confirmation prompts
- ✅ **CheckUserCommand**: User lookup, not found scenarios
- ✅ **ListAdminsCommand**: Admin listing, empty results

### Integration (80%+ Coverage)
- ✅ **End-to-End Workflows**: Complete user scenarios
- ✅ **Service Integration**: Multi-service coordination
- ✅ **Error Handling**: Exception propagation and recovery
- ✅ **Dependency Injection**: Proper dependency management

## 🔧 Test Fixtures

### Database Fixtures
- `postgres_container`: PostgreSQL test container (session scope)
- `test_engine`: SQLModel engine for tests (session scope)
- `session`: Database session for each test (function scope)

### User Fixtures
- `sample_user`: Standard user for testing
- `sample_admin`: Admin user for testing

### Service Fixtures
- Services are created in tests using dependency injection
- Mocking is used to isolate components

## 📊 Test Patterns

### Mocking Strategy
```python
# Mock external dependencies
with patch.object(DatabaseService, 'test_connection', return_value=True):
    # Test code here
    pass

# Mock service interactions
with patch.object(user_service, 'execute_operation', return_value=mock_user):
    # Test code here
    pass
```

### Dependency Injection Testing
```python
# Test proper dependency injection
db_service = DatabaseService()
user_service = UserService(db_service)
assert user_service.database_service is db_service
```

### Error Handling Testing
```python
# Test exception handling
with patch.object(service, 'method', side_effect=Exception("Test error")):
    result = command.execute()
    assert result == 1  # Error exit code
```

## 🎨 Test Quality Guidelines

### Test Naming
- **Descriptive**: `test_create_admin_user_success`
- **Behavior-focused**: `test_validation_fails_with_empty_username`
- **Scenario-based**: `test_health_check_with_database_failure`

### Test Structure
```python
def test_specific_behavior(self):
    """Test description explaining what is being tested."""
    # Arrange: Set up test data and mocks
    service = ServiceClass()
    mock_dependency = Mock()
    
    # Act: Execute the behavior being tested
    result = service.method(test_data)
    
    # Assert: Verify the expected outcome
    assert result == expected_value
    mock_dependency.assert_called_once()
```

### Mock Guidelines
- **Minimal Mocking**: Only mock external dependencies
- **Realistic Mocks**: Mock behavior should match real implementations
- **Clear Assertions**: Verify both return values and interactions

## 🔍 Debugging Tests

### Common Issues
1. **Import Errors**: Check that CLI modules are properly imported
2. **Mock Setup**: Ensure mocks are configured before test execution
3. **Environment**: Verify environment variables don't interfere
4. **Database**: Check that test database is properly isolated

### Debug Commands
```bash
# Run single test with full output
uv run pytest projeto_aplicado/cli/tests/test_services.py::TestDatabaseService::test_initialization -v -s

# Run with pdb debugger
uv run pytest projeto_aplicado/cli/tests/test_services.py::TestDatabaseService::test_initialization --pdb

# Show test output
uv run pytest projeto_aplicado/cli/tests/ -s
```

---

**These tests ensure that the CLI clean architecture is reliable, maintainable, and follows industry best practices!** 🚚✨
