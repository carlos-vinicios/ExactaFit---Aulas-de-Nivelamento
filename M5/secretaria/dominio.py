"""Tipos do domínio: o que circula entre as camadas.

Não sabem nada de banco nem de terminal. O acesso a dados devolve Aluno, Turma e Matricula; os
managers montam Linha, Boletim e RelatorioTurma; a apresentação só lê esses objetos.
"""

from dataclasses import dataclass
from enum import StrEnum


class Situacao(StrEnum):
    CURSANDO = "cursando"
    APROVADO = "aprovado"
    REPROVADO = "reprovado"


@dataclass(frozen=True, slots=True)
class Aluno:
    id: int
    matricula: str
    nome: str
    curso: str  # sigla do curso, como CC


@dataclass(frozen=True, slots=True)
class Turma:
    id: int
    codigo: str
    disciplina: str
    semestre: str
    professor: str
    curso: str  # sigla do curso da disciplina


@dataclass(frozen=True, slots=True)
class Matricula:
    aluno: Aluno
    turma: Turma
    nota: float | None


@dataclass(frozen=True, slots=True)
class Linha:
    """Uma matrícula com a situação calculada pelo manager."""

    matricula: Matricula
    situacao: Situacao


@dataclass(frozen=True, slots=True)
class Boletim:
    aluno: Aluno
    linhas: list[Linha]
    media: float | None


@dataclass(frozen=True, slots=True)
class RelatorioTurma:
    turma: Turma
    linhas: list[Linha]
    media: float | None
    contagem: dict[Situacao, int]
