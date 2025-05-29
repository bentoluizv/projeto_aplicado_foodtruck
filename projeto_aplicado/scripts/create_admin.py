"""Script to create an admin user manually."""

import sys

import click
from sqlmodel import Session, select

from projeto_aplicado.auth.password import get_password_hash
from projeto_aplicado.ext.database.db import get_engine
from projeto_aplicado.resources.user.model import User, UserRole
from projeto_aplicado.settings import get_settings

settings = get_settings()


def create_admin_user(session: Session, name: str, email: str, password: str):
    """Create an admin user if it doesn't exist."""
    try:
        # Check if admin user exists
        stmt = select(User).where(User.email == email)
        existing_user = session.exec(stmt).first()

        if not existing_user:
            user = User(
                name=name,
                email=email,
                password=get_password_hash(password),
                role=UserRole.ADMIN,
            )
            session.add(user)
            session.commit()

    except Exception as e:
        raise


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--name', prompt='Admin name', help='Name of the admin user')
@click.option('--email', prompt='Admin email', help='Email of the admin user')
@click.option(
    '--password',
    prompt=True,
    hide_input=True,
    help='Password for the admin user',
)
def main(verbose, name, email, password):
    """Create an admin user manually."""
    try:
        engine = get_engine()
        with Session(engine) as session:
            create_admin_user(session, name, email, password)
    except Exception as e:
        sys.exit(1)


if __name__ == '__main__':
    main()
