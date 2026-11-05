"""Classe base de todos os modelos.

Os modelos são os mesmos da Aula 5 (M4/modelo_de_dados/modelos), um por arquivo. Quem cria e
altera as tabelas no banco continua sendo o Alembic, nas migrações do M4.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
