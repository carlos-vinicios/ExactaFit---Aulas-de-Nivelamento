"""Módulo com as operações. Repare: este print roda no momento do import!"""

print(f"[operacoes] carregado, __name__ = {__name__!r}")


def somar(a: float, b: float) -> float:
    return a + b


def dividir(a: float, b: float) -> float:
    return a / b


if __name__ == "__main__":
    # Só roda quando o arquivo é executado diretamente, nunca no import.
    print("teste rápido:", somar(2, 3), dividir(9, 3))
