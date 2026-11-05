"""Acesso a dados: turmas."""

from typing import Any

from secretaria.dominio import Turma

from .conexao import Conexao

SQL_TURMA = """
SELECT t.id, d.codigo, d.nome, t.semestre, p.nome, c.sigla
FROM turma AS t
JOIN disciplina AS d ON d.id = t.disciplina_id
JOIN professor AS p ON p.id = t.professor_id
JOIN curso AS c ON c.id = d.curso_id
"""


def turma_da_linha(linha: tuple[Any, ...]) -> Turma:
    """Converte (id, código, disciplina, semestre, professor, sigla do curso) numa Turma."""
    return Turma(*linha)


def buscar_turma(con: Conexao, codigo: str, semestre: str) -> Turma | None:
    linha = con.execute(
        SQL_TURMA + "WHERE d.codigo = ? AND t.semestre = ?", (codigo, semestre)
    ).fetchone()
    return None if linha is None else turma_da_linha(linha)
