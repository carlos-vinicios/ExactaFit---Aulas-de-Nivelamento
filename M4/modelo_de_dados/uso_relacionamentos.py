"""Navegando pelos relacionamentos: de um objeto para os objetos ligados a ele.

Cada relationship() dos modelos vira um atributo. aluno.curso devolve um Curso; aluno.matriculas
devolve uma lista de Matricula. O SQLAlchemy faz o SELECT quando o atributo é lido.

    python -m modelo_de_dados.uso_relacionamentos
"""

from sqlalchemy import select

from modelo_de_dados.conexao import Sessao
from modelo_de_dados.modelos import Aluno, Curso, Professor


def main() -> None:
    with Sessao() as sessao:
        aluno = sessao.scalars(select(Aluno).where(Aluno.matricula == "2025001")).one()

        print("1) N:1, do aluno para o curso")
        print(f"   {aluno.nome} estuda {aluno.curso.nome}")

        print("2) 1:N, do aluno para as matrículas, e delas para turma e disciplina")
        matriculas = sorted(
            aluno.matriculas,
            key=lambda m: (m.turma.semestre, m.turma.disciplina.codigo),
        )
        for m in matriculas:
            nota = "-" if m.nota is None else f"{m.nota:.1f}"
            print(f"   {m.turma.semestre}  {m.turma.disciplina.codigo}  {nota:>4}")

        print("3) 1:N, do professor para as turmas")
        juliana = sessao.scalars(
            select(Professor).where(Professor.nome == "Juliana Teixeira")
        ).one()
        for turma in sorted(
            juliana.turmas, key=lambda t: (t.semestre, t.disciplina.codigo)
        ):
            print(
                f"   {turma.semestre}  {turma.disciplina.codigo}  {turma.disciplina.nome}"
            )

        print("4) O outro lado da mesma relação")
        si = sessao.scalars(select(Curso).where(Curso.sigla == "SI")).one()
        print(
            f"   {si.sigla} tem {len(si.alunos)} alunos e {len(si.disciplinas)} disciplinas"
        )


if __name__ == "__main__":
    main()
