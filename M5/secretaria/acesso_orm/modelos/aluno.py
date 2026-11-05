"""Modelo da tabela aluno."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .curso import Curso
    from .matricula import Matricula


class Aluno(Base):
    __tablename__ = "aluno"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(10), unique=True)
    nome: Mapped[str] = mapped_column(String(100))
    # str | None: a coluna aceita NULL (sem o None, o modelo diz que ela é NOT NULL)
    email: Mapped[str | None] = mapped_column(String(120), unique=True)
    data_ingresso: Mapped[date]
    # A coluna da chave estrangeira guarda o id do curso...
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"))

    # ...e o relationship devolve o objeto Curso desse id.
    curso: Mapped[Curso] = relationship(back_populates="alunos")
    matriculas: Mapped[list[Matricula]] = relationship(back_populates="aluno")

    def __repr__(self) -> str:
        return f"Aluno({self.matricula!r}, {self.nome!r})"
