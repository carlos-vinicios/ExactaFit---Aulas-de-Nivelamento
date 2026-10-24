# M4: banco de dados das Aulas 3, 4 e 5

Pasta do repositório da turma com o projeto de apoio às aulas de banco de dados. Tem o banco
de exemplo de uma escola, scripts para criar o banco e rodar arquivos SQL, as migrações do
Alembic e os exercícios.

| Aula | Tema | Exercícios |
|---|---|---|
| 3 | Modelo relacional: entidades, chaves, cardinalidade e SQL | `exercicios/aula3` |
| 4 | SQL na prática: operações e relações entre tabelas | `exercicios/aula4` |
| 5 | SQLite e PostgreSQL, migrações e automação com Task | `exercicios/aula5` |

## Preparação

Requisitos: Python 3.13 instalado com pyenv (`pyenv install 3.13.0`; o arquivo
`.python-version`, na raiz do repositório, seleciona a versão em todas as pastas). Para a
Aula 5, também o [Docker](https://docs.docker.com/get-started/get-docker/) (ou o PostgreSQL
instalado na máquina) e o [Task](https://taskfile.dev/docs/installation).

O ambiente virtual fica na raiz do repositório (é o `.venv` que o VS Code procura) e serve
para o M3 e o M4. Os comandos deste módulo rodam dentro da pasta `M4`:

```bash
cd ExactaFit---Aulas-de-Nivelamento       # raiz do repositório
git pull                                  # traz a versão mais recente das aulas
python --version                          # 3.13.0
python -m venv .venv                      # só se o .venv ainda não existir
source .venv/bin/activate                 # Windows (PowerShell): .venv\Scripts\Activate.ps1
cd M4
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python ferramentas/criar_banco.py         # cria escola.db com esquema e dados
```

| Arquivo | Conteúdo |
|---|---|
| `requirements.txt` | o que o projeto precisa para executar: Alembic, SQLAlchemy e psycopg (Aula 5) |
| `requirements-dev.txt` | `-r requirements.txt` e as ferramentas de desenvolvimento: ruff e mypy |

Os dois arquivos foram gerados com `pip freeze` e têm versões exatas.

Abra a pasta do repositório no VS Code e aceite as extensões recomendadas. Todos os comandos
deste arquivo são executados a partir da pasta `M4`, com o ambiente ativo.

## Scripts da pasta ferramentas

```bash
python ferramentas/criar_banco.py [arquivo.db]                     # SQLite com esquema e dados
python ferramentas/sql.py escola.db consulta.sql                   # executa um .sql e mostra os resultados
python ferramentas/sql.py :memory: esquema.sql --continuar conf.sql  # banco em memória; depois de --continuar, não para no erro
python ferramentas/semear.py                                       # dados num banco já migrado (DATABASE_URL)
```

No `sql.py`, o banco pode ser um arquivo SQLite, `:memory:` ou uma URL
`postgresql://usuario:senha@host:porta/banco`. Os scripts importam funções de
`ferramentas/banco.py`; isso funciona porque o Python coloca a pasta do script em
`sys.path[0]`, como vimos na Aula 1.

## O banco da escola

```mermaid
erDiagram
    CURSO ||--o{ ALUNO : tem
    CURSO ||--o{ DISCIPLINA : oferece
    DISCIPLINA ||--o{ TURMA : "abre"
    PROFESSOR ||--o{ TURMA : leciona
    ALUNO ||--o{ MATRICULA : faz
    TURMA ||--o{ MATRICULA : recebe
```

| Tabela | Linhas | Observação |
|---|---|---|
| curso | 3 | CC, SI e ES |
| professor | 9 | Otávio Rezende ainda não tem turmas |
| disciplina | 13 | CC301 Compiladores não tem turma |
| turma | 18 | 12 em 2026.1 e 6 em 2026.2 |
| aluno | 45 | 3 ingressaram em agosto e ainda não têm matrícula |
| matricula | 210 | notas de 2026.1 lançadas; 2026.2 ainda sem nota (NULL) |

O esquema está em `dados/escola_esquema.sql` (SQLite, Aulas 3 e 4) e em
`migracoes/versions/0001_esquema_inicial.py` (Alembic, Aula 5). Os dados ficam em
`dados/escola_dados.sql`, gerado por `ferramentas/gerar_dados.py`, e funcionam nos dois bancos.

## Exercícios

Cada prática tem um enunciado e uma forma de conferir o resultado, sem testes automatizados:

| Pasta | O que fazer | Como conferir |
|---|---|---|
| `aula3/p1_modelagem` | modelo ER da biblioteca em Mermaid (`modelo.md`) | pré-visualização do Mermaid |
| `aula3/p2_normalizacao` | anomalias e formas normais de uma planilha (`respostas.md`) | discussão em aula |
| `aula3/p3_ddl` | esquema da biblioteca em SQL (`biblioteca.sql`) | `conferencia.sql` e `conferencia_esperada.txt` |
| `aula3/desafio` | reservas com índice único parcial | `conferencia.sql` e `conferencia_esperada.txt` |
| `aula4/p1_consultas` | consultas simples e alterações (q01 a q08) | resultado esperado no topo de cada arquivo |
| `aula4/p2_juncoes` | junções, agregação e subconsultas (q09 a q16) | resultado esperado no topo de cada arquivo |
| `aula4/p3_python` | SQL a partir do Python com parâmetros (`consultas.py`) | saída esperada na docstring |
| `aula4/desafio` | ranking por curso com funções de janela | resultado esperado no topo do arquivo |
| `aula5/p1_postgres` | PostgreSQL com Docker, psql e comparação com o SQLite | `respostas.md` |
| `aula5/p2_migracoes` | primeira revisão do Alembic (`migracoes/versions/`) | `conferir.sql` e saídas no enunciado |
| `aula5/p3_task` | completar o `Taskfile.yml` da pasta M4 | `task --list` e `task --dry` |
| `aula5/desafio` | migração com dados: situação da matrícula | `conferir.sql` e saída no enunciado |

## PostgreSQL (Aula 5)

```bash
cp .env.exemplo .env              # Windows: copy .env.exemplo .env
docker compose up -d --wait
# Linux e macOS
export DATABASE_URL=postgresql+psycopg://escola:escola@localhost:5432/escola
# Windows (PowerShell)
$env:DATABASE_URL = "postgresql+psycopg://escola:escola@localhost:5432/escola"
alembic upgrade head
python ferramentas/semear.py
docker compose exec db psql -U escola -d escola
```

Depois da Prática 3, os mesmos passos viram `task db:up` e `task db:reset`.
