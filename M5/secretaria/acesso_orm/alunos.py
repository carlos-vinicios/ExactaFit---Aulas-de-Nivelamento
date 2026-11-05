"""Acesso a dados pelo ORM: alunos."""

from sqlalchemy import select

from secretaria.dominio import Aluno

from . import modelos
from .conexao import Conexao


def aluno_do_modelo(registro: modelos.Aluno) -> Aluno:
    """Converte o objeto do ORM no Aluno do domínio: o ORM não sai desta camada."""
    return Aluno(registro.id, registro.matricula, registro.nome, registro.curso.sigla)


def buscar_aluno(sessao: Conexao, matricula: str) -> Aluno | None:
    registro = sessao.scalar(
        select(modelos.Aluno).where(modelos.Aluno.matricula == matricula)
    )
    return None if registro is None else aluno_do_modelo(registro)
