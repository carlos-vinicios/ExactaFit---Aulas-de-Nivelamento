"""Acesso a dados: alunos."""

from typing import Any

from secretaria.dominio import Aluno

from .conexao import Conexao

SQL_ALUNO = """
SELECT a.id, a.matricula, a.nome, c.sigla
FROM aluno AS a
JOIN curso AS c ON c.id = a.curso_id
"""


def aluno_da_linha(linha: tuple[Any, ...]) -> Aluno:
    """Converte (id, matricula, nome, sigla do curso) num Aluno."""
    return Aluno(*linha)


def buscar_aluno(con: Conexao, matricula: str) -> Aluno | None:
    linha = con.execute(SQL_ALUNO + "WHERE a.matricula = ?", (matricula,)).fetchone()
    return None if linha is None else aluno_da_linha(linha)
