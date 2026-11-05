"""Montagem dos relatórios: boletim do aluno e relatório da turma."""

from collections import Counter  # noqa: F401 (usado nas práticas)

from secretaria.dominio import (
    Aluno,
    Boletim,
    Matricula,
    RelatorioTurma,
    Situacao,  # noqa: F401 (usado nas práticas)
    Turma,
)

from .avaliacao import classificar, media


def montar_boletim(aluno: Aluno, matriculas: list[Matricula]) -> Boletim:
    return Boletim(aluno, classificar(matriculas), media(m.nota for m in matriculas))


def montar_relatorio_turma(turma: Turma, matriculas: list[Matricula]) -> RelatorioTurma:
    """Linhas classificadas, média da turma e quantos alunos em cada situação.

    A contagem tem as três situações, mesmo as que ficam com zero:
    {Situacao.CURSANDO: 0, Situacao.APROVADO: 8, Situacao.REPROVADO: 3}.
    Dica: collections.Counter, como na Aula 2.
    """
    raise NotImplementedError("TODO Aula 6, Prática 2")
