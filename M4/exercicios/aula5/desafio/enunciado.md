# Desafio da Aula 5: migração com dados

A secretaria quer ver a situação de cada matrícula sem calcular nada na hora: `cursando`,
`aprovado` ou `reprovado`.

Crie a revisão `0003` que:

1. acrescenta à tabela `matricula` a coluna `situacao`, obrigatória, que só aceita os três
   valores acima, com `cursando` como padrão para matrículas novas;
2. preenche a coluna nas matrículas que já existem: sem nota é `cursando`, nota maior ou igual
   a 6 é `aprovado`, abaixo de 6 é `reprovado`;
3. tem um `downgrade` que remove a coluna e a restrição.

```bash
alembic revision -m "situação da matrícula" --rev-id 0003
```

## Como conferir

No SQLite, num terminal sem `DATABASE_URL`, recrie o banco até a 0002 com dados, aplique a
sua 0003 e rode a conferência:

```bash
# apague o escola.db (Windows: del escola.db; Linux e macOS: rm escola.db)
alembic upgrade 0002
python ferramentas/semear.py
alembic upgrade head
python ferramentas/sql.py escola.db --continuar exercicios/aula5/desafio/conferir.sql
```

Saída esperada (o texto da mensagem de erro pode variar):

```text
> SELECT situacao, count(*) AS matriculas FROM matricula GROUP BY situacao ORDER BY situacao;
situacao  | matriculas
----------+-----------
aprovado  | 85
cursando  | 84
reprovado | 41
(3 linhas)

> SELECT DISTINCT situacao AS com_nota_6_ou_mais FROM matricula WHERE nota >= 6;
com_nota_6_ou_mais
------------------
aprovado
(1 linha)

> INSERT INTO matricula (aluno_id, turma_id) VALUES ((SELECT id FROM aluno WHERE matricula = '2026005'), (SELECT t.id FROM turma AS t JOIN disciplina AS d ON d.id = t.disciplina_id WHERE d.codigo = 'CC102' AND t.semestre = '2026.2'));
ok: 1 linha(s) afetada(s)

> SELECT situacao AS matricula_nova FROM matricula WHERE aluno_id = (SELECT id FROM aluno WHERE matricula = '2026005');
matricula_nova
--------------
cursando
(1 linha)

> UPDATE matricula SET situacao = 'trancado';
ERRO IntegrityError: CHECK constraint failed: ck_matricula_situacao

> DELETE FROM matricula WHERE aluno_id = (SELECT id FROM aluno WHERE matricula = '2026005');
ok: 1 linha(s) afetada(s)

> SELECT count(*) AS matriculas FROM matricula;
matriculas
----------
210
(1 linha)
```

Depois, `alembic downgrade 0002` deve remover a coluna e manter as 210 matrículas. Confira
com `SELECT situacao FROM matricula;`, que passa a dar erro (`no such column: situacao`).

Depois, aplique a migração nos dois bancos usando as tarefas do seu `Taskfile.yml`
(Prática 3) e confira o resultado com uma consulta que conte as matrículas por situação.

Pistas:

* Uma coluna `NOT NULL` nova numa tabela com dados precisa de valor para as linhas que já
  existem. Veja `server_default` em
  <https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column.params.server_default>.
* Migração de dados dentro de uma migração de esquema: `op.execute("UPDATE ...")` com `CASE`.
* `CHECK` no SQLite só pode ser criado recriando a tabela: use `batch_alter_table` e
  `create_check_constraint`. <https://alembic.sqlalchemy.org/en/latest/batch.html>

Por fim, rode `task db:reset --yes` e conte de novo as matrículas por situação. Todas ficam
`cursando`, inclusive as que têm nota. Por que isso acontece, se a sua migração calcula a
situação a partir da nota?

Entrega: o arquivo da migração, com a conferência igual à esperada nos dois bancos, e, num
comentário no topo do arquivo,
as respostas:

1. Por que o `task db:reset` deixou tudo `cursando`? Proponha uma correção.
2. Se a regra de aprovação mudar para nota 7, você edita a 0003 ou cria a 0004? Por quê?
