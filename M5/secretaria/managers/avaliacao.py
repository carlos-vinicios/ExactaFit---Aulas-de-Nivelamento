"""Regras de avaliação: situação, média e lançamento de nota."""

from collections.abc import Iterable

from secretaria.config import SEMESTRE_ATUAL  # noqa: F401 (usado nas práticas)
from secretaria.dominio import Linha, Matricula, Situacao
from secretaria.erros import RegraDeNegocioError  # noqa: F401 (usado nas práticas)

NOTA_APROVACAO = 6.0


def situacao(nota: float | None) -> Situacao:
    """Sem nota: cursando. Nota a partir de 6: aprovado. Abaixo de 6: reprovado."""
    if nota is None:
        return Situacao.CURSANDO
    return Situacao.APROVADO if nota >= NOTA_APROVACAO else Situacao.REPROVADO


def media(notas: Iterable[float | None]) -> float | None:
    """Média das notas lançadas, com duas casas. None se nenhuma nota foi lançada."""
    lancadas = [nota for nota in notas if nota is not None]
    if not lancadas:
        return None
    return round(sum(lancadas) / len(lancadas), 2)


def classificar(matriculas: Iterable[Matricula]) -> list[Linha]:
    """Uma Linha para cada matrícula, com a situação calculada."""
    return [Linha(m, situacao(m.nota)) for m in matriculas]


def preparar_nota(matricula: Matricula, nota: float) -> float:
    """Regras do lançamento, nesta ordem:

    * a nota vai de 0 a 10;
    * só se lança nota no semestre em andamento (SEMESTRE_ATUAL);
    * a nota é gravada com uma casa decimal (8.46 vira 8.5).

    Regra não atendida: RegraDeNegocioError com uma mensagem clara.
    """
    raise NotImplementedError("TODO Aula 6, Prática 3")
