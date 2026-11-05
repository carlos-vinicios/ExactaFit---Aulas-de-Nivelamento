# Proposta: relatório da turma

Pedido: `python -m secretaria.apresentacao.turma CC201 2026.1`

## Funções, de baixo para cima

| Camada | Arquivo | Função (parâmetros e retorno, com tipos) | O que faz |
|---|---|---|---|
| acesso a dados | | | |
| manager | | | |
| serviço | | | |
| apresentação | `apresentacao/turma.py` | `mostrar_turma(codigo: str, semestre: str) -> None` | chama o serviço e imprime o relatório |

## Perguntas

1. Algum tipo novo precisa entrar em `dominio.py`? Qual, e com quais campos?
2. Qual função já existente cada camada pode reaproveitar?
3. Turma que não existe (`CC301 2026.1`): qual exceção, e em qual camada ela nasce?
4. Quem calcula "9 aprovados, 2 reprovados": o banco, o manager ou a apresentação? Por quê?
