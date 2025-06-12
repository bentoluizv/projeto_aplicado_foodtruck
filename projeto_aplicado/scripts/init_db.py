"""Script to initialize the database."""

import sys
from contextlib import contextmanager

import click
import psycopg2
from alembic import command
from alembic.config import Config

from projeto_aplicado.settings import get_settings

settings = get_settings()


@contextmanager
def get_postgres_connection(database='postgres', autocommit=False):
    """Get a connection to PostgreSQL with proper cleanup."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOSTNAME,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=database,
        )
        if autocommit:
            conn.autocommit = True
        yield conn
    finally:
        if conn:
            conn.close()


def create_database(conn):
    """Create the database if it doesn't exist (database-level operation)."""
    try:
        # Check if database exists
        with conn.cursor() as cur:
            cur.execute(
                'SELECT 1 FROM pg_database WHERE datname = %s',
                (settings.POSTGRES_DB,),
            )
            exists = cur.fetchone()

        if not exists:
            with conn.cursor() as cur:
                cur.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')

    except Exception:
        raise


def run_migrations():
    """Run database migrations using Alembic (database-level operation)."""
    try:
        # Configure Alembic using the existing alembic.ini
        alembic_cfg = Config('alembic.ini')

        # Run migrations
        command.upgrade(alembic_cfg, 'head')
    except Exception:
        raise


def init_database():
    """Initialize the database with all tables."""
    try:
        with get_postgres_connection(autocommit=True) as sys_conn:
            create_database(sys_conn)
            run_migrations()

    except Exception:
        raise


@click.command()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(verbose):
    """Initialize the database with all required tables and migrations."""
    try:
        init_database()
    except Exception:
        sys.exit(1)


if __name__ == '__main__':
    main()
