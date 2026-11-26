"""Gera as imagens de exemplo do desafio extra da Aula 10 (documentos digitalizados, fictícios).

    python exercicios/aula10/desafio_extra/gerar_imagens.py

Cria três PNG nesta pasta, com texto em português, para testar a rota de OCR:
atestado_2025001.png, requerimento_2026005.png e aviso_sem_matricula.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PASTA = Path(__file__).parent

DOCUMENTOS = {
    "atestado_2025001.png": [
        "ATESTADO",
        "",
        "Atesto, para os devidos fins, que a aluna",
        "Ana Beatriz Souza, matrícula 2025001, do curso",
        "de Ciência da Computação, esteve afastada das",
        "aulas de 10/11/2026 a 12/11/2026.",
        "",
        "Documento fictício, gerado para a Aula 10.",
    ],
    "requerimento_2026005.png": [
        "REQUERIMENTO DE MATRÍCULA",
        "",
        "Eu, Olívia Santos, matrícula 2026005, solicito",
        "matrícula na turma CC102 do semestre 2026.2.",
        "Turma de origem: CC101, semestre 2026.1.",
        "",
        "Documento fictício, gerado para a Aula 10.",
    ],
    "aviso_sem_matricula.png": [
        "AVISO DA SECRETARIA",
        "",
        "As notas de 2026.2 devem ser lançadas até",
        "o fim do semestre. Dúvidas: procure a secretaria.",
    ],
}


# Fontes com acentos: a do Linux (DejaVu, Ubuntu e WSL) ou a do Windows (Arial).
FONTES = [
    "DejaVuSans.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "arial.ttf",
]


def fonte() -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for nome in FONTES:
        try:
            return ImageFont.truetype(nome, 30)
        except OSError:
            continue
    print(
        "aviso: sem DejaVu nem Arial; com a fonte padrão, os acentos podem sair errados"
    )
    return ImageFont.load_default(size=30)


def gerar(nome: str, linhas: list[str]) -> None:
    letra = fonte()
    imagem = Image.new("L", (1000, 90 + 46 * len(linhas)), color=255)
    desenho = ImageDraw.Draw(imagem)
    for i, linha in enumerate(linhas):
        desenho.text((50, 45 + 46 * i), linha, fill=0, font=letra)
    imagem.save(PASTA / nome)
    print(f"gerado: {PASTA / nome}")


def main() -> None:
    for nome, linhas in DOCUMENTOS.items():
        gerar(nome, linhas)


if __name__ == "__main__":
    main()
