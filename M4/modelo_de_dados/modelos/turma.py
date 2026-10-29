"""Modelo da tabela turma."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .disciplina import Disciplina
    from .matricula import Matricula
    from .professor import Professor


class Turma(Base):
    __tablename__ = "turma"

    id: Mapped[int] = mapped_column(primary_key=True)
    disciplina_id: Mapped[int] = mapped_column(ForeignKey("disciplina.id"))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professor.id"))
    semestre: Mapped[str] = mapped_column(String(6))

    disciplina: Mapped[Disciplina] = relationship(back_populates="turmas")
    professor: Mapped[Professor] = relationship(back_populates="turmas")
    matriculas: Mapped[list[Matricula]] = relationship(back_populates="turma")

    def __repr__(self) -> str:
        return f"Turma({self.disciplina.codigo!r}, {self.semestre!r})"
