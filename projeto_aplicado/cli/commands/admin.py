"""Admin commands implementation following SOLID principles."""

from typing import Any, Dict

import cyclopts
from rich.console import Console

from projeto_aplicado.cli.base.command import BaseCommand
from projeto_aplicado.cli.schemas import UserListResult, UserOperationResult
from projeto_aplicado.cli.services.user import UserService


class CreateAdminCommand(BaseCommand):
    """Create a new admin user.

    Creates an admin user with full access to the system.
    Requires username, email, password, and full name.
    """

    def __init__(self, **kwargs):
        """Initialize the create admin command."""
        super().__init__(**kwargs)
        self.user_service = self.get_service(UserService)

    def execute(self, **kwargs: Any) -> int:
        """Execute the create admin command.

        Creates a new admin user with the provided information.
        Shows a confirmation prompt unless --force is used.

        Returns:
            0 if successful, 1 if failed
        """
        raw_data = {
            'username': kwargs['username'],
            'email': kwargs['email'],
            'password': kwargs['password'],
            'full_name': kwargs['full_name'],
        }

        force = kwargs.get('force', False)
        if not force and not self._confirm_creation(raw_data):
            self.print_warning('Operation cancelled')
            return 0

        result: UserOperationResult = self.user_service.create_admin(raw_data)
        if result.success:
            user = result.data
            msg = (
                f'[green]Admin user "{user.username}" created successfully![/green]\n'  # noqa: E501
                f'[dim]User ID: {user.id}[/dim]'
            )
            self.console.print(msg)
            return 0
        else:
            self.print_error(result.error or 'Failed to create admin user')
            return 1

    def _confirm_creation(self, data: Dict) -> bool:
        """Show confirmation prompt before creating the admin user.

        Args:
            data: User data to be confirmed

        Returns:
            True if user confirms, False if cancelled
        """
        msg = (
            '[blue]Creating admin user:[/blue]\n'
            f'  Username: {data["username"]}\n'
            f'  Email: {data["email"]}\n'
            f'  Full Name: {data["full_name"]}\n'
        )
        self.console.print(msg)
        confirm = self.console.input('[bold]Continue? (y/N): [/bold]')
        return confirm.lower() == 'y'


class CheckUserCommand(BaseCommand):
    """Check if a user exists and display their information.

    Looks up a user by email address and shows their details
    including username, role, and creation date.
    """

    def __init__(self, **kwargs):
        """Initialize the check user command."""
        super().__init__(**kwargs)
        self.user_service = self.get_service(UserService)

    def execute(self, **kwargs: Any) -> int:
        """Look up and display user information.

        Searches for a user by email address and displays
        their profile information if found.

        Returns:
            0 if user found, 1 if not found or error
        """
        email = kwargs.get('email')
        if not email:
            self.print_error('Email is required')
            return 1

        raw_data = {'email': email}
        result: UserOperationResult = self.user_service.check_user(raw_data)

        if not result.success:
            self.print_error(result.error or 'Failed to check user')
            return 1

        user = result.data
        if user:
            msg = (
                '[green]User found:[/green]\n'
                f'  Username: {user.username}\n'
                f'  Email: {user.email}\n'
                f'  Role: {user.role.value}\n'
                f'  Full Name: {user.full_name}\n'
                f'  Created: {user.created_at}'
            )
            self.console.print(msg)
            return 0
        else:
            self.print_warning(f'No user found with email: {email}')
            return 1


class ListAdminsCommand(BaseCommand):
    """List all admin users in the system.

    Displays a list of all users with admin privileges,
    showing their username, email, and full name.
    """

    def __init__(self, **kwargs):
        """Initialize the list admins command."""
        super().__init__(**kwargs)
        self.user_service = self.get_service(UserService)

    def execute(self, **kwargs: Any) -> int:
        """List all admin users.

        Retrieves and displays all users with admin role.
        Shows count and details for each admin user.

        Returns:
            0 if successful, 1 if error occurred
        """
        result: UserListResult = self.user_service.list_admins()

        if not result.success:
            self.print_error(result.error or 'Failed to list admin users')
            return 1

        admins = result.data
        if admins:
            admin_list = '\n'.join(
                f'  • {admin.username} ({admin.email}) - {admin.full_name}'
                for admin in admins
            )
            msg = (
                f'[green]Found {len(admins)} admin user(s):[/green]\n'
                f'{admin_list}'
            )
            self.console.print(msg)
            return 0
        else:
            self.print_warning('No admin users found')
            return 0


# Create the admin app with sub-commands
admin_app = cyclopts.App(
    name='admin',
    help='Admin user management commands',
)


# Register admin commands
@admin_app.default
def admin_default() -> int:
    """Manage admin users - create, check, and list administrators.

    Use subcommands to perform specific admin user operations.
    """
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
    force: bool = False,
) -> int:
    """Create an admin user.

    Args:
        username: Username for the admin user (must be unique)
        email: Email address for the admin user (must be unique and valid)
        password: Password for the admin user (minimum 6 characters)
        full_name: Full name of the admin user
        force: Skip confirmation prompt
    """
    command = CreateAdminCommand()
    return command.execute(
        username=username,
        email=email,
        password=password,
        full_name=full_name,
        force=force,
    )


@admin_app.command
def check(email: str) -> int:
    """Check if an admin user exists.

    Args:
        email: Email address to check
    """
    command = CheckUserCommand()
    return command.execute(email=email)


@admin_app.command
def list_admins() -> int:
    """List all admin users in the system.

    Lists all admin users in the system.
    """
    command = ListAdminsCommand()
    return command.execute()
