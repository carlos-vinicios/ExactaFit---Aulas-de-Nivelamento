"""Ambiente do Alembic: decide em qual banco as migrações rodam."""

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Sem modelos ORM: as migrações são escritas à mão com op.create_table, op.add_column etc.
target_metadata = None


def url() -> str:
    # Prioridade: alembic -x url=... > variável DATABASE_URL > sqlite:///escola.db
    da_linha = context.get_x_argument(as_dictionary=True).get("url")
    return da_linha or os.environ.get("DATABASE_URL", "sqlite:///escola.db")


def run_migrations_offline() -> None:
    """alembic upgrade head --sql: só imprime o SQL, sem conectar."""
    alvo = url()
    context.configure(
        url=alvo,
        target_metadata=target_metadata,
        literal_binds=True,
        render_as_batch=alvo.startswith("sqlite"),
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(url())
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # O SQLite tem ALTER TABLE limitado. No modo batch o Alembic recria a tabela
            # (cria nova, copia os dados, apaga a antiga, renomeia).
            render_as_batch=connection.dialect.name == "sqlite",
        )
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
