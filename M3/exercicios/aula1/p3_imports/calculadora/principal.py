"""Ponto de entrada da calculadora (Aula 1, Prática 3).

Experimente, a partir da pasta exercicios/aula1/p3_imports/:
    python calculadora/principal.py
    python -m calculadora.principal
Um funciona, o outro quebra. Por quê?
"""

import sys

print(f"[principal] __name__ = {__name__!r}")
print(f"[principal] sys.path[0] = {sys.path[0]!r}")

from exercicios.aula1.p3_imports.calculadora.operacoes import (
    somar,  # <- o problema mora aqui
)

print("2 + 3 =", somar(2, 3))
