"""Tela do boletim de um aluno.

python -m secretaria.apresentacao.boletim 2025001
"""

from secretaria.servicos import consultas

from .terminal import executar, formatar_media, formatar_nota, ler_argumentos


def mostrar_boletim(matricula: str) -> None:
    boletim = consultas.consultar_boletim(matricula)
    aluno = boletim.aluno
    print(f"{aluno.nome} ({aluno.matricula}), curso {aluno.curso}")
    print()
    print(f"{'semestre':<9} {'disciplina':<32} {'nota':>4}  situação")
    for linha in boletim.linhas:
        t = linha.matricula.turma
        disciplina = f"{t.codigo} {t.disciplina}"
        nota = formatar_nota(linha.matricula.nota)
        print(f"{t.semestre:<9} {disciplina:<32} {nota:>4}  {linha.situacao}")
    print()
    print(f"Média das notas lançadas: {formatar_media(boletim.media)}")


def main() -> None:
    (matricula,) = ler_argumentos("matricula")
    executar(lambda: mostrar_boletim(matricula))


if __name__ == "__main__":
    main()
