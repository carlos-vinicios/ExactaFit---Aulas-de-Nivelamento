# Aula 7, Prática 3: matricular, da proposta à escrita pelo ORM

A secretaria quer matricular um aluno numa turma:
`python -m secretaria.apresentacao.matricular MATRICULA CODIGO SEMESTRE`.

## Parte A: proposta

Antes de abrir o código, preencha `PROPOSTA.md`: as funções de cada camada, e quem recusa cada
pedido da saída esperada. Use as quatro defesas que você já conhece: o schema (formato), o
serviço (registro que não existe), o manager (regra da escola) e o banco (restrições).

## Parte B: implementação

A tela (`apresentacao/matricular.py`) está pronta. Procure `TODO Aula 7, Prática 3`:

1. **Schema**, `schemas.py`: os campos de `NovaMatricula` (matrícula, código e semestre, com os
   tipos já prontos).
2. **Manager**, `managers/matriculas.py`: `conferir_matricula`. Três regras, na ordem: só no
   semestre em andamento; a disciplina tem de ser do curso do aluno; o aluno não pode já estar
   matriculado na turma.
3. **Acesso a dados**, `acesso_orm/matriculas.py`: `inserir_matricula`, com `sessao.add()` de
   um `modelos.Matricula` sem nota e `sessao.flush()`.
4. **Serviço**, `servicos/matriculas.py`: `matricular`. Busque aluno e turma, descubra se a
   matrícula já existe (`dados.buscar_matricula`), peça a conferência ao manager e insira.

## Saída esperada

Com o banco recém-criado, nesta ordem:

```text
$ python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2
Matrícula feita: 2026005 Olívia Santos, CC102 Estruturas de Dados (2026.2), cursando

$ python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2
não permitido: 2026005 já está matriculado em CC102 (2026.2)

$ python -m secretaria.apresentacao.matricular 2026005 ES201 2026.2
não permitido: ES201 é uma disciplina de ES, e o aluno é de CC

$ python -m secretaria.apresentacao.matricular 2026005 CC101 2026.1
não permitido: matrículas só no semestre em andamento (2026.2)

$ python -m secretaria.apresentacao.matricular 2026005 cc999 2026.2
erro: turma CC999 (2026.2) não encontrada

$ python -m secretaria.apresentacao.matricular 2026005 CC1 2026.2
erro: codigo: deve ter 2 letras e 3 dígitos, como CC201
```

## Para pensar

* Comente, por um instante, a regra da matrícula repetida no manager e repita o segundo pedido.
  Quem recusa agora, e como a mensagem chega à tela? Por que vale ter as duas defesas? Volte a
  regra para o lugar.
* Compare a sua `PROPOSTA.md` com o que você implementou. O que mudou entre a proposta e o
  código, e por quê?
