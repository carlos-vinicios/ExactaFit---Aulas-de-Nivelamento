"""esquema inicial da escola

Revision ID: 0001
Revises:
Create Date: 2026-10-14
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "curso",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("sigla", sa.String(10), nullable=False, unique=True),
        sa.Column("nome", sa.String(100), nullable=False, unique=True),
    )
    op.create_table(
        "aluno",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("matricula", sa.String(10), nullable=False, unique=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("email", sa.String(120), unique=True),
        sa.Column("data_ingresso", sa.Date, nullable=False),
        sa.Column("curso_id", sa.Integer, sa.ForeignKey("curso.id"), nullable=False),
    )
    op.create_table(
        "professor",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("email", sa.String(120), nullable=False, unique=True),
    )
    op.create_table(
        "disciplina",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column("codigo", sa.String(10), nullable=False, unique=True),
        sa.Column("nome", sa.String(100), nullable=False),
        sa.Column("carga_horaria", sa.Integer, nullable=False),
        sa.Column("curso_id", sa.Integer, sa.ForeignKey("curso.id"), nullable=False),
        sa.CheckConstraint("carga_horaria > 0", name="ck_disciplina_carga_positiva"),
    )
    op.create_table(
        "turma",
        sa.Column("id", sa.Integer, sa.Identity(), primary_key=True),
        sa.Column(
            "disciplina_id", sa.Integer, sa.ForeignKey("disciplina.id"), nullable=False
        ),
        sa.Column(
            "professor_id", sa.Integer, sa.ForeignKey("professor.id"), nullable=False
        ),
        sa.Column("semestre", sa.String(6), nullable=False),
        sa.UniqueConstraint(
            "disciplina_id", "semestre", name="uq_turma_disciplina_semestre"
        ),
    )
    op.create_table(
        "matricula",
        sa.Column(
            "aluno_id",
            sa.Integer,
            sa.ForeignKey("aluno.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("turma_id", sa.Integer, sa.ForeignKey("turma.id"), primary_key=True),
        sa.Column("nota", sa.Numeric(4, 2)),
        sa.CheckConstraint("nota BETWEEN 0 AND 10", name="ck_matricula_nota_0_10"),
    )


def downgrade() -> None:
    # Ordem inversa: quem tem chave estrangeira sai primeiro.
    for tabela in ("matricula", "turma", "disciplina", "professor", "aluno", "curso"):
        op.drop_table(tabela)
