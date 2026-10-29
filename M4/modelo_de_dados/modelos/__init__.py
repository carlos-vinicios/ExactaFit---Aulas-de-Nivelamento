"""Os modelos do banco da escola, um por arquivo.

Importar este pacote carrega todos os modelos. Assim o SQLAlchemy conhece todas as classes e
consegue ligar os relacionamentos escritos com nomes (relationship com back_populates):

    from modelo_de_dados.modelos import Aluno, Curso
"""

from .aluno import Aluno
from .base import Base
from .curso import Curso
from .disciplina import Disciplina
from .matricula import Matricula
from .professor import Professor
from .turma import Turma

__all__ = ["Aluno", "Base", "Curso", "Disciplina", "Matricula", "Professor", "Turma"]
