"""Admin commands implementation following SOLID principles."""

from typing import Any

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.services.database import DatabaseService
from projeto_aplicado.cli.services.user import UserService


class CreateAdminCommand(BaseCommand):
    """Create admin user command.

    Follows Single Responsibility Principle: only handles admin creation.
    Follows Dependency Inversion Principle: depends on service abstractions.
    """

    def __init__(self, db_host: str = 'localhost', **kwargs):
        """Initialize the create admin command.

        Args:
            db_host: Database hostname
            **kwargs: Additional arguments for base class
        """
        super().__init__(**kwargs)

        # Dependency injection
        self.database_service = DatabaseService(db_host)
        self.user_service = UserService(self.database_service)

    def execute(self, **kwargs: Any) -> int:
        """Execute the create admin command.

        Args:
            **kwargs: Command arguments (username, email, password, full_name, force)

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        # Validate input
        if not self.user_service.validate_input(**kwargs):
            self._print_validation_errors(**kwargs)
            return 1

        # Get parameters
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')
        full_name = kwargs.get('full_name')
        force = kwargs.get('force', False)

        # Confirmation prompt (unless force flag is used)
        if not force and not self._confirm_creation(
            username, email, full_name
        ):
            self.print_warning('Operation cancelled')
            return 0

        try:
            # Create admin user
            user = self.user_service.execute_operation(
                'create',
                username=username,
                email=email,
                password=password,
                full_name=full_name,
            )

            if user:
                self.print_success(
                    f'Admin user "{user.username}" created successfully!'
                )
                self.console.print(f'[dim]User ID: {user.id}[/dim]')
                return 0
            else:
                self.print_error(
                    f'Admin user with email "{email}" already exists.'
                )
                return 1

        except Exception as e:
            self.print_error(f'Error creating admin user: {str(e)}')
            return 1

    def _print_validation_errors(self, **kwargs) -> None:
        """Print validation error messages."""
        username = kwargs.get('username', '')
        email = kwargs.get('email', '')
        password = kwargs.get('password', '')
        full_name = kwargs.get('full_name', '')

        if not username.strip():
            self.print_error('Username cannot be empty')

        if not email.strip() or '@' not in email:
            self.print_error('Invalid email address')

        if len(password) < 6:
            self.print_error('Password must be at least 6 characters')

        if not full_name.strip():
            self.print_error('Full name cannot be empty')

    def _confirm_creation(
        self, username: str, email: str, full_name: str
    ) -> bool:
        """Show confirmation prompt for user creation.

        Args:
            username: Username to create
            email: Email for the user
            full_name: Full name of the user

        Returns:
            True if user confirms, False otherwise
        """
        self.console.print('Creating admin user:')
        self.console.print(f'  Username: {username}')
        self.console.print(f'  Email: {email}')
        self.console.print(f'  Full Name: {full_name}')
        self.console.print()

        confirm = self.console.input('[bold]Continue? (y/N): [/bold]')
        return confirm.lower() == 'y'


class CheckUserCommand(BaseCommand):
    """Check user command."""

    def __init__(self, db_host: str = 'localhost', **kwargs):
        """Initialize the check user command."""
        super().__init__(**kwargs)

        # Dependency injection
        self.database_service = DatabaseService(db_host)
        self.user_service = UserService(self.database_service)

    def execute(self, **kwargs: Any) -> int:
        """Execute the check user command."""
        email = kwargs.get('email')
        if not email:
            self.print_error('Email is required')
            return 1

        try:
            user = self.user_service.execute_operation('check', email=email)

            if user:
                self.print_success('User found:')
                self.console.print(f'  Username: {user.username}')
                self.console.print(f'  Email: {user.email}')
                self.console.print(f'  Role: {user.role.value}')
                self.console.print(f'  Full Name: {user.full_name}')
                self.console.print(f'  Created: {user.created_at}')
                return 0
            else:
                self.print_warning(f'No user found with email: {email}')
                return 1

        except Exception as e:
            self.print_error(f'Error checking user: {str(e)}')
            return 1


class ListAdminsCommand(BaseCommand):
    """List admin users command."""

    def __init__(self, db_host: str = 'localhost', **kwargs):
        """Initialize the list admins command."""
        super().__init__(**kwargs)

        # Dependency injection
        self.database_service = DatabaseService(db_host)
        self.user_service = UserService(self.database_service)

    def execute(self, **kwargs: Any) -> int:
        """Execute the list admins command."""
        try:
            admins = self.user_service.execute_operation('list')

            if admins:
                self.print_success(f'Found {len(admins)} admin user(s):')
                for admin in admins:
                    self.console.print(
                        f'  • {admin.username} ({admin.email}) - {admin.full_name}'
                    )
                return 0
            else:
                self.print_warning('No admin users found')
                return 0

        except Exception as e:
            self.print_error(f'Error listing admin users: {str(e)}')
            return 1


# Create the admin app with sub-commands
admin_app = cyclopts.App(
    name='admin',
    help='Admin user management commands',
)


# Register admin commands
@admin_app.default
def admin_default(db_host: str = 'localhost') -> int:
    """Admin user management commands."""
    console = Console()
    console.print('[bold blue]🔐 Admin User Management[/bold blue]')
    console.print()
    console.print('[blue]Available commands:[/blue]')
    console.print('  • [cyan]create[/cyan]      - Create an admin user')
    console.print(
        '  • [cyan]check[/cyan]       - Check if an admin user exists'
    )
    console.print('  • [cyan]list-admins[/cyan] - List all admin users')
    console.print()
    console.print('[yellow]Use --help with any command for details[/yellow]')
    return 0


@admin_app.command
def create(
    username: str,
    email: str,
    password: str,
    full_name: str,
    *,
    force: bool = False,
    db_host: str = 'localhost',
) -> int:
    """Create an admin user.

    Args:
        username: Username for the admin user (must be unique)
        email: Email address for the admin user (must be unique and valid)
        password: Password for the admin user (minimum 6 characters)
        full_name: Full name of the admin user
        force: Skip confirmation prompt
        db_host: Database hostname (default: localhost)
    """
    command = CreateAdminCommand(db_host=db_host)
    return command.execute(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        force=force,
    )


@admin_app.command
def check(email: str = '', *, db_host: str = 'localhost') -> int:
    """Check if an admin user exists.

    Args:
        email: Email address to check
        db_host: Database hostname (default: localhost)
    """
    command = CheckUserCommand(db_host=db_host)
    return command.execute(email=email if email else None)


@admin_app.command
def list_admins(*, db_host: str = 'localhost') -> int:
    """List all admin users in the system.

    Args:
        db_host: Database hostname (default: localhost)
    """
    command = ListAdminsCommand(db_host=db_host)
    return command.execute()
