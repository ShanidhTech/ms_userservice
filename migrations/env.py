from logging.config import fileConfig

from sqlalchemy import create_engine
from alembic import context

from database import DATABASE_URL
from models import User  # Import Base from your database module

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use metadata for autogeneration
target_metadata = User.metadata  # ✅ FIXED: Use `Base.metadata`

# Create a synchronous engine for migrations
sync_engine = create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))  # ✅ Convert to psycopg2


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (without DB connection)."""
    url = config.get_main_option("sqlalchemy.url") or DATABASE_URL.replace("asyncpg", "psycopg2")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (with DB connection)."""
    with sync_engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Run migrations
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
