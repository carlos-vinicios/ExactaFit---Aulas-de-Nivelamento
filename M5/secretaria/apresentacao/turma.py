"""Tela do relatório de uma turma.

python -m secretaria.apresentacao.turma CC201 2026.1
"""

from secretaria.dominio import Situacao
from secretaria.servicos import consultas

from .terminal import executar, formatar_media, formatar_nota, ler_argumentos, quantos


def mostrar_turma(codigo: str, semestre: str) -> None:
    relatorio = consultas.relatorio_turma(codigo.upper(), semestre)
    t = relatorio.turma
    print(f"{t.codigo} {t.disciplina}, {t.semestre}, docente: {t.professor}")
    print()
    print(f"{'matrícula':<10} {'nome':<22} {'nota':>4}  situação")
    for linha in relatorio.linhas:
        a = linha.matricula.aluno
        nota = formatar_nota(linha.matricula.nota)
        print(f"{a.matricula:<10} {a.nome:<22} {nota:>4}  {linha.situacao}")
    print()
    c = relatorio.contagem
    print(
        f"{quantos(len(relatorio.linhas), 'aluno', 'alunos')}: "
        f"{quantos(c[Situacao.APROVADO], 'aprovado', 'aprovados')}, "
        f"{quantos(c[Situacao.REPROVADO], 'reprovado', 'reprovados')}, "
        f"{c[Situacao.CURSANDO]} cursando"
    )
    print(f"Média da turma: {formatar_media(relatorio.media)}")


def main() -> None:
    codigo, semestre = ler_argumentos("codigo", "semestre")
    executar(lambda: mostrar_turma(codigo, semestre))


if __name__ == "__main__":
    main()
