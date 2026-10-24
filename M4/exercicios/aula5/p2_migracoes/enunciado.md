# Prática 2: migrações com Alembic

O projeto já tem o Alembic configurado:

| Arquivo | Papel |
|---|---|
| `alembic.ini` | onde ficam as migrações e a configuração de log |
| `migracoes/env.py` | decide em qual banco rodar: lê `DATABASE_URL` (padrão `sqlite:///escola.db`) |
| `migracoes/versions/0001_esquema_inicial.py` | cria as seis tabelas da escola |
| `migracoes/script.py.mako` | modelo usado para gerar novas revisões |

## Parte A: explorar

```bash
alembic history                  # lista as revisões
alembic current                  # revisão aplicada no banco deste terminal
alembic upgrade head --sql       # mostra o SQL sem executar
```

Abra `migracoes/versions/0001_esquema_inicial.py` e compare com o `escola_esquema.sql` da
pasta `dados/`. No psql, rode `SELECT * FROM alembic_version;`.

## Parte B: a sua primeira revisão

A secretaria precisa do telefone dos alunos e a busca por nome está lenta.

1. Crie a revisão com um id legível:

   ```bash
   alembic revision -m "telefone do aluno e índice por nome" --rev-id 0002
   ```

2. No arquivo criado em `migracoes/versions/`, escreva:
   * `upgrade()`: acrescenta a `aluno` a coluna `telefone` (texto até 20 caracteres,
     opcional) e cria o índice `ix_aluno_nome` na coluna `nome`;
   * `downgrade()`: desfaz o upgrade, na ordem inversa.

   Use `op.batch_alter_table("aluno")` para alterar colunas: no PostgreSQL vira um
   `ALTER TABLE` comum, e no SQLite o Alembic recria a tabela quando o `ALTER TABLE` do SQLite
   não dá conta.

3. Confira no SQLite. Use um terminal **sem** a variável `DATABASE_URL`, a partir da pasta
   M4. Os passos recriam o banco pela 0001, inserem os dados e então aplicam a sua
   revisão:

   ```bash
   # apague o escola.db (Windows: del escola.db; Linux e macOS: rm escola.db)
   alembic upgrade 0001
   python ferramentas/semear.py
   alembic upgrade head
   python ferramentas/sql.py escola.db exercicios/aula5/p2_migracoes/conferir.sql
   ```

   Saída esperada depois do upgrade:

   ```text
   revisao
   -------
   0002
   (1 linha)

   coluna        | tipo         | obrigatoria
   --------------+--------------+------------
   id            | INTEGER      | 1
   matricula     | VARCHAR(10)  | 1
   nome          | VARCHAR(100) | 1
   email         | VARCHAR(120) | 0
   data_ingresso | DATE         | 1
   curso_id      | INTEGER      | 1
   telefone      | VARCHAR(20)  | 0
   (7 linhas)

   indice                   | unico
   -------------------------+------
   ix_aluno_nome            | 0
   sqlite_autoindex_aluno_1 | 1
   sqlite_autoindex_aluno_2 | 1
   (3 linhas)

   alunos | matriculas
   -------+-----------
   45     | 210
   (1 linha)
   ```

   Agora desfaça e confira de novo:

   ```bash
   alembic downgrade -1
   python ferramentas/sql.py escola.db exercicios/aula5/p2_migracoes/conferir.sql
   ```

   Saída esperada depois do downgrade: revisão 0001, sem `telefone`, sem `ix_aluno_nome`,
   com os dois índices únicos e os mesmos 45 alunos e 210 matrículas.

   ```text
   revisao
   -------
   0001
   (1 linha)

   coluna        | tipo         | obrigatoria
   --------------+--------------+------------
   id            | INTEGER      | 1
   matricula     | VARCHAR(10)  | 1
   nome          | VARCHAR(100) | 1
   email         | VARCHAR(120) | 0
   data_ingresso | DATE         | 1
   curso_id      | INTEGER      | 1
   (6 linhas)

   indice                   | unico
   -------------------------+------
   sqlite_autoindex_aluno_1 | 1
   sqlite_autoindex_aluno_2 | 1
   (2 linhas)

   alunos | matriculas
   -------+-----------
   45     | 210
   (1 linha)
   ```

   Os índices `sqlite_autoindex_aluno_1` e `sqlite_autoindex_aluno_2` são as restrições
   `UNIQUE` de matrícula e e-mail. Eles precisam continuar lá depois da ida e volta: no SQLite,
   o modo batch recria a tabela, e uma migração mal escrita pode perder restrições pelo
   caminho.

   Por fim, aplique de novo com `alembic upgrade head`: uma revisão bem escrita vai e volta
   quantas vezes for preciso.

4. Aplique no PostgreSQL, no terminal com `DATABASE_URL`:

   ```bash
   alembic upgrade head
   alembic downgrade -1            # volta para a 0001
   alembic upgrade head            # e de novo para a 0002
   ```

   No psql, `\d aluno` deve mostrar a coluna nova e o índice `ix_aluno_nome`.

## Referências

* Tutorial do Alembic: <https://alembic.sqlalchemy.org/en/latest/tutorial.html>
* Operações disponíveis (`op.*`): <https://alembic.sqlalchemy.org/en/latest/ops.html>
* Modo batch para SQLite: <https://alembic.sqlalchemy.org/en/latest/batch.html>
