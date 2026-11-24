"""Regras dos documentos dos alunos (M7, Aula 9: exemplo de upload)."""

import mimetypes
from pathlib import PurePosixPath

from secretaria.erros import RegraDeNegocioError

TIPOS_ACEITOS = {"application/pdf", "image/png", "image/jpeg"}
TAMANHO_MAXIMO = 2 * 1024 * 1024  # 2 MB


def nome_seguro(nome: str) -> str:
    """Só o nome, sem pastas: "../../config.py" vira "config.py".

    Nunca use o nome enviado pelo cliente como caminho no disco.
    """
    limpo = PurePosixPath(nome.replace("\\", "/")).name.strip()
    if not limpo or limpo.startswith("."):
        raise RegraDeNegocioError("o arquivo precisa de um nome, como atestado.pdf")
    return limpo


def conferir_documento(nome: str, tipo: str, tamanho: int, ja_existe: bool) -> None:
    """A escola aceita PDF, PNG e JPEG de até 2 MB, e um nome por documento."""
    if tipo not in TIPOS_ACEITOS:
        raise RegraDeNegocioError(f"tipo {tipo} não aceito; envie PDF, PNG ou JPEG")
    if mimetypes.guess_type(nome)[0] != tipo:
        raise RegraDeNegocioError(
            f"a extensão de {nome} não corresponde ao tipo {tipo}"
        )
    if tamanho == 0:
        raise RegraDeNegocioError(f"o arquivo {nome} está vazio")
    if tamanho > TAMANHO_MAXIMO:
        raise RegraDeNegocioError(f"o arquivo tem {tamanho} bytes; o máximo é 2 MB")
    if ja_existe:
        raise RegraDeNegocioError(f"o aluno já tem um documento chamado {nome}")
