# Prática 1: consultas e alterações

Cada arquivo `q01` a `q08` traz o pedido em comentário e, logo abaixo, o resultado esperado.
Escreva o SQL depois dos comentários e rode a partir da pasta M4:

```bash
python ferramentas/criar_banco.py             # recria escola.db do zero
python ferramentas/sql.py escola.db exercicios/aula4/p1_consultas/q01_professores.sql
```

Compare a saída com o bloco "Resultado esperado" do arquivo: as mesmas colunas, as mesmas
linhas e a mesma ordem.

## Conferência de q06, q07 e q08

Essas três alteram o `escola.db` de verdade e não mostram linhas. Para conferir, recrie o
banco e rode as três seguidas, terminando com `conferir_alteracoes.sql`:

```bash
python ferramentas/criar_banco.py
python ferramentas/sql.py escola.db exercicios/aula4/p1_consultas/q06_inserir_professor.sql exercicios/aula4/p1_consultas/q07_atualizar_carga.sql exercicios/aula4/p1_consultas/q08_apagar_professor.sql exercicios/aula4/p1_consultas/conferir_alteracoes.sql
```

A saída começa com três linhas `ok (nenhum comando devolveu linhas)`, uma para cada alteração.
Depois delas, o esperado é:

```text
professores | marina | otavio
------------+--------+-------
9           | 1      | 0
(1 linha)

menor_carga | total_horas
------------+------------
60          | 860
(1 linha)

codigo | carga_horaria
-------+--------------
CC101  | 80
CC201  | 60
CC301  | 60
(3 linhas)

turmas | matriculas | alunos
-------+------------+-------
18     | 210        | 45
(1 linha)
```

Depois, recrie o banco com `python ferramentas/criar_banco.py` antes da Prática 2.

## Antes de q06, q07 e q08

Um `UPDATE` ou `DELETE` sem `WHERE` altera **todas** as linhas. Um hábito seguro: escreva
primeiro o `SELECT` com o mesmo `WHERE`, confira as linhas, e só então troque pelo `UPDATE`
ou `DELETE`.

Depois de fazer a q08, experimente apagar a professora Helena Prado. O que acontece? Por quê?
(Pense na tabela `turma` e no que você viu sobre chaves estrangeiras na Aula 3.)

## Referências

* SELECT no SQLite: <https://www.sqlite.org/lang_select.html>
* Tutorial interativo com exercícios: <https://sqlbolt.com>
* Funções de data do SQLite: <https://www.sqlite.org/lang_datefunc.html>
