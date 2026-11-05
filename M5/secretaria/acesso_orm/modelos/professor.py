"""Modelo da tabela professor."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .turma import Turma


class Professor(Base):
    __tablename__ = "professor"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)

    turmas: Mapped[list[Turma]] = relationship(back_populates="professor")

    def __repr__(self) -> str:
        return f"Professor({self.nome!r})"
