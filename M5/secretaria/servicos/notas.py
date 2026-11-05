"""Serviço de lançamento de nota."""

from secretaria import acesso_dados as dados  # noqa: F401 (usado nas práticas)
from secretaria.dominio import Linha, Matricula  # noqa: F401 (usado nas práticas)
from secretaria.managers import avaliacao  # noqa: F401 (usado nas práticas)

from .buscas import aluno_existente, matricula_existente, turma_existente  # noqa: F401 (usado nas práticas)


def lancar_nota(matricula: str, codigo: str, semestre: str, nota: float) -> Linha:
    """Lança a nota de um aluno numa turma, tudo numa transação:

    1. busca aluno, turma e matrícula (NaoEncontradoError se faltar algum);
    2. pede ao manager a nota que será gravada (avaliacao.preparar_nota);
    3. grava pelo acesso a dados e devolve a Linha com a nova situação.
    """
    raise NotImplementedError("TODO Aula 6, Prática 3")
