"""Tela de lançamento de nota.

python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 8.5
"""

from secretaria.servicos import notas  # noqa: F401 (usado nas práticas)

from .terminal import descrever, executar, formatar_nota, ler_argumentos, numero  # noqa: F401 (usado nas práticas)


def lancar(matricula: str, codigo: str, semestre: str, nota: float) -> None:
    """Chama o serviço notas.lancar_nota e mostra o resultado numa linha, por exemplo:

    Nota 8.5 lançada: 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2), aprovado

    O código da disciplina vai em maiúsculas (cc201 vira CC201). Use formatar_nota() e
    descrever(), de terminal.py.
    """
    raise NotImplementedError("TODO Aula 6, Prática 3")


def main() -> None:
    matricula, codigo, semestre, nota = ler_argumentos(
        "matricula", "codigo", "semestre", "nota"
    )
    valor = numero(nota, "a nota")
    executar(lambda: lancar(matricula, codigo, semestre, valor))


if __name__ == "__main__":
    main()
