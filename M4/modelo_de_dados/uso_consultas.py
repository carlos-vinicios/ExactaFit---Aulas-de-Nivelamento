"""Consultas com os modelos: select(), where(), order_by() e contagem.

Rode a partir da pasta M4, com o banco migrado e semeado (alembic upgrade head e
python ferramentas/semear.py):

    python -m modelo_de_dados.uso_consultas
"""

from sqlalchemy import func, select

from modelo_de_dados.conexao import Sessao
from modelo_de_dados.modelos import Aluno, Curso, Disciplina, Professor


def main() -> None:
    with Sessao() as sessao:
        print("1) Todos os cursos")
        for curso in sessao.scalars(select(Curso).order_by(Curso.sigla)):
            print(f"   {curso.sigla}  {curso.nome}")

        print("2) Disciplinas com 80 horas ou mais (a q03 da Aula 4)")
        consulta = (
            select(Disciplina)
            .where(Disciplina.carga_horaria >= 80)
            .order_by(Disciplina.carga_horaria.desc(), Disciplina.codigo)
        )
        for disciplina in sessao.scalars(consulta):
            print(
                f"   {disciplina.codigo}  {disciplina.nome:<26} {disciplina.carga_horaria} h"
            )

        print("3) Um aluno pela matrícula")
        aluno = sessao.scalars(select(Aluno).where(Aluno.matricula == "2025001")).one()
        print(f"   {aluno}, ingresso em {aluno.data_ingresso:%d/%m/%Y}")

        print("4) Um professor pela chave primária")
        print(f"   {sessao.get(Professor, 1)}")

        print("5) Quantos alunos em cada curso (a q10 da Aula 4)")
        contagem = (
            select(Curso.sigla, func.count(Aluno.id))
            .join(Curso.alunos)
            .group_by(Curso.sigla)
            .order_by(Curso.sigla)
        )
        for sigla, total in sessao.execute(contagem):
            print(f"   {sigla}: {total} alunos")


if __name__ == "__main__":
    main()
