"""Acesso a dados pelo ORM: matrículas e notas."""

from sqlalchemy import Select, select

from secretaria.dominio import Matricula

from . import modelos
from .alunos import aluno_do_modelo
from .conexao import Conexao
from .turmas import turma_do_modelo


def matricula_do_modelo(registro: modelos.Matricula) -> Matricula:
    return Matricula(
        aluno_do_modelo(registro.aluno), turma_do_modelo(registro.turma), registro.nota
    )


def consulta_matriculas() -> Select[modelos.Matricula]:
    """SELECT de matrícula com as junções até aluno, turma e disciplina, para filtrar e ordenar."""
    return (
        select(modelos.Matricula)
        .join(modelos.Matricula.aluno)
        .join(modelos.Matricula.turma)
        .join(modelos.Turma.disciplina)
    )


def matriculas_do_aluno(sessao: Conexao, aluno_id: int) -> list[Matricula]:
    consulta = (
        consulta_matriculas()
        .where(modelos.Matricula.aluno_id == aluno_id)
        .order_by(modelos.Turma.semestre, modelos.Disciplina.codigo)
    )
    return [matricula_do_modelo(r) for r in sessao.scalars(consulta)]


def matriculas_da_turma(sessao: Conexao, turma_id: int) -> list[Matricula]:
    """Matrículas da turma, em ordem de nome do aluno. Siga matriculas_do_aluno()."""
    raise NotImplementedError("TODO Aula 7, Prática 2")


def buscar_matricula(sessao: Conexao, aluno_id: int, turma_id: int) -> Matricula | None:
    registro = sessao.get(modelos.Matricula, (aluno_id, turma_id))
    return None if registro is None else matricula_do_modelo(registro)


def gravar_nota(sessao: Conexao, aluno_id: int, turma_id: int, nota: float) -> None:
    """Muda a nota do objeto Matricula; a sessão faz o UPDATE no commit do serviço."""
    raise NotImplementedError("TODO Aula 7, Prática 2")


def inserir_matricula(sessao: Conexao, aluno_id: int, turma_id: int) -> None:
    """Acrescenta uma Matricula sem nota e envia o INSERT com flush()."""
    raise NotImplementedError("TODO Aula 7, Prática 3")
