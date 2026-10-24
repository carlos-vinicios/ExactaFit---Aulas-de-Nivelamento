# Prática 1: PostgreSQL rodando, o mesmo banco nos dois SGBDs

Ao final desta prática você terá o banco da escola criado pelas migrações no SQLite e no
PostgreSQL, e terá comparado como os dois reagem ao mesmo SQL.

## 1. Subir o PostgreSQL

### Com Docker (recomendado)

Instale o [Docker Desktop](https://docs.docker.com/get-started/get-docker/) (Windows e macOS)
ou o Docker Engine (Linux). Na pasta M4:

```bash
docker compose up -d --wait     # baixa a imagem postgres:18 na primeira vez
docker compose ps               # o serviço db deve aparecer como healthy
```

O `docker-compose.yml` cria o usuário `escola`, com senha `escola`, dono do banco `escola`,
na porta 5432.

### Sem Docker

Instale o PostgreSQL 18 pelo [instalador oficial](https://www.postgresql.org/download/)
(Windows: instalador da EDB; macOS: [Postgres.app](https://postgresapp.com); Linux: pacote da
distribuição ou repositório PGDG). Depois, como superusuário `postgres`, crie o usuário e o banco:

```sql
CREATE ROLE escola LOGIN PASSWORD 'escola';
CREATE DATABASE escola OWNER escola;
```

## 2. Conhecer o psql

```bash
docker compose exec db psql -U escola -d escola
```

(sem Docker: `psql -U escola -h localhost -d escola`)

| Comando | O que faz |
|---|---|
| `\l` | lista os bancos |
| `\dt` | lista as tabelas do banco atual |
| `\d nome` | descreve uma tabela: colunas, tipos, índices, chaves |
| `\x` | alterna a exibição em colunas ou em registros |
| `\?` | ajuda dos comandos com barra |
| `\h CREATE TABLE` | ajuda de um comando SQL |
| `\q` | sai |

Rode `\dt`. O banco ainda está vazio: quem cria as tabelas são as migrações.

## 3. Criar o banco pelas migrações, nos dois SGBDs

O Alembic e o script `ferramentas/semear.py` usam o banco da variável de ambiente `DATABASE_URL`. Sem ela,
usam o SQLite `escola.db`. Abra dois terminais no VS Code (botão `+` do painel): um para o
SQLite e outro para o PostgreSQL. Nos dois, ative o `.venv`.

No terminal do SQLite:

```bash
# apague o escola.db das aulas anteriores, que foi criado sem migrações
alembic upgrade head
python ferramentas/semear.py
```

No terminal do PostgreSQL, defina a variável só para esse terminal e repita:

```bash
# Linux e macOS
export DATABASE_URL=postgresql+psycopg://escola:escola@localhost:5432/escola
# Windows (PowerShell)
$env:DATABASE_URL = "postgresql+psycopg://escola:escola@localhost:5432/escola"

alembic upgrade head
python ferramentas/semear.py
```

Para conferir qual banco um terminal está usando: `alembic current -v` mostra a URL usada.

Volte ao psql e rode `\dt`, `\d aluno` e `SELECT * FROM alembic_version;`. Compare a coluna
`id` de `aluno` com o que você escreveu na Aula 3.

## 4. Comparar os dois bancos

1. Leia `comparacao.sql` e preencha a coluna **Previsão** de `respostas.md` antes de rodar.
2. Rode o arquivo nos dois bancos:

   ```bash
   python ferramentas/sql.py escola.db --continuar exercicios/aula5/p1_postgres/comparacao.sql
   python ferramentas/sql.py postgresql://escola:escola@localhost:5432/escola --continuar exercicios/aula5/p1_postgres/comparacao.sql
   ```

3. Preencha as colunas de resultado e a explicação de cada caso.

## 5. Opcional: PostgreSQL dentro do VS Code

A extensão [PostgreSQL](https://marketplace.visualstudio.com/items?itemName=ms-ossdata.vscode-pgsql)
da Microsoft conecta no banco, mostra as tabelas numa árvore e executa consultas com
autocompletar. Crie uma conexão com servidor `localhost`, usuário `escola`, senha `escola` e
banco `escola`.

## Referências

* Imagem oficial no Docker Hub: <https://hub.docker.com/_/postgres>
* Documentação do psql: <https://www.postgresql.org/docs/current/app-psql.html>
* Tipos de dados do PostgreSQL: <https://www.postgresql.org/docs/current/datatype.html>
* Tipagem flexível do SQLite: <https://www.sqlite.org/flextypegood.html>
