"""Serviços dos documentos dos alunos (M7, Aula 9: exemplo de upload e download).

O banco só confere se o aluno existe; o arquivo vai para a camada acesso_arquivos.
"""

from secretaria import acesso_arquivos as arquivos
from secretaria import acesso_orm as dados
from secretaria.dominio import Documento
from secretaria.erros import NaoEncontradoError
from secretaria.managers import documentos as regras

from .buscas import aluno_existente


def guardar_documento(matricula: str, nome: str, tipo: str, conteudo: bytes) -> Documento:
    """Confere o aluno e as regras, e só então grava o arquivo."""
    nome = regras.nome_seguro(nome)
    with dados.abrir() as con:
        aluno_existente(con, matricula)
    regras.conferir_documento(nome, tipo, len(conteudo), arquivos.existe(matricula, nome))
    return arquivos.gravar(matricula, nome, conteudo)


def listar_documentos(matricula: str) -> list[Documento]:
    with dados.abrir() as con:
        aluno_existente(con, matricula)
    return arquivos.listar(matricula)


def ler_documento(matricula: str, nome: str) -> tuple[Documento, bytes]:
    with dados.abrir() as con:
        aluno_existente(con, matricula)
    lido = arquivos.ler(matricula, nome)
    if lido is None:
        raise NaoEncontradoError(f"documento {nome} de {matricula} não encontrado")
    return lido
