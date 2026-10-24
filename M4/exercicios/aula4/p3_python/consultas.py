"""Aula 4, Prática 3: SQL a partir do Python com o módulo sqlite3.

Complete as quatro funções marcadas com TODO. Regras:

* Use SEMPRE parâmetros (?) para os valores que vêm de fora. Nunca monte SQL com f-string,
  + ou format: isso abre a porta para injeção de SQL. A seção "injeção" da saída tenta isso.
* Cada função recebe uma conexão aberta; não abra nem feche conexões dentro dela.

Rode a partir da pasta M4 e compare com a saída esperada:

    python exercicios/aula4/p3_python/consultas.py

O programa cria um banco novo, numa pasta temporária, a cada execução: o escola.db não muda.

Saída esperada com as quatro funções prontas:

    1) buscar_aluno
       2025001: Ana Beatriz Souza, CC, ana.souza@aluno.escola.edu
       1999999: None
       injeção: None
    2) alunos_do_curso
       ES: 15 alunos; os três primeiros: Felipe Azevedo, Giovana Batista, Henrique Coelho
       XX: []
       injeção: []
    3) media_por_disciplina
       2026.1: 12 disciplinas, de CC201 (7.77) a ES101 (5.99)
       2026.2: []
    4) lancar_nota
       8.5 em CC201 (2026.2): gravada; lida de outra conexão: 8.5
       10.5: ValueError: nota fora do intervalo de 0 a 10: 10.5
       ES101 (2026.1): ValueError: 2025001 não está matriculado em ES101 (2026.1)
       injeção: ValueError: 2025001' OR '1'='1 não está matriculado em CC201 (2026.2)

Documentação: https://docs.python.org/pt-br/3/library/sqlite3.html
"""

import sqlite3
import tempfile
from collections.abc import Callable
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
INJECAO = "' OR '1'='1"


# 1) Uma linha ou nenhuma ------------------------------------------------------------
def buscar_aluno(con: sqlite3.Connection, matricula: str) -> dict[str, str] | None:
    """Devolve {"matricula", "nome", "email", "curso"} do aluno, com a SIGLA do curso,
    ou None se a matrícula não existir."""
    raise NotImplementedError("TODO 1")


# 2) Várias linhas ---------------------------------------------------------------------
def alunos_do_curso(con: sqlite3.Connection, sigla: str) -> list[str]:
    """Nomes dos alunos do curso com essa sigla, em ordem alfabética.
    Lista vazia se a sigla não existir."""
    raise NotImplementedError("TODO 2")


# 3) Agregação ---------------------------------------------------------------------------
def media_por_disciplina(
    con: sqlite3.Connection, semestre: str
) -> list[tuple[str, float]]:
    """Pares (código da disciplina, média das notas arredondada em 2 casas) do semestre,
    da maior média para a menor. Disciplinas sem nenhuma nota lançada ficam de fora."""
    raise NotImplementedError("TODO 3")


# 4) Alteração com transação --------------------------------------------------------------
def lancar_nota(
    con: sqlite3.Connection, matricula: str, codigo: str, semestre: str, nota: float
) -> None:
    """Grava a nota do aluno na turma da disciplina naquele semestre.

    Levanta ValueError se:
    * a nota estiver fora do intervalo de 0 a 10
      (mensagem: "nota fora do intervalo de 0 a 10: 10.5");
    * o aluno não estiver matriculado nessa turma, ou seja, nenhuma linha foi alterada
      (mensagem: "2025001 não está matriculado em ES101 (2026.1)").

    A alteração deve ser confirmada (commit) antes de a função retornar. Dica: use a
    conexão como gerenciador de contexto (with con:), que faz commit no sucesso e
    rollback no erro.
    """
    raise NotImplementedError("TODO 4")


# Pronto: execução da prática ----------------------------------------------------------
def conectar(caminho: Path) -> sqlite3.Connection:
    con = sqlite3.connect(caminho)
    con.execute("PRAGMA foreign_keys = ON")
    return con


