"""Aula 2, Prática 1: tipos e funções.

Complete as funções marcadas com TODO, na ordem 1, 2 e 3 (a 4 é bônus). Depois de cada
uma, rode o arquivo a partir da pasta aula-python e compare com a saída esperada:

    python exercicios/aula2/p1_funcoes/funcoes.py

Confira também os tipos com: mypy exercicios/aula2/p1_funcoes/funcoes.py

Saída esperada com as quatro funções prontas:

    1) Nomes normalizados
       Ana Beatriz, Bruno Costa, Carla Mendes, Diego Ramos, Elisa Fonseca,
       Fábio Nunes, Gabriela Lima, Heitor Souza, Íris Carvalho, João Pedro
    2) Três maiores médias
       Carla Mendes     9.83
       Gabriela Lima    8.50
       Ana Beatriz      8.17
    3) Alunos por situação
       aprovado: Ana Beatriz, Carla Mendes, Fábio Nunes, Gabriela Lima, Íris Carvalho
       recuperação: Bruno Costa, Elisa Fonseca, João Pedro
       reprovado: Diego Ramos, Heitor Souza
    4) Bônus: registrar_nota
       [7]
       [9]

A primeira parte do arquivo já está pronta: os tipos Situacao e Aluno, as funções
media() e situacao() e a leitura de turma.json. Use-as nas suas funções.
"""

import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

ARQUIVO = Path(__file__).with_name("turma.json")
NOTA_APROVACAO = 7.0
NOTA_RECUPERACAO = 5.0


# Pronto: tipos e funções de apoio ----------------------------------------------
class Situacao(StrEnum):
    APROVADO = "aprovado"
    RECUPERACAO = "recuperação"
    REPROVADO = "reprovado"


@dataclass(frozen=True, slots=True)
class Aluno:
    nome: str
    notas: tuple[float, ...]


def media(notas: Sequence[float]) -> float:
    """Média simples das notas.

    >>> media([6, 8])
    7.0
    >>> media([5.5, 6.0, 4.5])
    5.333333333333333
    """
    return sum(notas) / len(notas)


def situacao(
    media_final: float,
    *,
    aprovacao: float = NOTA_APROVACAO,
    recuperacao: float = NOTA_RECUPERACAO,
) -> Situacao:
    """Classifica a média: >= aprovacao, >= recuperacao ou abaixo.

    >>> situacao(7.0)
    <Situacao.APROVADO: 'aprovado'>
    >>> situacao(6.0, aprovacao=6.0)
    <Situacao.APROVADO: 'aprovado'>
    """
    if media_final >= aprovacao:
        return Situacao.APROVADO
    if media_final >= recuperacao:
        return Situacao.RECUPERACAO
    return Situacao.REPROVADO


def carregar_turma(caminho: Path) -> list[Aluno]:
    """Lê o JSON da turma: uma lista de objetos com "nome" e "notas"."""
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return [Aluno(item["nome"], tuple(item["notas"])) for item in dados]


# 1) Strings --------------------------------------------------------------------
def normalizar_nome(nome: str) -> str:
    """Remove espaços extras e deixa cada palavra com inicial maiúscula.

    "  ana   BEATRIZ " deve virar "Ana Beatriz".
    Dica: str.split() sem argumentos já descarta espaços repetidos.
    """
    raise NotImplementedError("TODO 1")


# 2) Coleções, sorted e key= ----------------------------------------------------
def top_n(alunos: Iterable[Aluno], n: int = 3) -> list[tuple[str, float]]:
    """Os `n` alunos de maior média, como (nome, média), maior primeiro.

    Empate na média: ordem alfabética do nome. Se n for negativo, levante ValueError.
    Dica: sorted(..., key=lambda par: (-par[1], par[0]))
    """
    raise NotImplementedError("TODO 2")


# 3) Dicionários ----------------------------------------------------------------
def agrupar_por_situacao(alunos: Iterable[Aluno]) -> dict[Situacao, list[str]]:
    """Agrupa os NOMES por situação, usando media() e situacao().

    Regras: toda situação aparece como chave (mesmo com lista vazia),
    e os nomes de cada lista ficam em ordem alfabética.
    Dica: comece com {s: [] for s in Situacao}.
    """
    raise NotImplementedError("TODO 3")


# 4) Bônus: a armadilha do argumento padrão mutável ------------------------------
def registrar_nota(nota: float, historico: list[float] = []) -> list[float]:
    """Adiciona `nota` ao histórico e devolve o histórico.

    Esta função TEM UM DEFEITO: rode o arquivo e veja a seção 4 da saída.
    Corrija para que cada chamada sem histórico comece com uma lista nova.
    """
    historico.append(nota)
    return historico


# Pronto: execução da prática -----------------------------------------------------
def main() -> None:
    alunos = carregar_turma(ARQUIVO)

    print("1) Nomes normalizados")
    try:
        alunos = [Aluno(normalizar_nome(a.nome), a.notas) for a in alunos]
        nomes = [a.nome for a in alunos]
        print("   " + ", ".join(nomes[:5]) + ",")
        print("   " + ", ".join(nomes[5:]))
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")

    print("2) Três maiores médias")
    try:
        for nome, valor in top_n(alunos):
            print(f"   {nome:<16} {valor:.2f}")
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")

    print("3) Alunos por situação")
    try:
        for chave, grupo in agrupar_por_situacao(alunos).items():
            print(f"   {chave}: {', '.join(grupo)}")
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")

    print("4) Bônus: registrar_nota")
    print(f"   {registrar_nota(7)}")
    print(f"   {registrar_nota(9)}")


if __name__ == "__main__":
    main()
