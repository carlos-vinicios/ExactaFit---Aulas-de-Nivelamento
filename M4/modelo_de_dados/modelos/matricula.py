"""Modelo da tabela matricula: a tabela associativa da relação N:N entre aluno e turma."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .aluno import Aluno
    from .turma import Turma


class Matricula(Base):
    __tablename__ = "matricula"

    # Chave primária composta: as duas colunas juntas identificam a matrícula.
    aluno_id: Mapped[int] = mapped_column(ForeignKey("aluno.id"), primary_key=True)
    turma_id: Mapped[int] = mapped_column(ForeignKey("turma.id"), primary_key=True)
    # asdecimal=False: a nota chega como float, e não como Decimal (que o PostgreSQL devolveria)
    nota: Mapped[float | None] = mapped_column(Numeric(4, 2, asdecimal=False))

    aluno: Mapped[Aluno] = relationship(back_populates="matriculas")
    turma: Mapped[Turma] = relationship(back_populates="matriculas")

    def __repr__(self) -> str:
        return f"Matricula({self.aluno.matricula!r}, {self.turma!r}, nota={self.nota})"
