import asyncio
import socket
from logging.config import fileConfig

import sqlalchemy
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from src.configuration import conf
from src.db import Base


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = Base.metadata


config.set_main_option('sqlalchemy.url', conf.db.build_connection_str())


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


class FailedConnectToDatabase(Exception):
    def __init__(self, url_info: str, other=""):
        self.url_info = url_info
        self.other = other

    def __str__(self):
        return f"Tried connect to {self.url_info} ({self.other})"


class MigrationError(Exception):
    def __init__(self, info: str):
        self.info = info

    def __str__(self):
        return self.info


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )
    try:
        async with connectable.connect() as connection:
                await connection.run_sync(do_run_migrations)
    except ProgrammingError as pe:
        raise MigrationError(str(pe))
    except (Exception) as e:
        raise FailedConnectToDatabase(url_info=connectable.url, other=e)
    finally:
        await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
