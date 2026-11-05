"""Camada de acesso a dados com o SQLAlchemy ORM (Aula 7).

A mesma interface de acesso_dados (sqlite3): as mesmas funções, com os mesmos parâmetros e os
mesmos tipos de saída. Por isso os serviços trocam de uma para a outra mudando só o import.
Diferenças: funciona com qualquer banco da DATABASE_URL, inclusive o PostgreSQL, e as consultas
são escritas com select() sobre os modelos da pasta modelos/.
"""

from .alunos import buscar_aluno
from .conexao import Conexao, abrir
from .matriculas import (
    buscar_matricula,
    gravar_nota,
    inserir_matricula,
    matriculas_da_turma,
    matriculas_do_aluno,
)
from .turmas import buscar_turma

__all__ = [
    "Conexao",
    "abrir",
    "buscar_aluno",
    "buscar_matricula",
    "buscar_turma",
    "gravar_nota",
    "inserir_matricula",
    "matriculas_da_turma",
    "matriculas_do_aluno",
]
