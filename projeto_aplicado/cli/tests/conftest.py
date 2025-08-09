"""Pytest configuration for CLI tests."""

import pytest
from sqlmodel import Session, SQLModel, create_engine
from testcontainers.postgres import PostgresContainer

from projeto_aplicado.resources.user.model import User


@pytest.fixture(scope="session")
def postgres_container():
    """Create a PostgreSQL test container for the session."""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def test_engine(postgres_container):
    """Create a test database engine."""
    connection_url = postgres_container.get_connection_url()
    engine = create_engine(connection_url, echo=False)

    # Create all tables
    SQLModel.metadata.create_all(engine)

    yield engine

    # Cleanup
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session
        # Rollback any changes after each test
        session.rollback()


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return User(
        username="testuser",
        email="test@example.com",
        password="hashed_password",
        full_name="Test User",
        role="user"
    )


@pytest.fixture
def sample_admin():
    """Create a sample admin user for testing."""
    return User(
        username="testadmin",
        email="admin@example.com",
        password="hashed_password",
        full_name="Test Admin",
        role="admin"
    )
