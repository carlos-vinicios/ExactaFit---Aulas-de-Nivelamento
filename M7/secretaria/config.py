"""Configuração: onde estão o banco e os documentos, e qual é o semestre em andamento."""

import os
from pathlib import Path

URL_PADRAO = "sqlite:///escola.db"
PASTA_DOCUMENTOS = "documentos"
SEMESTRE_ATUAL = "2026.2"


def url_banco() -> str:
    """DATABASE_URL, se estiver definida no terminal; senão, o escola.db da pasta atual."""
    return os.environ.get("DATABASE_URL", URL_PADRAO)


def pasta_documentos() -> Path:
    """DOCUMENTOS_DIR, se estiver definida; senão, a pasta documentos da pasta atual (M7)."""
    return Path(os.environ.get("DOCUMENTOS_DIR", PASTA_DOCUMENTOS))
