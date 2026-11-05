"""Modelo da tabela curso."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:  # só para o mypy e o editor: evita import circular entre os arquivos
    from .aluno import Aluno
    from .disciplina import Disciplina


class Curso(Base):
    __tablename__ = "curso"

    id: Mapped[int] = mapped_column(primary_key=True)
    sigla: Mapped[str] = mapped_column(String(10), unique=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True)

    # Lado "1" das relações 1:N: um curso tem vários alunos e várias disciplinas.
    alunos: Mapped[list[Aluno]] = relationship(back_populates="curso")
    disciplinas: Mapped[list[Disciplina]] = relationship(back_populates="curso")

    def __repr__(self) -> str:
        return f"Curso({self.sigla!r}, {self.nome!r})"
