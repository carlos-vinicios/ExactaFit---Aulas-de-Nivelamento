"""Regras de matrícula (Aula 7)."""

from secretaria.config import SEMESTRE_ATUAL  # noqa: F401 (usado nas práticas)
from secretaria.dominio import Aluno, Turma
from secretaria.erros import RegraDeNegocioError  # noqa: F401 (usado nas práticas)


def conferir_matricula(aluno: Aluno, turma: Turma, ja_matriculado: bool) -> None:
    """Regras da matrícula, nesta ordem:

    * só no semestre em andamento (SEMESTRE_ATUAL);
    * a disciplina tem de ser do curso do aluno;
    * o aluno não pode estar matriculado na turma (ja_matriculado).

    Regra não atendida: RegraDeNegocioError com as mensagens do enunciado.
    """
    raise NotImplementedError("TODO Aula 7, Prática 3")
