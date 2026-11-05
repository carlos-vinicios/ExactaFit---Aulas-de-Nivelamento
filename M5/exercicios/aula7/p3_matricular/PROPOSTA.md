# Proposta: matrícula

Pedido: `python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2`

## Funções, de cima para baixo

| Camada | Arquivo | Função (parâmetros e retorno, com tipos) | O que faz |
|---|---|---|---|
| apresentação | `apresentacao/matricular.py` | `matricular(matricula: str, codigo: str, semestre: str) -> None` | monta o pedido, chama o serviço e imprime |
| schema | | | |
| serviço | | | |
| manager | | | |
| acesso a dados | | | |

## Quem recusa cada pedido

| Pedido | Defesa que recusa (schema, serviço, manager ou banco) | Por quê |
|---|---|---|
| `2026005 CC102 2026.2` (segunda vez) | | |
| `2026005 ES201 2026.2` | | |
| `2026005 CC101 2026.1` | | |
| `2026005 cc999 2026.2` | | |
| `2026005 CC1 2026.2` | | |
