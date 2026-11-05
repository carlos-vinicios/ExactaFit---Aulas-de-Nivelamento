"""Serviços de consulta: boletim do aluno e relatório da turma."""

from secretaria import acesso_dados as dados
from secretaria.dominio import Boletim, RelatorioTurma
from secretaria.managers import relatorios

from .buscas import aluno_existente, turma_existente  # noqa: F401 (usado nas práticas)


def consultar_boletim(matricula: str) -> Boletim:
    with dados.abrir() as con:
        aluno = aluno_existente(con, matricula)
        matriculas = dados.matriculas_do_aluno(con, aluno.id)
        return relatorios.montar_boletim(aluno, matriculas)


def relatorio_turma(codigo: str, semestre: str) -> RelatorioTurma:
    """Relatório de uma turma: busca a turma e as matrículas e pede ao manager o relatório.

    Turma inexistente: NaoEncontradoError (use turma_existente, como consultar_boletim usa
    aluno_existente).
    """
    raise NotImplementedError("TODO Aula 6, Prática 2")
