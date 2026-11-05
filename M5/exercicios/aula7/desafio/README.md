# Desafio da Aula 7: cancelar matrícula

A secretaria quer cancelar uma matrícula feita por engano:

```text
$ python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2
Matrícula feita: 2026005 Olívia Santos, CC102 Estruturas de Dados (2026.2), cursando

$ python -m secretaria.apresentacao.cancelar_matricula 2026005 CC102 2026.2
Matrícula cancelada: 2026005 Olívia Santos, CC102 Estruturas de Dados (2026.2)

$ python -m secretaria.apresentacao.cancelar_matricula 2025001 CC101 2026.1
não permitido: o semestre 2026.1 está encerrado; a matrícula não pode ser cancelada

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 8.5
Nota 8.5 lançada: 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2), aprovado

$ python -m secretaria.apresentacao.cancelar_matricula 2025001 CC201 2026.2
não permitido: a matrícula já tem nota e não pode ser cancelada

$ python -m secretaria.apresentacao.cancelar_matricula 2026005 CC102 2026.2
erro: 2026005 não está matriculado em CC102 (2026.2)
```

Regras: só se cancela matrícula do semestre em andamento, e só se ela ainda não tem nota.

Como no desafio da Aula 6, a funcionalidade é sua, da proposta ao código:

1. Escreva `PROPOSTA.md` nesta pasta: as funções por camada e quem recusa cada pedido acima.
2. Implemente: a tela `apresentacao/cancelar_matricula.py` (o pedido usa o mesmo schema
   `NovaMatricula`), o serviço, a regra no manager e a remoção pelo ORM (`sessao.delete()`),
   acrescentada à interface de `acesso_orm`.
3. Confira estilo e tipos: `ruff check .` e `mypy --strict secretaria`.

Entrega: `PROPOSTA.md` e o código.
