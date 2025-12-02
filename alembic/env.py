import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context

# 1. IMPORTAMOS NUESTRA CONFIGURACIÓN Y MODELOS
from app.core.config import settings
from app.models import User  # Importante para que Alembic 'vea' la tabla User

# Configuración de Alembic
config = context.config

# Configuración de Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. DEFINIMOS LA METADATA
target_metadata = SQLModel.metadata

# 3. SOBRESCRIBIMOS LA URL CON LA DE NUESTRO .env
# Esto es vital para no tener la clave hard-codeada en alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


def run_migrations_offline() -> None:
    """Correr migraciones en modo 'offline'."""
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


async def run_migrations_online() -> None:
    """Correr migraciones en modo 'online' (con conexión asíncrona)."""

    # Creamos el motor asíncrono usando la configuración inyectada
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Aquí está el truco: ejecutamos la función síncrona dentro del contexto async
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Ejecutamos el loop asíncrono
    asyncio.run(run_migrations_online())