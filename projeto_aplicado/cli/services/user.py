"""User service for CLI admin operations following SOLID principles."""

from typing import Dict, List, Optional

from pydantic import EmailStr, ValidationError

from projeto_aplicado.cli.ext.database import DatabaseService
from projeto_aplicado.cli.schemas import UserListResult, UserOperationResult
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.user.repository import UserRepository
from projeto_aplicado.resources.user.schemas import CreateUserDTO


class UserService:
    """User service that handles admin user operations.

    Follows Single Responsibility Principle: only handles user operations.
    Follows Dependency Inversion Principle: depends on repository abstraction.
    """

    def __init__(self, database_service: DatabaseService):
        """Initialize the user service.

        Args:
            database_service: Database service for operations
        """
        self.database_service = database_service
        self._repository: Optional[UserRepository] = None

    @property
    def repository(self) -> UserRepository:
        """Get or create the user repository instance."""
        if not self._repository:
            with self.database_service.get_session() as session:
                self._repository = UserRepository(session)
        return self._repository

    def create_admin(self, raw_data: Dict) -> UserOperationResult:
        """Create an admin user.

        Args:
            raw_data: Raw user data dictionary

        Returns:
            UserOperationResult with status and data
        """
        try:
            user = self._create_admin_user(raw_data)
            return UserOperationResult(success=True, data=user)
        except ValidationError as e:
            return UserOperationResult(
                success=False,
                error=f'Validation error: {str(e)}',
            )
        except Exception as e:
            return UserOperationResult(
                success=False,
                error=f'Operation failed: {str(e)}',
            )

    def check_user(self, raw_data: Dict) -> UserOperationResult:
        """Check if a user exists.

        Args:
            raw_data: Raw data containing email

        Returns:
            UserOperationResult with status and data
        """
        try:
            user = self._check_user(raw_data)
            return UserOperationResult(success=True, data=user)
        except ValidationError as e:
            return UserOperationResult(
                success=False,
                error=f'Validation error: {str(e)}',
            )
        except Exception as e:
            return UserOperationResult(
                success=False,
                error=f'Operation failed: {str(e)}',
            )

    def list_admins(self) -> UserListResult:
        """List all admin users.

        Returns:
            UserListResult with status and data
        """
        try:
            users = self._list_admin_users()
            return UserListResult(success=True, data=users)
        except Exception as e:
            return UserListResult(
                success=False,
                error=f'Operation failed: {str(e)}',
            )

    def _create_admin_user(self, raw_data: Dict) -> User:
        """Create an admin user.

        Args:
            raw_data: Raw user data dictionary

        Returns:
            Created user

        Raises:
            ValidationError: If data validation fails
            ValueError: If user already exists
        """
        # Validate and create DTO
        create_dto = CreateUserDTO(
            username=raw_data['username'],
            email=raw_data['email'],
            password=raw_data['password'],
            full_name=raw_data.get('full_name'),
            role=UserRole.ADMIN,
        )

        # Check if user already exists
        existing_user = self.repository.get_by_email(create_dto.email)
        if existing_user:
            raise ValueError(
                f'User with email {create_dto.email} already exists'
            )

        # Create the user - the DTO automatically hashes the password
        user = User(
            username=create_dto.username,
            email=create_dto.email,
            password=create_dto.password,  # Already hashed by DTO
            full_name=create_dto.full_name,
            role=UserRole.ADMIN,
        )

        return self.repository.create(user)

    def _check_user(self, raw_data: Dict) -> Optional[User]:
        """Check if a user exists by email.

        Args:
            raw_data: Raw data containing email

        Returns:
            User if found, None otherwise

        Raises:
            ValidationError: If email validation fails
        """
        try:
            with self.database_service.get_session() as session:
                repository = UserRepository(session)
                return repository.get_by_email(raw_data['email'])
        except Exception:
            return None

    def _list_admin_users(self) -> List[User]:
        """List all admin users.

        Returns:
            List of admin users
        """
        users = self.repository.get_all()
        return [user for user in users if user.role == UserRole.ADMIN]

    def _count_admin_users(self) -> int:
        """Count admin users.

        Returns:
            Number of admin users
        """
        try:
            with self.database_service.get_session() as session:
                repository = UserRepository(session)
                users = repository.get_all()
                admin_users = [user for user in users if user.role == UserRole.ADMIN]
                return len(admin_users)
        except Exception:
            return 0
