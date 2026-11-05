"""Camada de acesso a dados com o módulo sqlite3 (Aula 6).

Regras desta camada:
* é a única que escreve SQL e conhece tabelas e colunas;
* recebe a conexão aberta pelo serviço e não faz commit: quem decide a transação é o serviço;
* devolve os tipos de dominio.py, nunca linhas cruas do banco.

Este arquivo é a interface da camada: os serviços usam só o que está listado em __all__.
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
