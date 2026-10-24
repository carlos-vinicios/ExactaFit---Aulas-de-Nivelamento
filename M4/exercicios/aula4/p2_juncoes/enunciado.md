# Prática 2: junções e agregação

Arquivos `q09` a `q16`. As perguntas agora cruzam tabelas. Antes de escrever cada consulta,
desenhe no papel o caminho entre as tabelas: por exemplo, para a média por disciplina,
`matricula` → `turma` → `disciplina`.

```bash
python ferramentas/sql.py escola.db exercicios/aula4/p2_juncoes/q09_aluno_curso.sql
```

Cada arquivo traz o resultado esperado no comentário do topo. Nos resultados longos, o
comentário mostra as primeiras e as últimas linhas e o total: confira essas linhas e o número
no final, `(45 linhas)` por exemplo.

Pistas:

* q10: e se um curso não tivesse nenhum aluno? Ele deveria aparecer com 0. Qual junção garante isso?
* q13: `WHERE` filtra linhas antes de agrupar; `HAVING` filtra grupos depois.
* q14: `LEFT JOIN` mantém os alunos sem par em `matricula`, com as colunas da direita em NULL.
  Outra forma: `NOT EXISTS`.
* q16: a média geral é uma subconsulta que devolve um único valor.

Para ver o plano de execução de uma consulta, coloque `EXPLAIN QUERY PLAN` antes do `SELECT`.

## Referências

* Junções explicadas com diagramas: <https://www.sqlitetutorial.net/sqlite-join/>
* Agregação: <https://www.sqlite.org/lang_aggfunc.html>
* Exercícios extras com junções: <https://pgexercises.com> (PostgreSQL, mas quase tudo roda no SQLite)