def criar_banco(caminho: Path) -> None:
    con = conectar(caminho)
    with con:
        for nome in ("escola_esquema.sql", "escola_dados.sql"):
            con.executescript((RAIZ / "dados" / nome).read_text(encoding="utf-8"))
    con.close()


def nota_de(
    con: sqlite3.Connection, matricula: str, codigo: str, semestre: str
) -> object:
    linha = con.execute(
        """
        SELECT m.nota FROM matricula AS m
        JOIN aluno AS a ON a.id = m.aluno_id
        JOIN turma AS t ON t.id = m.turma_id
        JOIN disciplina AS d ON d.id = t.disciplina_id
        WHERE a.matricula = ? AND d.codigo = ? AND t.semestre = ?
        """,
        (matricula, codigo, semestre),
    ).fetchone()
    return None if linha is None else linha[0]


def secao_buscar(con: sqlite3.Connection) -> None:
    aluno = buscar_aluno(con, "2025001")
    if aluno is not None:
        print(f"   2025001: {aluno['nome']}, {aluno['curso']}, {aluno['email']}")
    else:
        print("   2025001: None")
    print(f"   1999999: {buscar_aluno(con, '1999999')}")
    print(f"   injeção: {buscar_aluno(con, 'x' + INJECAO)}")


def secao_curso(con: sqlite3.Connection) -> None:
    nomes = alunos_do_curso(con, "ES")
    print(f"   ES: {len(nomes)} alunos; os três primeiros: {', '.join(nomes[:3])}")
    print(f"   XX: {alunos_do_curso(con, 'XX')}")
    print(f"   injeção: {alunos_do_curso(con, 'CC' + INJECAO)}")


def secao_medias(con: sqlite3.Connection) -> None:
    medias = media_por_disciplina(con, "2026.1")
    if medias:
        (primeira, maior), (ultima, menor) = medias[0], medias[-1]
        faixa = f"de {primeira} ({maior}) a {ultima} ({menor})"
        print(f"   2026.1: {len(medias)} disciplinas, {faixa}")
    else:
        print("   2026.1: []")
    print(f"   2026.2: {media_por_disciplina(con, '2026.2')}")


def secao_lancar(caminho: Path) -> None:
    con = conectar(caminho)
    try:
        lancar_nota(con, "2025001", "CC201", "2026.2", 8.5)
    finally:
        con.close()  # fechar sem commit descartaria a alteração
    outra = conectar(caminho)
    try:
        conferir_lancamentos(outra)
    finally:
        outra.close()


def conferir_lancamentos(outra: sqlite3.Connection) -> None:
    lida = nota_de(outra, "2025001", "CC201", "2026.2")
    print(f"   8.5 em CC201 (2026.2): gravada; lida de outra conexão: {lida}")
    tentativas = [
        ("10.5", ("2025001", "CC201", "2026.2", 10.5)),
        ("ES101 (2026.1)", ("2025001", "ES101", "2026.1", 9.0)),
        ("injeção", ("2025001" + INJECAO, "CC201", "2026.2", 10.0)),
    ]
    for rotulo, (matricula, codigo, semestre, nota) in tentativas:
        try:
            lancar_nota(outra, matricula, codigo, semestre, nota)
        except ValueError as erro:
            print(f"   {rotulo}: ValueError: {erro}")
        else:
            print(f"   {rotulo}: aceita, mas deveria ser recusada")


def main() -> None:
    with tempfile.TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "escola.db"
        criar_banco(caminho)
        con = conectar(caminho)
        secoes: list[tuple[str, Callable[[sqlite3.Connection], None]]] = [
            ("1) buscar_aluno", secao_buscar),
            ("2) alunos_do_curso", secao_curso),
            ("3) media_por_disciplina", secao_medias),
        ]
        for titulo, executar in secoes:
            print(titulo)
            try:
                executar(con)
            except NotImplementedError as falta:
                print(f"   ainda não implementada ({falta})")
        con.close()
        print("4) lancar_nota")
        try:
            secao_lancar(caminho)
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")


if __name__ == "__main__":
    main()
