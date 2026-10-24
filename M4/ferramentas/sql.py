"""Executa arquivos .sql num banco e mostra o resultado de cada consulta.

Uso, a partir da pasta M4:
    python ferramentas/sql.py BANCO ARQUIVO.sql [OUTRO.sql ...]
    python ferramentas/sql.py BANCO ARQUIVO.sql --continuar CONFERENCIA.sql

BANCO pode ser:
    escola.db                 arquivo SQLite (criado vazio se não existir)
    :memory:                  SQLite em memória, apagado no fim (bom para conferir esquemas)
    postgresql://usuario:senha@localhost:5432/banco

Os arquivos rodam em ordem, na mesma conexão, e o script para no primeiro erro. Os arquivos
que vêm depois de --continuar rodam de outro jeito: cada comando aparece na saída com o
resultado, inclusive os erros, e o script segue para o próximo comando.
No SQLite, as chaves estrangeiras são ligadas (PRAGMA foreign_keys = ON).
"""

import sys
from pathlib import Path

from banco import ERROS_BANCO, conectar_url, executar_arquivo, formatar_tabela

USO = "uso: python ferramentas/sql.py BANCO ARQUIVO.sql [...] [--continuar ARQUIVO.sql ...]"


def main(argumentos: list[str]) -> int:
    if len(argumentos) < 2 or argumentos[0].startswith("-"):
        print(USO, file=sys.stderr)
        return 2
    banco, *resto = argumentos
    textos: list[
        tuple[str, bool]
    ] = []  # (conteúdo do arquivo, continuar depois de erro?)
    continuar = False
    for arquivo in resto:
        if arquivo == "--continuar":
            continuar = True
            continue
        if arquivo.startswith("-"):
            print(USO, file=sys.stderr)
            return 2
        try:
            textos.append((Path(arquivo).read_text(encoding="utf-8"), continuar))
        except FileNotFoundError:
            print(f"erro: arquivo {arquivo} não encontrado", file=sys.stderr)
            return 1
    if not textos:
        print(USO, file=sys.stderr)
        return 2
    try:
        con = conectar_url(banco)
    except ERROS_BANCO as erro:
        print(f"erro ao conectar em {banco}: {erro}", file=sys.stderr)
        return 1
    try:
        for texto, continuar in textos:
            mostrar(executar_arquivo(con, texto, continuar), continuar)
    except ERROS_BANCO as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    finally:
        con.close()
    return 0


def mostrar(
    resultados: list[tuple[str, list[str], list[tuple[object, ...]]]], continuar: bool
) -> None:
    for comando, colunas, linhas in resultados:
        if continuar:
            print(f"> {' '.join(comando.split())}")
        if colunas == ["ok"]:
            print(f"ok: {linhas[0][0]}")
        elif colunas == ["erro"]:
            print(f"ERRO {linhas[0][0]}")
        else:
            print(formatar_tabela(colunas, linhas))
        print()
    if not resultados:
        print("ok (nenhum comando devolveu linhas)")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
