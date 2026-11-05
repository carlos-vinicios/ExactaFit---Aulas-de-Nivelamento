"""Abrir o banco com o SQLAlchemy: o engine e a sessão da Aula 5, agora dentro da camada."""

from collections.abc import Iterator
from contextlib import contextmanager
from functools import cache
from typing import Any

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from secretaria import config
from secretaria.erros import BancoIndisponivelError

# Tipo da conexão desta camada; os serviços usam o nome dados.Conexao.
type Conexao = Session


@cache
def motor(url: str) -> Engine:
    """Um engine por URL, criado na primeira chamada e reaproveitado nas seguintes."""
    engine = create_engine(url)
    if engine.dialect.name == "sqlite":

        @event.listens_for(engine, "connect")
        def _ligar_chaves(conexao_dbapi: Any, _registro: Any) -> None:
            conexao_dbapi.execute("PRAGMA foreign_keys = ON")

    return engine


@contextmanager
def abrir() -> Iterator[Conexao]:
    """Abre uma sessão numa transação: commit no fim do bloco, rollback se houver erro."""
    try:
        with Session(motor(config.url_banco())) as sessao, sessao.begin():
            yield sessao
    except OperationalError as erro:
        motivo = str(erro.orig).strip().splitlines()[0]
        raise BancoIndisponivelError(
            f"não foi possível usar o banco: {motivo}"
        ) from erro
