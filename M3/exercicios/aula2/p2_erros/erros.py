"""Aula 2, Prática 2: tratamento de erros.

Rode a partir da pasta aula-python e compare com a saída esperada:

    python exercicios/aula2/p2_erros/erros.py

Contexto: ler_turma() já está pronta e é ESTRITA: para no primeiro erro (seção 0 da
saída). Para a secretaria, é mais útil ver TODOS os problemas do arquivo de uma vez.
Complete as funções marcadas com TODO, na ordem A e B.

Os arquivos de exemplo estão em exercicios/aula2/p2_erros/dados/. O CSV segue o formato
do Excel em português: `;` entre colunas e `,` nos decimais.

Saída esperada com as duas funções prontas:

    0) Leitura estrita de turma_com_erros.csv
       erro: linha 3: coluna 'n2' vazia
    A) Leitura tolerante de turma_com_erros.csv
       válidos: Ana Beatriz, Carla Mendes, Fábio Nunes
       linha 3: coluna 'n2' vazia
       linha 5: n1='dez': could not convert string to float: 'dez'
       linha 7: n3='11': nota 11.0 fora do intervalo de 0 a 10
       linha 8: matrícula e nome são obrigatórios
       linha 10: coluna 'n3' vazia
    B) Configurações
       config.json: aprovação 6.0, recuperação 4.0
       nao_existe.json: aprovação 7.0, recuperação 5.0
       config_quebrada.json: erro: config_quebrada.json não é um JSON válido
          causa: JSONDecodeError
       config_tipo_errado.json: erro: nota_aprovacao deve ser número, veio 'seis'
"""

import csv
import json  # noqa: F401  (você vai precisar dele na função B)
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

DADOS = Path(__file__).with_name("dados")
CONFIG_PADRAO: dict[str, float] = {"nota_aprovacao": 7.0, "nota_recuperacao": 5.0}


# Pronto: exceções do exercício -------------------------------------------------
class TurmaError(Exception):
    """Base de todos os erros deste exercício."""


class LinhaInvalidaError(TurmaError):
    """Uma linha do CSV não pôde ser convertida em Aluno."""

    def __init__(self, numero_linha: int, motivo: str) -> None:
        super().__init__(f"linha {numero_linha}: {motivo}")
        self.numero_linha = numero_linha


class ConfigInvalidaError(TurmaError):
    """O arquivo de configuração existe, mas não dá para usar."""


# Pronto: leitura do CSV ----------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Aluno:
    matricula: str
    nome: str
    notas: tuple[float, ...]


def converter_nota(texto: str) -> float:
    """'7,5' -> 7.5. Levanta ValueError se não for número ou estiver fora de 0 a 10."""
    valor = float(texto.strip().replace(",", "."))
    if not 0 <= valor <= 10:
        raise ValueError(f"nota {valor} fora do intervalo de 0 a 10")
    return valor


def converter_linha(linha: Mapping[str, str | None], numero_linha: int) -> Aluno:
    """Transforma uma linha do DictReader em Aluno, ou levanta LinhaInvalidaError."""
    matricula = (linha.get("matricula") or "").strip()
    nome = (linha.get("nome") or "").strip()
    if not matricula or not nome:
        raise LinhaInvalidaError(numero_linha, "matrícula e nome são obrigatórios")
    notas: list[float] = []
    for coluna in [c for c in linha if c not in ("matricula", "nome")]:
        bruto = linha[coluna]
        if bruto is None or not bruto.strip():
            raise LinhaInvalidaError(numero_linha, f"coluna {coluna!r} vazia")
        try:
            notas.append(converter_nota(bruto))
        except ValueError as erro:
            raise LinhaInvalidaError(
                numero_linha, f"{coluna}={bruto!r}: {erro}"
            ) from erro
    return Aluno(matricula, nome, tuple(notas))


def iterar_linhas(caminho: Path) -> Iterator[tuple[int, dict[str, str | None]]]:
    """Gera (número_da_linha, linha). A linha 1 é o cabeçalho."""
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        for linha in leitor:
            yield leitor.line_num, linha


def ler_turma(caminho: Path) -> list[Aluno]:
    """Leitura ESTRITA: para no primeiro problema."""
    return [converter_linha(linha, numero) for numero, linha in iterar_linhas(caminho)]


# A) Coletar erros em vez de parar no primeiro -----------------------------------
def ler_turma_tolerante(caminho: Path) -> tuple[list[Aluno], list[LinhaInvalidaError]]:
    """Lê todas as linhas válidas e COLETA os erros das inválidas.

    Use iterar_linhas() e converter_linha(). Capture SÓ LinhaInvalidaError.
    Um FileNotFoundError deve continuar subindo: não é problema de uma linha,
    é do arquivo todo.
    """
    raise NotImplementedError("TODO A")


# B) Tradução de exceções com `raise ... from` ------------------------------------
def abrir_config(caminho: Path) -> dict[str, float]:
    """Lê um JSON de configuração e devolve CONFIG_PADRAO atualizado com ele.

    Regras:
    - arquivo não existe        -> devolve uma CÓPIA de CONFIG_PADRAO (não é erro)
    - JSON malformado           -> ConfigInvalidaError, encadeando o erro original
                                   (except json.JSONDecodeError as e: raise ... from e)
    - valor que não é número    -> ConfigInvalidaError dizendo qual chave
    - chave desconhecida        -> ignore

    Dicas: abra com open(caminho, encoding="utf-8") e leia com json.load(arquivo).
    Cuidado: True é instância de int em Python, e true não é uma nota.
    """
    raise NotImplementedError("TODO B")


# Pronto: execução da prática -----------------------------------------------------
def main() -> None:
    print("0) Leitura estrita de turma_com_erros.csv")
    try:
        ler_turma(DADOS / "turma_com_erros.csv")
    except TurmaError as erro:
        print(f"   erro: {erro}")

    print("A) Leitura tolerante de turma_com_erros.csv")
    try:
        alunos, erros = ler_turma_tolerante(DADOS / "turma_com_erros.csv")
        print(f"   válidos: {', '.join(aluno.nome for aluno in alunos)}")
        for problema in erros:
            print(f"   {problema}")
    except NotImplementedError as falta:
        print(f"   ainda não implementada ({falta})")

    print("B) Configurações")
    for nome in [
        "config.json",
        "nao_existe.json",
        "config_quebrada.json",
        "config_tipo_errado.json",
    ]:
        try:
            config = abrir_config(DADOS / nome)
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")
            break
        except ConfigInvalidaError as erro:
            print(f"   {nome}: erro: {erro}")
            if erro.__cause__ is not None:
                print(f"      causa: {type(erro.__cause__).__name__}")
        else:
            print(
                f"   {nome}: aprovação {config['nota_aprovacao']}, recuperação {config['nota_recuperacao']}"
            )


if __name__ == "__main__":
    main()
