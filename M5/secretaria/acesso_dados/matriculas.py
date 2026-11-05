"""Acesso a dados: matrículas e notas."""

from typing import Any

from secretaria.dominio import Matricula

from .alunos import aluno_da_linha
from .conexao import Conexao
from .turmas import turma_da_linha

# Cada linha traz o aluno (4 colunas), a turma (6 colunas) e a nota.
SQL_MATRICULA = """
SELECT a.id, a.matricula, a.nome, ca.sigla,
       t.id, d.codigo, d.nome, t.semestre, p.nome, cd.sigla,
       m.nota
FROM matricula AS m
JOIN aluno AS a ON a.id = m.aluno_id
JOIN curso AS ca ON ca.id = a.curso_id
JOIN turma AS t ON t.id = m.turma_id
JOIN disciplina AS d ON d.id = t.disciplina_id
JOIN professor AS p ON p.id = t.professor_id
JOIN curso AS cd ON cd.id = d.curso_id
"""


def matricula_da_linha(linha: tuple[Any, ...]) -> Matricula:
    nota = linha[10]
    return Matricula(
        aluno_da_linha(linha[0:4]),
        turma_da_linha(linha[4:10]),
        None if nota is None else float(nota),
    )


def matriculas_do_aluno(con: Conexao, aluno_id: int) -> list[Matricula]:
    cursor = con.execute(
        SQL_MATRICULA + "WHERE a.id = ? ORDER BY t.semestre, d.codigo", (aluno_id,)
    )
    return [matricula_da_linha(linha) for linha in cursor]


def matriculas_da_turma(con: Conexao, turma_id: int) -> list[Matricula]:
    """Matrículas da turma, em ordem de nome do aluno.

    Use SQL_MATRICULA e matricula_da_linha(), como em matriculas_do_aluno().
    """
    raise NotImplementedError("TODO Aula 6, Prática 2")


def buscar_matricula(con: Conexao, aluno_id: int, turma_id: int) -> Matricula | None:
    linha = con.execute(
        SQL_MATRICULA + "WHERE a.id = ? AND t.id = ?", (aluno_id, turma_id)
    ).fetchone()
    return None if linha is None else matricula_da_linha(linha)


def gravar_nota(con: Conexao, aluno_id: int, turma_id: int, nota: float) -> None:
    """Muda a nota da matrícula com um UPDATE. Sem commit: quem confirma é o serviço."""
    raise NotImplementedError("TODO Aula 6, Prática 3")


def inserir_matricula(con: Conexao, aluno_id: int, turma_id: int) -> None:
    con.execute(
        "INSERT INTO matricula (aluno_id, turma_id) VALUES (?, ?)", (aluno_id, turma_id)
    )
