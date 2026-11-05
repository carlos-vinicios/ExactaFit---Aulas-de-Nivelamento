# Aula 6, Prática 3: lançar nota, com a transação no serviço

Agora uma tela que grava no banco:
`python -m secretaria.apresentacao.lancar_nota MATRICULA CODIGO SEMESTRE NOTA`.

## Parte A: proposta

Antes de abrir o código, escreva em `PROPOSTA.md` o caminho de
`lancar_nota 2025001 CC201 2026.2 8.46`, como no `MAPA.md` da Prática 1, e responda: em que
ponto a transação começa e onde ela é confirmada? Para cada pedido recusado da saída esperada,
qual camada recusa?

## Parte B: implementação

Procure `TODO Aula 6, Prática 3` e compare com a sua proposta:

1. **Acesso a dados**, `acesso_dados/matriculas.py`: `gravar_nota`, com um `UPDATE` e
   parâmetros `?`. Sem `commit` aqui.
2. **Manager**, `managers/avaliacao.py`: `preparar_nota`. Três regras, na ordem: nota de 0 a
   10; só no semestre em andamento (`SEMESTRE_ATUAL`, de `config.py`); uma casa decimal. Regra
   não atendida: `RegraDeNegocioError` com a mensagem da saída esperada.
3. **Serviço**, `servicos/notas.py`: `lancar_nota`. Um único `with dados.abrir() as con:` para
   buscar aluno, turma e matrícula, pedir a nota ao manager e gravar.
4. **Apresentação**, `apresentacao/lancar_nota.py`: `lancar`, que chama o serviço e imprime a
   linha do resultado. A leitura dos argumentos e a conversão da nota (`numero()`) já estão
   prontas em `main()`.

## Saída esperada

Com o banco recém-criado (`python ../M4/ferramentas/criar_banco.py escola.db`), nesta ordem:

```text
$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 8.46
Nota 8.5 lançada: 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2), aprovado

$ python -m secretaria.apresentacao.boletim 2025001
Ana Beatriz Souza (2025001), curso CC

semestre  disciplina                       nota  situação
2026.1    CC101 Algoritmos                  9.9  aprovado
2026.1    CC102 Estruturas de Dados         4.5  reprovado
2026.1    CC202 Redes de Computadores       5.6  reprovado
2026.2    CC102 Estruturas de Dados           -  cursando
2026.2    CC201 Banco de Dados              8.5  aprovado

Média das notas lançadas: 7.12
```

Os pedidos que devem ser recusados:

```text
$ python -m secretaria.apresentacao.lancar_nota 2025001 CC101 2026.1 9
não permitido: o semestre 2026.1 está encerrado; notas só podem ser lançadas em 2026.2

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 11
não permitido: a nota deve ficar entre 0 e 10, e veio 11.0

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 dez
erro: a nota deve ser um número, como 8.5

$ python -m secretaria.apresentacao.lancar_nota 2025001 ES201 2026.2 7
erro: 2025001 não está matriculado em ES201 (2026.2)
```

## Para pensar

* A nota `dez` foi recusada pela apresentação, e a nota `11` pelo manager. As duas são problemas
  do mesmo tipo? Guarde a resposta para a Aula 7.
* Abra o `escola.db` com a extensão SQLite Viewer depois de um lançamento recusado. Alguma
  coisa mudou no banco? Qual parte do código garante isso?
