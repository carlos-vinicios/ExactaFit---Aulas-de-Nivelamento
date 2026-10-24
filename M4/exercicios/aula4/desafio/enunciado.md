# Desafio da Aula 4: ranking por curso

A coordenação quer premiar os três alunos com maior média no semestre 2026.1 **em cada
curso**. Escreva a consulta em `top3_por_curso.sql`.

Colunas: `sigla`, `posicao` (1, 2, 3), `nome`, `media` (arredondada em 2 casas). Ordene por
sigla e posição. Se dois alunos do mesmo curso tiverem a mesma média, o desempate é pelo nome.

Com `GROUP BY` você calcula a média de cada aluno, mas não consegue numerar os alunos dentro
de cada curso. Para isso, estude:

* **CTE** (`WITH ... AS`): dá nome a uma consulta intermediária.
  <https://www.sqlite.org/lang_with.html>
* **Funções de janela** (`row_number() OVER (PARTITION BY ... ORDER BY ...)`): numeram as
  linhas dentro de cada grupo sem juntar as linhas num só resultado.
  <https://www.sqlite.org/windowfunctions.html>
* Tutorial com exemplos: <https://www.sqlitetutorial.net/sqlite-window-functions/sqlite-row_number/>

Rode com `python ferramentas/sql.py escola.db exercicios/aula4/desafio/top3_por_curso.sql` e
compare com o resultado esperado no topo do arquivo.

Entrega: o arquivo `top3_por_curso.sql` com a saída igual à esperada e, em comentário no final,
a resposta: o que muda no resultado se você trocar `row_number()` por `rank()`? Quando
isso faria diferença?
