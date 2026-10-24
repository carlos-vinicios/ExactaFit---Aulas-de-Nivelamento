# Prática 3: automação com Task

Até aqui você digitou comandos longos e precisou lembrar em qual terminal estava a variável
`DATABASE_URL`: `docker compose up -d --wait`, `alembic upgrade head`, `python ferramentas/semear.py`... O
[Task](https://taskfile.dev) guarda esses comandos com nomes curtos num arquivo
`Taskfile.yml`, que vai para o repositório junto com o código. Quem clona o projeto roda
`task` e vê tudo o que dá para fazer.

## 1. Instalar

Escolha uma opção na [página de instalação](https://taskfile.dev/docs/installation):

| Sistema | Comando |
|---|---|
| Windows | `winget install Task.Task` |
| macOS | `brew install go-task` |
| Linux | `sudo snap install task --classic` |
| Qualquer um, com Node | `npm install -g @go-task/cli` |
| Qualquer um, com Python | `pip install go-task-bin`, com o `.venv` ativo (pacote mantido pela comunidade) |

Confira com `task --version`. Para o VS Code existe a extensão
[Task](https://marketplace.visualstudio.com/items?itemName=task.vscode-task), que lista e
roda as tarefas pela barra lateral.

## 2. Explorar o Taskfile

Na pasta M4:

```bash
task                 # lista as tarefas com descrição
task setup
task --dry setup     # mostra o que seria executado, sem executar
```

Copie `.env.exemplo` para `.env`. O `dotenv: ['.env']` no topo faz o Task carregar
`DATABASE_URL` do `.env` para todas as tarefas. Por isso, dentro do Task, `python -m alembic
upgrade head` vai para o PostgreSQL sem você definir a variável no terminal.

As tarefas usam `python -m alembic`, `python -m ruff` e assim por diante: com o `.venv` ativo,
`python` é o do ambiente, e o `-m` garante que a ferramenta vem dele.

## 3. Completar as tarefas

Abra o `Taskfile.yml` da pasta M4 e escreva as tarefas marcadas com `TODO`. Cada uma precisa de
`desc` (senão não aparece em `task --list`). Recursos que você vai usar:

* `cmds`: lista de comandos, executados em ordem;
* `deps`: tarefas que rodam antes, em paralelo;
* `- task: nome` dentro de `cmds`: chama outra tarefa, em sequência;
* `interactive: true`: para comandos que leem o teclado, como o psql;
* `prompt`: pede confirmação antes de algo destrutivo (o `--yes` responde sim).

Guia de uso: <https://taskfile.dev/docs/guide>. Referência do esquema:
<https://taskfile.dev/docs/reference/schema>.

### Como conferir

Liste as tarefas. A ordem é a do Task (as tarefas com dois-pontos no nome aparecem depois):

```bash
task --list
```

```text
task: Available tasks for this project:
* check:            Tudo o que precisa passar antes de um commit
* default:          Lista as tarefas disponíveis
* setup:            Instala as dependências do projeto
* db:down:          Para o PostgreSQL (os dados ficam no volume)
* db:migrate:       Aplica as migrações pendentes no banco de DATABASE_URL
* db:psql:          Abre o psql no banco da escola
* db:reset:         Recria o banco do zero (desfaz tudo, migra e semeia)
* db:seed:          Insere os dados de exemplo
* db:up:            Sobe o PostgreSQL e espera ficar pronto
* lint:mypy:        Verifica os tipos com o mypy
* lint:ruff:        Verifica o estilo com o ruff
```

Veja, sem executar nada, o que o `db:reset` faria. O `--yes` responde ao `prompt`:

```bash
task --dry --yes db:reset
```

```text
task: [db:reset] python -m alembic downgrade base
task: [db:migrate] python -m alembic upgrade head
task: [db:seed] python ferramentas/semear.py
```

Os nomes, as descrições e os comandos podem ter outras palavras, mas a ordem do `db:reset`
precisa ser esta: desfazer, migrar, semear. Confira também que o `db:down` não usa `-v`
(`task --dry db:down`): esse parâmetro apaga o volume com os dados.

## 4. Usar de verdade

```bash
task db:up
task db:reset        # PostgreSQL do zero, com dados
task db:psql         # \dt para conferir, \q para sair
task check           # ruff e mypy, em paralelo
```

Para rodar as tarefas no SQLite, comente a linha `DATABASE_URL` do `.env`.
