# Desafio da Aula 6: ranking por curso

A coordenação quer as maiores médias de um curso num semestre:

```text
$ python -m secretaria.apresentacao.ranking CC 2026.1
Ranking CC, 2026.1
 1  Diego Ramos            8.53
 2  Bruno Costa            8.10
 3  Lucas Martins          8.00

$ python -m secretaria.apresentacao.ranking es 2026.1
Ranking ES, 2026.1
 1  Thiago Moreira         8.00
 2  Renato Bezerra         7.60
 3  Priscila Rangel        7.23
```

Regras: a média de cada aluno considera só as notas lançadas nas turmas do semestre; alunos sem
nota nenhuma ficam de fora; os 3 maiores aparecem; empate pela ordem alfabética do nome.

Desta vez não há esqueleto: a funcionalidade é sua, da proposta ao código.

1. Escreva `PROPOSTA.md` nesta pasta: a tabela de funções por camada (como na Prática 1), o
   tipo novo de `dominio.py` com os seus campos, e em qual camada fica cada regra acima.
2. Implemente nas quatro camadas, sem quebrar as regras de cada uma: SQL só no acesso a dados
   (e a função nova na interface da camada, `acesso_dados/__init__.py`), regras no manager,
   transação no serviço e `print` só na tela nova, `apresentacao/ranking.py`.
3. Confira estilo e tipos: `ruff check .` e `mypy --strict secretaria`.

Entrega: `PROPOSTA.md` e o código. Na Aula 7, o ranking passa a funcionar também no PostgreSQL;
anote na proposta o que você acha que vai precisar mudar para isso.
