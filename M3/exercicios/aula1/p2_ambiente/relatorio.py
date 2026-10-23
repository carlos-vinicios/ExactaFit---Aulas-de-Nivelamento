"""Aula 1, Prática 2: relatório da turma em quatro etapas.

Cada etapa tem UM defeito. Encontre e corrija os quatro usando as ferramentas do
ambiente (ruff e mypy, instalados pelo requirements-dev.txt) e o depurador do VS
Code. Confira o resultado comparando a saída com a saída esperada abaixo.

Execute a partir da pasta aula-python, com o ambiente virtual ativo:
    python exercicios/aula1/p2_ambiente/relatorio.py

Saída esperada depois das correções: os 10 alunos de notas.csv, de Ana Beatriz (8.17,
aprovado) a João Pedro (5.33, reprovado), e a linha "Média da turma: 6.60".
"""

import csv
from pathlib import Path

ARQUIVO = Path(__file__).with_name("notas.csv")
NOTA_APROVACAO = 7.0


# Etapa 1: ler as linhas do arquivo, sem o cabeçalho
def ler_linhas(caminho: Path) -> list[list[str]]:
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        linhas = list(csv.reader(arquivo))
    return linhas[2:]


# Etapa 2: separar o nome e converter as notas em números
def converter(linha: list[str]) -> tuple[str, list[float]]:
    nome = linha[0].strip()
    notas = [float(valor) for valor in linha[1:]]
    return nome, notass


# Etapa 3: calcular a média e a situação de cada aluno
def media(notas: list[float]) -> float:
    return sum(notas) / len(notas)


def situacao(valor: float) -> str:
    return "aprovado" if valor >= NOTA_APROVACAO else "reprovado"


def avaliar(linhas: list[list[str]]) -> list[tuple[str, float, str]]:
    avaliacoes = []
    for linha in linhas:
        nome, notas = converter(linha)
        valor = media(linha[1:])
        avaliacoes.append((nome, valor, situacao(valor)))
    return avaliacoes


# Etapa 4: calcular a média da turma
def media_da_turma(avaliacoes: list[tuple[str, float, str]]) -> float:
    total = 0.0
    for _nome, valor, _situacao in avaliacoes:
        total = valor
    return total / len(avaliacoes)


def main() -> None:
    linhas = ler_linhas(ARQUIVO)
    avaliacoes = avaliar(linhas)
    for nome, valor, sit in avaliacoes:
        print(f"{nome:<16} {valor:5.2f}  {sit}")
    print(f"Média da turma: {media_da_turma(avaliacoes):.2f}")


if __name__ == "__main__":
    main()
