"""Script to create an admin user manually."""

import sys

import click
from sqlmodel import Session, select

from projeto_aplicado.auth.password import get_password_hash
from projeto_aplicado.ext.database.db import get_engine
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.resources.user.schemas import CreateUserDTO
from projeto_aplicado.settings import get_settings

settings = get_settings()


def create_admin_user(session: Session, dto: CreateUserDTO):
    """Create an admin user if it doesn't exist."""
    try:
        # Check if admin user exists
        stmt = select(User).where(User.email == dto.email)
        existing_user = session.exec(stmt).first()

        if not existing_user:
            user = User(
                username=dto.username,
                email=dto.email,
                password=get_password_hash(dto.password),
                role=dto.role,
                full_name=dto.full_name,
            )
            session.add(user)
            session.commit()

    except Exception:
        raise


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option(
    '--username', prompt='Admin username', help='Username of the admin user   '
)
@click.option('--email', prompt='Admin email', help='Email of the admin user')
@click.option(
    '--password',
    prompt=True,
    hide_input=True,
    help='Password for the admin user',
)
@click.option(
    '--username', prompt='Admin username', help='Username of the admin user'
)
def main(verbose, email, password, username):
    """Create an admin user manually."""
    try:
        engine = get_engine()
        with Session(engine) as session:
            dto = CreateUserDTO(
                username=username,
                email=email,
                password=password,
                role=UserRole.ADMIN,
            )
            create_admin_user(session, dto)
    except Exception as e:
        sys.exit(1)


if __name__ == '__main__':
    main()
