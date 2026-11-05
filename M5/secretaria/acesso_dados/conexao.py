"""Abrir o banco com o módulo sqlite3: conexão, commit e rollback num só lugar."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from secretaria import config
from secretaria.erros import BancoIndisponivelError

# Tipo da conexão desta camada; os serviços usam o nome dados.Conexao.
type Conexao = sqlite3.Connection


@contextmanager
def abrir() -> Iterator[Conexao]:
    """Abre o banco de config.url_banco(). Confirma no fim do bloco ou desfaz se houver erro."""
    url = config.url_banco()
    if not url.startswith("sqlite:///"):
        tipo = url.split("://")[0]
        raise BancoIndisponivelError(
            f"o acesso com sqlite3 só abre bancos SQLite, e DATABASE_URL aponta para {tipo}"
        )
    caminho = Path(url.removeprefix("sqlite:///"))
    if not caminho.exists():
        raise BancoIndisponivelError(
            f"o banco {caminho} não existe; crie com "
            "python ../M4/ferramentas/criar_banco.py escola.db"
        )
    con = sqlite3.connect(caminho)
    con.execute("PRAGMA foreign_keys = ON")  # desligado por padrão no SQLite (Aula 3)
    try:
        yield con
        con.commit()
    except BaseException:
        con.rollback()
        raise
    finally:
        con.close()
