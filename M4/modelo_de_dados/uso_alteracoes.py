"""Inserir, alterar e apagar com os modelos, dentro de uma transação.

A sessão anota as mudanças nos objetos e envia o INSERT, o UPDATE e o DELETE no flush() ou no
commit(). No fim, este script desfaz tudo com rollback(): o banco não muda e o script pode rodar
de novo. Num programa de verdade, a última linha seria sessao.commit().

    python -m modelo_de_dados.uso_alteracoes
"""

from sqlalchemy import func, select

from modelo_de_dados.conexao import Sessao
from modelo_de_dados.modelos import Disciplina, Professor


def contar_professores() -> int:
    with Sessao() as sessao:
        return sessao.scalar(select(func.count()).select_from(Professor)) or 0


def main() -> None:
    print(f"Professores antes: {contar_professores()}")

    with Sessao() as sessao:
        print("1) Inserir: um objeto novo e sessao.add()")
        marina = Professor(nome="Marina Duarte", email="marina.duarte@escola.edu")
        sessao.add(marina)
        sessao.flush()  # envia o INSERT agora; o banco gera o id
        print(f"   {marina} recebeu o id {marina.id}")

        print("2) Alterar: mudar o atributo do objeto")
        bd = sessao.scalars(
            select(Disciplina).where(Disciplina.codigo == "CC201")
        ).one()
        antes = bd.carga_horaria
        # A sessão percebe a mudança no objeto; o UPDATE sai no flush.
        bd.carga_horaria = antes + 20
        sessao.flush()
        print(f"   {bd.codigo}: {antes} h -> {bd.carga_horaria} h")

        print("3) Apagar: sessao.delete()")
        otavio = sessao.scalars(
            select(Professor).where(Professor.email == "otavio.rezende@escola.edu")
        ).one()
        sessao.delete(otavio)
        sessao.flush()
        total = sessao.scalar(select(func.count()).select_from(Professor))
        print(f"   {otavio.nome} apagado; dentro da transação há {total} professores")

        sessao.rollback()  # num programa de verdade: sessao.commit()
        print("4) rollback(): as três alterações foram desfeitas")

    print(f"Professores depois: {contar_professores()}")


if __name__ == "__main__":
    main()
