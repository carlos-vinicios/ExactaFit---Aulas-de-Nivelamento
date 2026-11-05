"""Tela de matrícula (Aula 7).

python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2
"""

from secretaria.schemas import NovaMatricula
from secretaria.servicos import matriculas

from .terminal import descrever, executar, ler_argumentos


def matricular(matricula: str, codigo: str, semestre: str) -> None:
    pedido = NovaMatricula.model_validate(
        {"matricula": matricula, "codigo": codigo, "semestre": semestre}
    )
    linha = matriculas.matricular(pedido)
    print(f"Matrícula feita: {descrever(linha)}, {linha.situacao}")


def main() -> None:
    matricula, codigo, semestre = ler_argumentos("matricula", "codigo", "semestre")
    executar(lambda: matricular(matricula, codigo, semestre))


if __name__ == "__main__":
    main()
