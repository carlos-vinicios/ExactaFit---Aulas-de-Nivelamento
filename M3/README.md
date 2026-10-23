# aula-python: exercícios das Aulas 1 e 2

- **Aula 1:** introdução ao Python, VS Code, ambientes e dependências, módulos e pacotes.
- **Aula 2:** classes, tipos, funções, tratamento de erros e leitura de código existente.

Os exercícios usam só a biblioteca padrão. Os dados ficam em arquivos CSV e JSON.

```text
aula-python/
├── .python-version        versão do Python usada pelo pyenv nesta pasta (3.13.0)
├── .gitignore             o que não vai para o Git (.venv, caches)
├── requirements.txt       pacotes para EXECUTAR (vazio: só biblioteca padrão)
├── requirements-dev.txt   pacotes para DESENVOLVER: mypy e ruff, com versões exatas
├── .vscode/               extensões recomendadas, configurações e depuração
└── exercicios/
    ├── aula1/
    │   ├── p1_vscode/     tour pelo VS Code
    │   ├── p2_ambiente/   ambiente virtual e um relatório com quatro etapas quebradas
    │   └── p3_imports/    módulos, pacotes e sys.path
    └── aula2/
        ├── p1_funcoes/    funções sobre a turma (turma.json)
        ├── p2_erros/      leitura tolerante a erros e configuração em JSON
        ├── p3_legado/     análise de um script legado
        ├── casa_recursos/ para casa: classe, decorador e gerador
        └── desafio/       relatório da turma reescrito
```

## 1. Instalar o Python 3.13 com pyenv

| Sistema | Instalação do pyenv |
|---|---|
| Windows | [pyenv-win](https://github.com/pyenv-win/pyenv-win), comando de instalação no README do projeto; depois `pyenv update` |
| Linux | `curl -fsSL https://pyenv.run \| bash` e as dependências de compilação da [wiki do pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) |
| macOS | `brew install pyenv` |
| Windows com WSL | [instale o WSL](https://learn.microsoft.com/pt-br/windows/wsl/install) e siga os passos de Linux |

```bash
pyenv install 3.13.0
cd aula-python
python --version          # 3.13.0, escolhido pelo arquivo .python-version
```

Se a versão não aparecer, rode `pyenv local 3.13.0` dentro da pasta.

## 2. Criar o ambiente virtual e instalar as dependências

```bash
python -m venv .venv
# Linux e macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

`requirements-dev.txt` começa com `-r requirements.txt`: instalar o arquivo de desenvolvimento
também instala o de execução. Para conferir o que ficou instalado: `pip freeze`.

No PowerShell, se a ativação for bloqueada:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

No VS Code: `Ctrl+Shift+P` > **Python: Select Interpreter** > o `.venv` desta pasta.

Todos os comandos abaixo são executados a partir da pasta `aula-python`, com o ambiente ativo.

## 3. Aula 1

| Prática | Tema | Onde |
|---|---|---|
| 1 | Tour pelo VS Code | `exercicios/aula1/p1_vscode/tour.py` |
| 2 | Ambiente e depuração | `exercicios/aula1/p2_ambiente/` |
| 3 | Módulos, pacotes e `import` | `exercicios/aula1/p3_imports/` |

### Prática 2: ambiente e etapas quebradas

`relatorio.py` gera o relatório da turma em quatro etapas, e cada etapa tem um defeito.

1. Antes de criar o ambiente, tente `ruff check exercicios/aula1/p2_ambiente`. O que acontece?
2. Crie o ambiente, instale `requirements-dev.txt` e selecione o interpretador (seção 2).
3. Rode o relatório: `python exercicios/aula1/p2_ambiente/relatorio.py`.
4. Use `ruff check exercicios/aula1/p2_ambiente` e `mypy exercicios/aula1/p2_ambiente/relatorio.py`
   para encontrar os defeitos das etapas 2 e 3.
5. Use o depurador (F9, F5 com **Prática 2: relatório da turma**, F10 e o painel Variables)
   para encontrar os defeitos das etapas 1 e 4.
6. Confira a saída: os 10 alunos e `Média da turma: 6.60`.
7. Rode `pip freeze` e compare com `requirements-dev.txt`.

### Prática 3: imports

```bash
cd exercicios/aula1/p3_imports
python calculadora/principal.py       # funciona
python -m calculadora.principal       # falha: compare o sys.path[0] impresso
python calculadora/operacoes.py       # observe o valor de __name__
cd sombra
python sorteio.py                     # o que acontece?
```

## 4. Aula 2

| Prática | Tema | Como verificar |
|---|---|---|
| 1 | Tipos e funções | `python exercicios/aula2/p1_funcoes/funcoes.py` |
| 2 | Tratamento de erros | `python exercicios/aula2/p2_erros/erros.py` |
| 3 | Análise do código legado | `exercicios/aula2/p3_legado/PERGUNTAS.md` |
| Casa | Classe, decorador e gerador | `python exercicios/aula2/casa_recursos/recursos.py` |

Nas práticas 1 e 2 e na atividade para casa, complete as funções marcadas com `TODO` e compare a saída do programa com
a saída esperada escrita no início de cada arquivo. As seções ainda não implementadas
aparecem como "ainda não implementada". Confira também os tipos:

```bash
mypy exercicios/aula2/p1_funcoes/funcoes.py
mypy exercicios/aula2/p2_erros/erros.py
mypy exercicios/aula2/casa_recursos/recursos.py
```

### Desafio: relatório da turma reescrito

Reescreva o script da Prática 3 em `exercicios/aula2/desafio/relatorio.py`, corrigindo os
problemas encontrados. Requisitos e saída esperada em `exercicios/aula2/desafio/README.md`.

## 5. Referências

- Tutorial oficial, Ambientes virtuais e pacotes: https://docs.python.org/pt-br/3/tutorial/venv.html
- pip, arquivos de requisitos: https://pip.pypa.io/en/stable/user_guide/#requirements-files
- Tutorial oficial, Módulos: https://docs.python.org/pt-br/3/tutorial/modules.html
- Tutorial oficial, Classes (inclui iteradores e geradores): https://docs.python.org/pt-br/3/tutorial/classes.html
- Tutorial oficial, Erros e exceções: https://docs.python.org/pt-br/3/tutorial/errors.html
- Módulo json: https://docs.python.org/pt-br/3/library/json.html
- Módulo csv: https://docs.python.org/pt-br/3/library/csv.html
- Python no VS Code: https://code.visualstudio.com/docs/python/python-tutorial
- Exercism, trilha de Python: https://exercism.org/tracks/python
