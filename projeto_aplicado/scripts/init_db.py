"""Script to initialize the database."""

import asyncio
import logging
from contextlib import asynccontextmanager

import asyncpg
from alembic import command
from alembic.config import Config

from projeto_aplicado.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def get_postgres_connection(database='postgres'):
    """Get a connection to PostgreSQL with proper cleanup."""
    conn = None
    try:
        conn = await asyncpg.connect(
            host=settings.POSTGRES_HOSTNAME,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=database,
        )
        yield conn
    finally:
        if conn:
            await conn.close()


async def create_database():
    """Create the database if it doesn't exist."""
    async with get_postgres_connection() as sys_conn:
        try:
            # Check if database exists
            exists = await sys_conn.fetchval(
                'SELECT 1 FROM pg_database WHERE datname = $1',
                settings.POSTGRES_DB,
            )

            if not exists:
                logger.info(f'Creating database {settings.POSTGRES_DB}')
                await sys_conn.execute(
                    f'CREATE DATABASE "{settings.POSTGRES_DB}"'
                )
                logger.info(
                    f'Database {settings.POSTGRES_DB} created successfully'
                )
            else:
                logger.info(f'Database {settings.POSTGRES_DB} already exists')

        except Exception as e:
            logger.error(f'Error creating database: {str(e)}')
            raise


def init_database():
    """Initialize the database with all tables using Alembic."""
    try:
        # Create database if it doesn't exist
        asyncio.run(create_database())

        # Configure Alembic using the existing alembic.ini
        alembic_cfg = Config('alembic.ini')

        # Run migrations
        logger.info('Running database migrations...')
        command.upgrade(alembic_cfg, 'head')
        logger.info('Database migrations completed successfully')

    except Exception as e:
        logger.error(f'Database initialization failed: {str(e)}')
        raise


def main():
    """Main function to run the database initialization."""
    logging.basicConfig(level=logging.INFO)
    try:
        init_database()
    except Exception as e:
        logger.error(f'Failed to initialize database: {str(e)}')
        raise


if __name__ == '__main__':
    main()
