"""Acesso a arquivos: o único lugar que lê e grava documentos no disco (M7, Aula 9).

É uma camada de acesso a dados, como acesso_orm, só que os dados ficam numa pasta, e não no
banco: documentos/<matrícula>/<nome do arquivo>. Os serviços usam só estas funções e recebem
Documento (de dominio.py) e bytes; nenhum caminho de arquivo sai desta camada.
"""

import mimetypes
from pathlib import Path

from secretaria import config
from secretaria.dominio import Documento


def _caminho(matricula: str, nome: str) -> Path | None:
    """O caminho do arquivo, ou None se o nome tentar sair da pasta do aluno (../, /, \\)."""
    if not nome or nome.startswith(".") or "/" in nome or "\\" in nome:
        return None
    return config.pasta_documentos() / matricula / nome


def _documento(matricula: str, caminho: Path) -> Documento:
    tipo = mimetypes.guess_type(caminho.name)[0] or "application/octet-stream"
    return Documento(matricula, caminho.name, tipo, caminho.stat().st_size)


def existe(matricula: str, nome: str) -> bool:
    caminho = _caminho(matricula, nome)
    return caminho is not None and caminho.is_file()


def gravar(matricula: str, nome: str, conteudo: bytes) -> Documento:
    caminho = _caminho(matricula, nome)
    if caminho is None:
        raise ValueError(f"nome de arquivo inválido: {nome!r}")
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(conteudo)
    return _documento(matricula, caminho)


def listar(matricula: str) -> list[Documento]:
    pasta = config.pasta_documentos() / matricula
    if not pasta.is_dir():
        return []
    return [_documento(matricula, c) for c in sorted(pasta.iterdir()) if c.is_file()]


def ler(matricula: str, nome: str) -> tuple[Documento, bytes] | None:
    caminho = _caminho(matricula, nome)
    if caminho is None or not caminho.is_file():
        return None
    return _documento(matricula, caminho), caminho.read_bytes()
