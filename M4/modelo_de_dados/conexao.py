"""Conexão com o banco: um engine para o programa todo e uma sessão por tarefa.

O banco vem da variável DATABASE_URL, a mesma do Alembic e do ferramentas/semear.py. Sem ela,
o padrão é o escola.db (SQLite) da pasta em que o comando roda.
"""

import os
from typing import Any

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

URL_PADRAO = "sqlite:///escola.db"
URL = os.environ.get("DATABASE_URL", URL_PADRAO)

# O engine sabe falar com o banco da URL e mantém as conexões abertas para reaproveitar.
# Troque para echo=True para ver no terminal o SQL que o SQLAlchemy gera.
motor = create_engine(URL, echo=False)

if motor.dialect.name == "sqlite":

    @event.listens_for(motor, "connect")
    def _ligar_chaves(conexao_dbapi: Any, _registro: Any) -> None:
        # No SQLite as chaves estrangeiras vêm desligadas (Aula 3): liga em cada conexão.
        conexao_dbapi.execute("PRAGMA foreign_keys = ON")


# Fábrica de sessões. Uso:
#   with Sessao() as sessao:            só leitura (ou commit manual)
#   with Sessao.begin() as sessao:      transação: commit no fim, rollback se der erro
Sessao = sessionmaker(motor)
