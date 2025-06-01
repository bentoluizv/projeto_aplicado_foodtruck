"""Script to create an admin user manually."""

import sys
from typing import Optional

import click
from sqlmodel import Session, select

from projeto_aplicado.auth.password import get_password_hash
from projeto_aplicado.ext.database.db import get_engine
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.user.schemas import CreateUserDTO


def create_admin_user(session: Session, dto: CreateUserDTO) -> Optional[User]:
    """Create an admin user if it doesn't exist.

    Args:
        session: Database session
        dto: User creation data transfer object

    Returns:
        Created user if successful, None if user already exists
    """
    if session.exec(select(User).where(User.email == dto.email)).first():
        return None

    user = User(
        username=dto.username,
        email=dto.email,
        password=get_password_hash(dto.password),
        role=UserRole.ADMIN,
        full_name=dto.full_name,
    )
    session.add(user)
    session.commit()
    return user


def validate_input(ctx, param, value):
    """Validate input value is not empty.

    Args:
        ctx: Click context
        param: Click parameter
        value: Input value to validate

    Returns:
        Validated value

    Raises:
        click.BadParameter: If value is empty
    """
    if not value or not value.strip():
        raise click.BadParameter(f'{param.name} cannot be empty')
    return value


@click.command()
@click.option(
    '--username',
    prompt='Admin username',
    help='Username of the admin user',
    callback=validate_input,
)
@click.option(
    '--email',
    prompt='Admin email',
    help='Email of the admin user',
    callback=validate_input,
)
@click.option(
    '--password',
    prompt=True,
    hide_input=True,
    help='Password for the admin user',
    callback=validate_input,
)
@click.option(
    '--full-name',
    prompt='Admin full name',
    help='Full name of the admin user',
    callback=validate_input,
)
def main(username: str, email: str, password: str, full_name: str) -> None:
    """Create an admin user manually."""
    try:
        with Session(get_engine()) as session:
            dto = CreateUserDTO(
                username=username,
                email=email,
                password=password,
                role=UserRole.ADMIN,
                full_name=full_name,
            )
            if user := create_admin_user(session, dto):
                click.echo(f'Admin user {user.username} created successfully!')
            else:
                click.echo(f'Admin user with email {email} already exists.')
                sys.exit(1)
    except Exception as e:
        click.echo(f'Error creating admin user: {str(e)}', err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
