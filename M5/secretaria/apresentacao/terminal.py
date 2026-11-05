"""O que é comum a todas as telas: ler os argumentos, mostrar valores e mostrar erros."""

import sys
from collections.abc import Callable
from typing import NoReturn

from secretaria.dominio import Linha
from secretaria.erros import (
    BancoIndisponivelError,
    NaoEncontradoError,
    RegraDeNegocioError,
)


def sair(mensagem: str) -> NoReturn:
    """Mostra a mensagem no terminal de erros e encerra o programa."""
    print(mensagem, file=sys.stderr)
    sys.exit(1)


def ler_argumentos(*nomes: str) -> list[str]:
    """Os valores digitados depois do nome do módulo, um para cada nome."""
    valores = sys.argv[1:]
    if len(valores) != len(nomes):
        modulo = sys.modules["__main__"].__spec__
        comando = f"python -m {modulo.name}" if modulo else "python"
        sair(f"uso: {comando} {' '.join(nome.upper() for nome in nomes)}")
    return valores


def numero(texto: str, campo: str) -> float:
    """Converte o texto digitado num float; aceita vírgula (8,5)."""
    try:
        return float(texto.replace(",", "."))
    except ValueError:
        sair(f"erro: {campo} deve ser um número, como 8.5")


def executar(tela: Callable[[], None]) -> None:
    """Roda uma tela e transforma os erros das outras camadas em mensagens curtas."""
    try:
        tela()
    except NaoEncontradoError as erro:
        sair(f"erro: {erro}")
    except RegraDeNegocioError as erro:
        sair(f"não permitido: {erro}")
    except BancoIndisponivelError as erro:
        sair(f"banco indisponível: {erro}")
    except NotImplementedError as falta:  # enquanto houver TODO no código
        sair(f"ainda não implementado ({falta})")


def formatar_nota(valor: float | None) -> str:
    return "-" if valor is None else f"{valor:.1f}"


def formatar_media(valor: float | None) -> str:
    return "sem notas lançadas" if valor is None else f"{valor:.2f}"


def quantos(n: int, singular: str, plural: str) -> str:
    return f"{n} {singular if n == 1 else plural}"


def descrever(linha: Linha) -> str:
    """Aluno e turma de uma linha, como 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2)."""
    m = linha.matricula
    return (
        f"{m.aluno.matricula} {m.aluno.nome}, {m.turma.codigo} {m.turma.disciplina} "
        f"({m.turma.semestre})"
    )
