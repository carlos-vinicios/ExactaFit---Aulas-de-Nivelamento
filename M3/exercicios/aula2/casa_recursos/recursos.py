"""Aula 2, atividade para casa: classes, decoradores e geradores.

Complete os TODO na ordem 1, 2 e 3. Depois de cada um, rode o arquivo a partir da pasta
aula-python e compare com a saída esperada:

    python exercicios/aula2/casa_recursos/recursos.py

Confira também os tipos com: mypy exercicios/aula2/casa_recursos/recursos.py

Saída esperada com os três TODO prontos:

    1) Classe Turma
       Turma('CC101', 4 alunos)
       Ana Beatriz, Bruno Costa, Carla Mendes, Diego Ramos
    2) Decorador validar_notas
       media(7, 8) = 7.5
       media(7, 11) recusada: nota fora de 0 a 10: 11
    3) Gerador acima_de
       Ana Beatriz      8.17
       Carla Mendes     9.83

O dataclass Aluno, com a média como propriedade, e a lista ALUNOS já estão prontos.
"""

from collections.abc import Callable, Iterator
from dataclasses import dataclass


# Pronto: o aluno e os dados -----------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Aluno:
    nome: str
    notas: tuple[float, ...]

    @property
    def media(self) -> float:
        return sum(self.notas) / len(self.notas)


ALUNOS = [
    Aluno("Ana Beatriz", (7.0, 9.5, 8.0)),
    Aluno("Bruno Costa", (5.0, 6.0, 4.5)),
    Aluno("Carla Mendes", (9.5, 10.0, 10.0)),
    Aluno("Diego Ramos", (3.0, 4.5, 5.0)),
]


# 1) Classe com métodos especiais -------------------------------------------------------
class Turma:
    """Uma turma com código e alunos.

    len(turma) devolve a quantidade de alunos, `for aluno in turma` percorre os alunos e
    print(turma) mostra, por exemplo, Turma('CC101', 4 alunos).
    """

    def __init__(self, codigo: str, alunos: list[Aluno]) -> None:
        raise NotImplementedError("TODO 1: guarde codigo e alunos no objeto")

    def __len__(self) -> int:
        raise NotImplementedError("TODO 1: __len__")

    def __iter__(self) -> Iterator[Aluno]:
        raise NotImplementedError("TODO 1: __iter__")

    def __repr__(self) -> str:
        raise NotImplementedError("TODO 1: __repr__")


# 2) Decorador ---------------------------------------------------------------------------
def validar_notas(funcao: Callable[..., float]) -> Callable[..., float]:
    """Decorador: antes de chamar `funcao`, confere se todos os argumentos estão entre 0 e 10.

    Se algum estiver fora, levanta ValueError("nota fora de 0 a 10: <valor>") e não chama a
    função. Na função interna, use @wraps(funcao), importado de functools.
    """
    # TODO 2: hoje o decorador devolve a função sem mudança, e a nota 11 passa.
    return funcao


@validar_notas
def media(*notas: float) -> float:
    return sum(notas) / len(notas)


# 3) Gerador -----------------------------------------------------------------------------
def acima_de(alunos: list[Aluno], minimo: float) -> Iterator[tuple[str, float]]:
    """Gera (nome, média) dos alunos com média >= minimo, na ordem da lista. Use yield."""
    raise NotImplementedError("TODO 3")


# Pronto: execução -----------------------------------------------------------------------
def main() -> None:
    print("1) Classe Turma")
    try:
        turma = Turma("CC101", ALUNOS)
        print(f"   {turma!r}")
        print("   " + ", ".join(aluno.nome for aluno in turma))
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")

    print("2) Decorador validar_notas")
    print(f"   media(7, 8) = {media(7, 8)}")
    try:
        print(f"   media(7, 11) = {media(7, 11)}")
    except ValueError as erro:
        print(f"   media(7, 11) recusada: {erro}")

    print("3) Gerador acima_de")
    try:
        for nome, valor in acima_de(ALUNOS, 8.0):
            print(f"   {nome:<16} {valor:.2f}")
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")


if __name__ == "__main__":
    main()
