"""Classe base de todos os modelos.

Toda classe que herda de Base vira um modelo: o SQLAlchemy guarda a descrição da tabela dela em
Base.metadata. Quem cria e altera as tabelas no banco continua sendo o Alembic (pasta migracoes/).
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
