"""Cria um banco SQLite com o esquema e os dados da escola (Aulas 3 e 4).

Uso, a partir da pasta M4:
    python ferramentas/criar_banco.py              cria (ou recria) escola.db
    python ferramentas/criar_banco.py outro.db     cria outro arquivo
"""

import sys

from banco import criar_banco


def main(argumentos: list[str]) -> int:
    if len(argumentos) > 1:
        print("uso: python ferramentas/criar_banco.py [ARQUIVO.db]", file=sys.stderr)
        return 2
    arquivo = argumentos[0] if argumentos else "escola.db"
    criar_banco(arquivo).close()
    print(f"banco criado: {arquivo}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
