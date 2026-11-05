"""Configuração: onde está o banco e qual é o semestre em andamento."""

import os

URL_PADRAO = "sqlite:///escola.db"
SEMESTRE_ATUAL = "2026.2"


def url_banco() -> str:
    """DATABASE_URL, se estiver definida no terminal; senão, o escola.db da pasta atual."""
    return os.environ.get("DATABASE_URL", URL_PADRAO)
