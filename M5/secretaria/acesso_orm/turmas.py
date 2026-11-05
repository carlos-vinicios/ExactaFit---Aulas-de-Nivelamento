"""Acesso a dados pelo ORM: turmas."""

from sqlalchemy import select

from secretaria.dominio import Turma

from . import modelos
from .conexao import Conexao


def turma_do_modelo(registro: modelos.Turma) -> Turma:
    disciplina = registro.disciplina
    return Turma(
        registro.id,
        disciplina.codigo,
        disciplina.nome,
        registro.semestre,
        registro.professor.nome,
        disciplina.curso.sigla,
    )


def buscar_turma(sessao: Conexao, codigo: str, semestre: str) -> Turma | None:
    registro = sessao.scalar(
        select(modelos.Turma)
        .join(modelos.Turma.disciplina)
        .where(modelos.Disciplina.codigo == codigo, modelos.Turma.semestre == semestre)
    )
    return None if registro is None else turma_do_modelo(registro)
