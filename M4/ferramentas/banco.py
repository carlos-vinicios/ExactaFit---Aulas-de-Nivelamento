"""Funções de apoio usadas pelos scripts desta pasta.

Os scripts importam este módulo com `from banco import ...`. Funciona porque, ao rodar
`python ferramentas/sql.py`, o Python coloca a pasta do script em sys.path[0] (Aula 1).
"""

import os
import sqlite3
from pathlib import Path
from typing import Any

import psycopg

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
ESQUEMA = DADOS / "escola_esquema.sql"
CARGA = DADOS / "escola_dados.sql"
URL_PADRAO = "sqlite:///escola.db"
PREFIXOS_POSTGRES = ("postgresql://", "postgresql+psycopg://", "postgres://")
# Erros esperados ao falar com um banco: do SQLite, do PostgreSQL, de arquivo e de SQL incompleto.
ERROS_BANCO = (sqlite3.Error, psycopg.Error, OSError, ValueError)

Resultado = tuple[str, list[str], list[tuple[object, ...]]]


def conectar(caminho: str | Path = ":memory:") -> sqlite3.Connection:
    """Abre uma conexão SQLite com as chaves estrangeiras ligadas."""
    con = sqlite3.connect(caminho)
    con.execute("PRAGMA foreign_keys = ON")  # desligado por padrão no SQLite
    return con


def criar_banco(caminho: str | Path = ":memory:") -> sqlite3.Connection:
    """Cria o banco a partir de dados/escola_esquema.sql e dados/escola_dados.sql."""
    if str(caminho) != ":memory:":
        Path(caminho).unlink(missing_ok=True)
    con = conectar(caminho)
    with con:
        con.executescript(ESQUEMA.read_text(encoding="utf-8"))
        con.executescript(CARGA.read_text(encoding="utf-8"))
    return con


def url_banco() -> str:
    """URL do banco usada pelo semear.py e pelo Alembic: DATABASE_URL ou o SQLite padrão."""
    return os.environ.get("DATABASE_URL", URL_PADRAO)


def conectar_url(banco: str) -> Any:
    """Conecta num arquivo SQLite, numa URL sqlite:/// ou numa URL do PostgreSQL."""
    if banco.startswith(PREFIXOS_POSTGRES):
        return psycopg.connect(banco.replace("postgresql+psycopg://", "postgresql://"))
    return conectar(banco.removeprefix("sqlite:///"))


def executar_arquivo(con: Any, texto: str, continuar: bool = False) -> list[Resultado]:
    """Executa os comandos de um script SQL, um por vez, e confirma no final.

    Devolve, para cada comando que retorna linhas (SELECT, RETURNING), o comando, os nomes
    das colunas e as linhas. Com continuar=True, um comando com erro não interrompe o
    script: o erro entra na lista como uma coluna "erro", e cada comando sem linhas entra
    como uma coluna "ok" com o número de linhas afetadas.
    """
    resultados: list[Resultado] = []
    comando = ""
    for linha in texto.splitlines(keepends=True):
        comando += linha
        if not sqlite3.complete_statement(comando):
            continue
        limpo = "\n".join(
            t for t in comando.splitlines() if not t.strip().startswith("--")
        ).strip()
        try:
            cur = con.execute(comando)
        except ERROS_BANCO as erro:
            if not continuar:
                raise
            con.rollback()  # no PostgreSQL, um erro invalida a transação em andamento
            mensagem = str(erro).strip().splitlines()[0]
            resultados.append(
                (limpo, ["erro"], [(f"{type(erro).__name__}: {mensagem}",)])
            )
        else:
            if cur.description:
                colunas = [d[0] for d in cur.description]
                resultados.append((limpo, colunas, cur.fetchall()))
            elif continuar:
                resultados.append(
                    (limpo, ["ok"], [(f"{max(cur.rowcount, 0)} linha(s) afetada(s)",)])
                )
            if continuar:
                con.commit()
        comando = ""
    resto = [
        t for t in comando.splitlines() if t.strip() and not t.strip().startswith("--")
    ]
    if resto:
        raise ValueError(
            f"comando incompleto (falta ponto e vírgula?): {resto[0].strip()[:60]}"
        )
    con.commit()
    return resultados


def formatar_tabela(colunas: list[str], linhas: list[tuple[object, ...]]) -> str:
    """Formata linhas como tabela de texto, no estilo do psql."""
    textos = [["NULL" if v is None else str(v) for v in linha] for linha in linhas]
    larguras = [
        max([len(c)] + [len(t[i]) for t in textos]) for i, c in enumerate(colunas)
    ]
    cab = " | ".join(
        c.ljust(w) for c, w in zip(colunas, larguras, strict=True)
    ).rstrip()
    sep = "-+-".join("-" * w for w in larguras)
    corpo = [
        " | ".join(v.ljust(w) for v, w in zip(t, larguras, strict=True)).rstrip()
        for t in textos
    ]
    n = len(linhas)
    return "\n".join([cab, sep, *corpo, f"({n} linha{'s' if n != 1 else ''})"])


def comandos_sql(texto: str) -> list[str]:
    """Separa um arquivo SQL simples (sem ; dentro de textos) em comandos."""
    sem_comentarios = "\n".join(
        t for t in texto.splitlines() if not t.lstrip().startswith("--")
    )
    return [c.strip() for c in sem_comentarios.split(";") if c.strip()]


def semear(banco: str) -> int:
    """Insere os dados de exemplo num banco já migrado, numa única transação."""
    comandos = comandos_sql(CARGA.read_text(encoding="utf-8"))
    con = conectar_url(banco)
    try:
        for comando in comandos:
            con.execute(comando)
        con.commit()  # tudo ou nada: um erro antes daqui descarta os INSERTs
    finally:
        con.close()
    return len(comandos)
