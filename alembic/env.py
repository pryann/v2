from alembic import context
from sqlalchemy import pool, engine_from_config
from logging.config import fileConfig
from src.user.models import User
from src.billing_address.models import BillingAddress
from src.models import CustomBase
from src.config import get_settings
    
settings = get_settings()
config = context.config
config.set_main_option("sqlalchemy.url", settings.MYSQL_DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = CustomBase.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=settings.mysql_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
