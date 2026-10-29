"""Modelo da tabela disciplina."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .curso import Curso
    from .turma import Turma


class Disciplina(Base):
    __tablename__ = "disciplina"

    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[str] = mapped_column(String(10), unique=True)
    nome: Mapped[str] = mapped_column(String(100))
    carga_horaria: Mapped[int]
    curso_id: Mapped[int] = mapped_column(ForeignKey("curso.id"))

    curso: Mapped[Curso] = relationship(back_populates="disciplinas")
    turmas: Mapped[list[Turma]] = relationship(back_populates="disciplina")

    def __repr__(self) -> str:
        return f"Disciplina({self.codigo!r}, {self.nome!r})"
