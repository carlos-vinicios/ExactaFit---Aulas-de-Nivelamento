# modelo_de_dados: o banco da escola em classes Python (Aula 5)

Os modelos do SQLAlchemy descrevem, no código, as tabelas que as migrações criam no banco. Cada
modelo fica num arquivo, como num sistema real:

```text
modelo_de_dados/
├── modelos/                 um modelo por tabela
│   ├── __init__.py          reúne os modelos: from modelo_de_dados.modelos import Aluno
│   ├── base.py              Base, a classe de que todos os modelos herdam
│   ├── curso.py             Curso
│   ├── aluno.py             Aluno
│   ├── professor.py         Professor
│   ├── disciplina.py        Disciplina
│   ├── turma.py             Turma
│   └── matricula.py         Matricula (chave primária composta)
├── conexao.py               engine e Sessao, a partir de DATABASE_URL
├── uso_consultas.py         select(), where(), order_by() e contagem
├── uso_relacionamentos.py   aluno.curso, aluno.matriculas, professor.turmas
└── uso_alteracoes.py        inserir, alterar e apagar, com rollback no fim
```

## Como rodar

A partir da pasta M4, com o `.venv` ativo e o banco migrado e semeado:

```bash
alembic upgrade head
python ferramentas/semear.py
python -m modelo_de_dados.uso_consultas
python -m modelo_de_dados.uso_relacionamentos
python -m modelo_de_dados.uso_alteracoes
```

O `-m` roda o arquivo como módulo do pacote `modelo_de_dados`: a pasta atual (M4) entra no
`sys.path`, e os imports usam o nome completo, como `from modelo_de_dados.modelos import Aluno`.

O banco é o da variável `DATABASE_URL`, a mesma do Alembic. Sem ela, é o `escola.db` (SQLite).
Os scripts dão o mesmo resultado no SQLite e no PostgreSQL.

## Modelo e migração

O Alembic cria e altera as tabelas; o modelo diz ao programa como elas são. Os dois precisam
andar juntos: uma coluna que existe no modelo e não existe no banco dá erro na primeira consulta
(`no such column`). Por isso, a migração e a mudança no modelo entram no mesmo commit.

## Referências

- SQLAlchemy 2.1, ORM Quick Start: https://docs.sqlalchemy.org/en/21/orm/quickstart.html
- Declaração de modelos com `Mapped`: https://docs.sqlalchemy.org/en/21/orm/declarative_tables.html
- Relacionamentos (`relationship`, `back_populates`): https://docs.sqlalchemy.org/en/21/orm/basic_relationships.html
- Sessão (`Session`, `begin`, `flush`, `commit`): https://docs.sqlalchemy.org/en/21/orm/session_basics.html
