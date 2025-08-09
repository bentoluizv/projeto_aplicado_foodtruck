"""User service for CLI admin operations following SOLID principles."""

from typing import List, Optional

from sqlmodel import Session, select

from projeto_aplicado.cli.base.service import BaseService
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.user.schemas import CreateUserDTO


class UserService(BaseService):
    """User service that handles admin user operations.

    Follows Single Responsibility Principle: only handles user operations.
    Follows Dependency Inversion Principle: depends on DatabaseService abstraction.
    """

    def __init__(self, database_service: DatabaseService):
        """Initialize the user service.

        Args:
            database_service: Database service for operations
        """
        self.database_service = database_service

    def validate_input(self, **kwargs) -> bool:
        """Validate user input parameters.

        Args:
            **kwargs: User parameters to validate

        Returns:
            True if valid, False otherwise
        """
        username = kwargs.get('username', '')
        email = kwargs.get('email', '')
        password = kwargs.get('password', '')
        full_name = kwargs.get('full_name', '')

        # Validate username
        if not username or not username.strip():
            return False

        # Validate email
        if not email or not email.strip() or '@' not in email:
            return False

        # Validate password
        if not password or len(password) < 6:
            return False

        # Validate full name
        if not full_name or not full_name.strip():
            return False

        return True

    def execute_operation(self, operation: str, **kwargs):
        """Execute user operation.

        Args:
            operation: Operation to perform ('create', 'check', 'list')
            **kwargs: Operation parameters

        Returns:
            Operation result
        """
        operation_map = {
            'create': self._create_admin_user,
            'check': self._check_user,
            'list': self._list_admin_users,
            'count': self._count_admin_users,
        }

        if operation not in operation_map:
            raise ValueError(f'Unknown operation: {operation}')

        return self.database_service.execute_operation(
            operation_map[operation], **kwargs
        )

    def _create_admin_user(self, session: Session, **kwargs) -> Optional[User]:
        """Create an admin user.

        Args:
            session: Database session
            **kwargs: User creation parameters

        Returns:
            Created user or None if already exists
        """
        # Check if user already exists
        existing_user = session.exec(
            select(User).where(User.email == kwargs['email'])
        ).first()

        if existing_user:
            return None

        # Create the user DTO
        dto = CreateUserDTO(
            username=kwargs['username'],
            email=kwargs['email'],
            password=kwargs['password'],
            full_name=kwargs['full_name'],
            role=UserRole.ADMIN,
        )

        # Create the user - the DTO automatically hashes the password
        user = User(
            username=dto.username,
            email=dto.email,
            password=dto.password,  # Already hashed by DTO
            full_name=dto.full_name,
            role=dto.role,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    def _check_user(self, session: Session, **kwargs) -> Optional[User]:
        """Check if a user exists by email.

        Args:
            session: Database session
            **kwargs: Parameters containing 'email'

        Returns:
            User if found, None otherwise
        """
        email = kwargs['email']
        return session.exec(select(User).where(User.email == email)).first()

    def _list_admin_users(self, session: Session, **kwargs) -> List[User]:
        """List all admin users.

        Args:
            session: Database session
            **kwargs: Additional parameters (unused)

        Returns:
            List of admin users
        """
        return session.exec(
            select(User).where(User.role == UserRole.ADMIN)
        ).all()

    def _count_admin_users(self, session: Session, **kwargs) -> int:
        """Count admin users.

        Args:
            session: Database session
            **kwargs: Additional parameters (unused)

        Returns:
            Number of admin users
        """
        return len(self._list_admin_users(session, **kwargs))
