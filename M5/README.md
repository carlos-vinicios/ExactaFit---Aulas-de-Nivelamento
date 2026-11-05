# M5: arquitetura em camadas (Aulas 6 e 7)

O sistema da secretaria da escola, organizado em camadas, sobre o mesmo banco do M4. Cada camada
é uma pasta dentro do pacote `secretaria`, e cada assunto é um arquivo dentro da camada:

```text
M5/
├── secretaria/
│   ├── apresentacao/      telas do terminal: leem o que foi digitado e imprimem
│   │   ├── terminal.py    o que é comum às telas: argumentos, mensagens de erro, formatação
│   │   ├── boletim.py     python -m secretaria.apresentacao.boletim 2025001
│   │   ├── turma.py       (Aula 6, Prática 2)
│   │   ├── lancar_nota.py (Aula 6, Prática 3)
│   │   └── matricular.py  (Aula 7, Prática 3)
│   ├── servicos/          um caso de uso por função; abre o banco e decide a transação
│   │   ├── buscas.py      aluno, turma e matrícula que precisam existir
│   │   ├── consultas.py   boletim e relatório da turma
│   │   ├── notas.py       lançamento de nota
│   │   └── matriculas.py  matrícula (Aula 7)
│   ├── managers/          regras de negócio, sem banco e sem terminal
│   │   ├── avaliacao.py   situação, média e regras do lançamento
│   │   ├── relatorios.py  boletim e relatório da turma
│   │   └── matriculas.py  regras da matrícula (Aula 7)
│   ├── acesso_dados/      o único lugar com SQL (sqlite3, Aula 6)
│   │   ├── __init__.py    a interface da camada: o que os serviços podem usar
│   │   ├── conexao.py     abrir(): conexão, commit e rollback
│   │   └── alunos.py, turmas.py, matriculas.py
│   ├── acesso_orm/        a mesma interface com o SQLAlchemy ORM (Aula 7)
│   │   ├── modelos/       os modelos da Aula 5, um por arquivo
│   │   └── conexao.py, alunos.py, turmas.py, matriculas.py
│   ├── dominio.py         os tipos que circulam entre as camadas (dataclasses)
│   ├── erros.py           as exceções do sistema
│   ├── schemas.py         schemas de entrada com Pydantic (Aula 7)
│   └── config.py          banco (DATABASE_URL) e semestre em andamento
└── exercicios/            enunciados das práticas e dos desafios
```

Cada camada chama só a de baixo: apresentação, serviço, manager e acesso a dados. As camadas
conversam pelos tipos de `dominio.py`, e o banco não sai da camada de acesso a dados.

## Preparação

O ambiente virtual é o mesmo do M3 e do M4, na raiz do repositório. Os comandos deste módulo
rodam dentro da pasta `M5`:

```bash
cd ExactaFit---Aulas-de-Nivelamento       # raiz do repositório
git pull
source .venv/bin/activate                 # Windows (PowerShell): .venv\Scripts\Activate.ps1
cd M5
pip install -r requirements-dev.txt
python ../M4/ferramentas/criar_banco.py escola.db
python -m secretaria.apresentacao.boletim 2025001
```

O banco é o da escola, criado pelo script do M4 dentro da pasta `M5`. Para recomeçar com os dados
originais, rode o `criar_banco.py` de novo.

| Arquivo | Conteúdo |
|---|---|
| `requirements.txt` | o que o sistema precisa para executar: SQLAlchemy, psycopg e Pydantic |
| `requirements-dev.txt` | `-r requirements.txt` e as ferramentas de desenvolvimento: ruff e mypy |

## Telas

Cada tela é um módulo da pasta `apresentacao`, rodado com `python -m` a partir da pasta `M5`:

```bash
python -m secretaria.apresentacao.boletim 2025001                  # boletim de um aluno
python -m secretaria.apresentacao.turma CC201 2026.1               # relatório da turma (Aula 6)
python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 8.5   # lança uma nota (Aula 6)
python -m secretaria.apresentacao.matricular 2026005 CC102 2026.2  # matrícula (Aula 7)
```

O semestre em andamento é `2026.2` (`config.py`): as notas de 2026.1 já estão lançadas, e só se
lança nota ou se matricula no semestre em andamento.

## PostgreSQL (Aula 7)

Depois da troca para o ORM, o sistema usa o banco da variável `DATABASE_URL`. O PostgreSQL e as
migrações continuam no M4:

```bash
cd ../M4
docker compose up -d --wait
export DATABASE_URL=postgresql+psycopg://escola:escola@localhost:5432/escola
# Windows (PowerShell): $env:DATABASE_URL = "postgresql+psycopg://escola:escola@localhost:5432/escola"
alembic downgrade base && alembic upgrade head && python ferramentas/semear.py
cd ../M5
python -m secretaria.apresentacao.turma CC201 2026.1
```

A variável vale só no terminal em que foi definida; num terminal novo, volta o `escola.db`.

## Práticas

As práticas não usam testes automatizados: cada enunciado traz a saída esperada das telas.
Procure os `TODO` no código; enquanto falta algo, a tela avisa `ainda não implementado`.

| Aula | Pasta | O que fazer |
|---|---|---|
| 6 | `exercicios/aula6/p1_mapa` | seguir uma chamada pelas camadas (`MAPA.md`) e propor a estrutura do relatório da turma (`PROPOSTA.md`) |
| 6 | `exercicios/aula6/p2_relatorio_turma` | relatório da turma, do acesso a dados ao serviço |
| 6 | `exercicios/aula6/p3_lancar_nota` | lançamento de nota, com a transação no serviço |
| 6 | `exercicios/aula6/desafio` | ranking por curso, da proposta ao código |
| 7 | `exercicios/aula7/p1_schema` | schema `LancamentoNota` com Pydantic, na entrada da apresentação |
| 7 | `exercicios/aula7/p2_orm` | trocar a camada de acesso a dados pelo ORM |
| 7 | `exercicios/aula7/p3_matricular` | matrícula, da proposta à escrita pelo ORM |
| 7 | `exercicios/aula7/desafio` | cancelar matrícula |

Para conferir estilo e tipos: `ruff check .` e `mypy --strict secretaria`.

## Referências

- Python, `dataclasses`: https://docs.python.org/pt-br/3/library/dataclasses.html
- Python, módulos e pacotes: https://docs.python.org/pt-br/3/tutorial/modules.html#packages
- SQLAlchemy 2.1, ORM Quick Start: https://docs.sqlalchemy.org/en/21/orm/quickstart.html
- Pydantic, Models: https://docs.pydantic.dev/latest/concepts/models/
