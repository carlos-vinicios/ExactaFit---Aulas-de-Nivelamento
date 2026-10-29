"""Aula 5, Prática 3: consultas e alterações com os modelos SQLAlchemy.

Complete as quatro funções marcadas com TODO usando os modelos de modelo_de_dados/modelos.
Nada de SQL escrito à mão: use select(), os atributos dos modelos e os relacionamentos.
Cada função recebe a sessão aberta; não abra outra sessão nem faça commit dentro dela.

Rode a partir da pasta M4, com o banco migrado e semeado, e compare com a saída esperada:

    python -m exercicios.aula5.p3_modelos.consultas_orm

No fim, o programa desfaz as alterações com rollback(): o banco não muda.

Saída esperada com as quatro funções prontas:

    1) alunos_do_curso
       ES: 15 alunos; os três primeiros: Felipe Azevedo, Giovana Batista, Henrique Coelho
       XX: []
    2) turmas_do_professor
       Juliana Teixeira: CC201 (2026.1), SI201 (2026.1), CC201 (2026.2), SI201 (2026.2)
       Otávio Rezende: []
    3) media_da_turma
       CC201 (2026.1): 7.77
       CC201 (2026.2): None
    4) lancar_nota
       8.5 em CC201 (2026.2): gravada; lida de novo: 8.5
       10.5: ValueError: nota fora do intervalo de 0 a 10: 10.5
       CC999 (2026.2): LookupError: 2025001 não está matriculado em CC999 (2026.2)
"""

from sqlalchemy import func, select  # noqa: F401 (func: para a função 3)
from sqlalchemy.orm import Session

from modelo_de_dados.conexao import Sessao
from modelo_de_dados.modelos import (
    Aluno,
    Curso,  # noqa: F401 (para a função 1)
    Disciplina,
    Matricula,
    Professor,  # noqa: F401 (para a função 2)
    Turma,
)


# 1) Filtro por uma tabela ligada -------------------------------------------------------
def alunos_do_curso(sessao: Session, sigla: str) -> list[Aluno]:
    """Alunos do curso de sigla `sigla`, em ordem de nome. Curso inexistente: lista vazia.

    Dica: select(Aluno).join(Aluno.curso).where(Curso.sigla == sigla), e list(sessao.scalars(...)).
    """
    raise NotImplementedError("TODO 1")


# 2) Duas junções e ordenação ------------------------------------------------------------
def turmas_do_professor(sessao: Session, nome: str) -> list[Turma]:
    """Turmas do professor de nome `nome`, por semestre e código da disciplina.

    Professor sem turmas ou inexistente: lista vazia.
    """
    raise NotImplementedError("TODO 2")


# 3) Agregação ------------------------------------------------------------------------------
def media_da_turma(sessao: Session, codigo: str, semestre: str) -> float | None:
    """Média das notas lançadas da turma, arredondada em 2 casas; None se não houver nota.

    Dica: select(func.avg(Matricula.nota)) com as junções até a disciplina, e sessao.scalar().
    """
    raise NotImplementedError("TODO 3")


# 4) Alteração ---------------------------------------------------------------------------
def lancar_nota(
    sessao: Session, matricula: str, codigo: str, semestre: str, nota: float
) -> None:
    """Grava a nota de um aluno numa turma.

    * nota fora de 0 a 10: ValueError("nota fora do intervalo de 0 a 10: <nota>"), antes de
      consultar o banco;
    * matrícula inexistente: LookupError("<matricula> não está matriculado em <codigo> (<semestre>)");
    * caso contrário, altere o atributo nota do objeto Matricula e chame sessao.flush().
    """
    raise NotImplementedError("TODO 4")


# Pronto: execução da prática -----------------------------------------------------------
def main() -> None:
    with Sessao() as sessao:
        print("1) alunos_do_curso")
        try:
            es = alunos_do_curso(sessao, "ES")
            primeiros = ", ".join(a.nome for a in es[:3])
            print(f"   ES: {len(es)} alunos; os três primeiros: {primeiros}")
            print(f"   XX: {alunos_do_curso(sessao, 'XX')}")
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")

        print("2) turmas_do_professor")
        try:
            for nome in ("Juliana Teixeira", "Otávio Rezende"):
                turmas = turmas_do_professor(sessao, nome)
                texto = ", ".join(
                    f"{t.disciplina.codigo} ({t.semestre})" for t in turmas
                )
                print(f"   {nome}: {texto or '[]'}")
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")

        print("3) media_da_turma")
        try:
            for semestre in ("2026.1", "2026.2"):
                print(
                    f"   CC201 ({semestre}): {media_da_turma(sessao, 'CC201', semestre)}"
                )
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")

        print("4) lancar_nota")
        try:
            lancar_nota(sessao, "2025001", "CC201", "2026.2", 8.5)
            lida = sessao.scalars(
                select(Matricula.nota)
                .join(Matricula.aluno)
                .join(Matricula.turma)
                .join(Turma.disciplina)
                .where(
                    Aluno.matricula == "2025001",
                    Disciplina.codigo == "CC201",
                    Turma.semestre == "2026.2",
                )
            ).one()
            print(f"   8.5 em CC201 (2026.2): gravada; lida de novo: {lida}")
            for nota, codigo in ((10.5, "CC201"), (7.0, "CC999")):
                try:
                    lancar_nota(sessao, "2025001", codigo, "2026.2", nota)
                except (ValueError, LookupError) as erro:
                    rotulo = nota if codigo == "CC201" else f"{codigo} (2026.2)"
                    print(f"   {rotulo}: {type(erro).__name__}: {erro}")
        except NotImplementedError as falta:
            print(f"   ainda não implementada ({falta})")

        sessao.rollback()  # desfaz a nota lançada: o banco continua igual


if __name__ == "__main__":
    main()
