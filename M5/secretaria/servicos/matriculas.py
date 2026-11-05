"""Serviços de matrícula (Aula 7)."""

from secretaria import acesso_dados as dados  # noqa: F401 (usado nas práticas)
from secretaria.dominio import Linha, Matricula, Situacao  # noqa: F401 (usado nas práticas)
from secretaria.managers import matriculas as regras  # noqa: F401 (usado nas práticas)
from secretaria.schemas import NovaMatricula

from .buscas import aluno_existente, turma_existente  # noqa: F401 (usado nas práticas)


def matricular(pedido: NovaMatricula) -> Linha:
    """Matricula o aluno na turma, numa transação:

    1. busca aluno e turma e confere se a matrícula já existe (dados.buscar_matricula);
    2. pede ao manager que confira as regras (regras.conferir_matricula);
    3. insere pelo acesso a dados e devolve a Linha da matrícula nova, sem nota.
    """
    raise NotImplementedError("TODO Aula 7, Prática 3")
