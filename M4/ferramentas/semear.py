"""Insere os dados de exemplo da escola num banco já migrado pelo Alembic (Aula 5).

Uso, a partir da pasta M4:
    python ferramentas/semear.py           usa DATABASE_URL (padrão: sqlite:///escola.db)
    python ferramentas/semear.py URL       usa a URL informada
"""

import sys

from banco import ERROS_BANCO, semear, url_banco


def main(argumentos: list[str]) -> int:
    if len(argumentos) > 1:
        print("uso: python ferramentas/semear.py [URL]", file=sys.stderr)
        return 2
    url = argumentos[0] if argumentos else url_banco()
    try:
        total = semear(url)
    except ERROS_BANCO as erro:  # conexão recusada ou dados já inseridos
        print(f"erro ao semear {url}: {erro}", file=sys.stderr)
        return 1
    print(f"{total} comandos executados em {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
