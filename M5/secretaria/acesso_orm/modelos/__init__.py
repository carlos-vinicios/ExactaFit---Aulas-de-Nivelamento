"""Os modelos do banco da escola, um por arquivo (os mesmos da Aula 5).

Ficam dentro da camada de acesso a dados: nenhuma outra camada importa este pacote.
"""

from .aluno import Aluno
from .base import Base
from .curso import Curso
from .disciplina import Disciplina
from .matricula import Matricula
from .professor import Professor
from .turma import Turma

__all__ = ["Aluno", "Base", "Curso", "Disciplina", "Matricula", "Professor", "Turma"]
