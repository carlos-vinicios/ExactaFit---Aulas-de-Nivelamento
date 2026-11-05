"""Schemas de entrada com Pydantic (Aula 7).

Um schema descreve o formato de um pedido: quais campos, de que tipo, em que faixa. A
apresentação monta o schema com o que a pessoa digitou; se algo estiver fora do formato, o
Pydantic levanta ValidationError com a lista de problemas, antes de o pedido chegar ao serviço.

Formato é diferente de regra de negócio: "a nota vai de 0 a 10" é formato e fica aqui;
"só se lança nota no semestre em andamento" depende do banco e fica no manager.
"""

import re
from typing import Annotated

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, Field  # noqa: F401 (usado nas práticas)


def _matricula(valor: str) -> str:
    if not re.fullmatch(r"\d{7}", valor):
        raise ValueError("deve ter 7 dígitos, como 2025001")
    return valor


def _codigo(valor: str) -> str:
    if not re.fullmatch(r"[A-Z]{2}\d{3}", valor):
        raise ValueError("deve ter 2 letras e 3 dígitos, como CC201")
    return valor


def _semestre(valor: str) -> str:
    if not re.fullmatch(r"\d{4}\.[12]", valor):
        raise ValueError("deve estar no formato AAAA.1 ou AAAA.2, como 2026.2")
    return valor


def _maiusculas(valor: object) -> object:
    return valor.strip().upper() if isinstance(valor, str) else valor


def _virgula(valor: object) -> object:
    return valor.replace(",", ".") if isinstance(valor, str) else valor


MatriculaAluno = Annotated[str, AfterValidator(_matricula)]
CodigoDisciplina = Annotated[str, BeforeValidator(_maiusculas), AfterValidator(_codigo)]
Semestre = Annotated[str, AfterValidator(_semestre)]


class LancamentoNota(BaseModel):
    """Pedido de lançamento de nota.

    TODO Aula 7, Prática 1: declare os campos
    * matricula, codigo e semestre, com os tipos MatriculaAluno, CodigoDisciplina e Semestre;
    * nota: float de 0 a 10 que aceita vírgula. Dica: crie, ao lado dos outros tipos,
      Nota = Annotated[float, BeforeValidator(_virgula), Field(ge=0, le=10)]
    """

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)


class NovaMatricula(BaseModel):
    """Pedido de matrícula (e de cancelamento, no desafio).

    TODO Aula 7, Prática 3: declare os campos matricula, codigo e semestre.
    """

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)
