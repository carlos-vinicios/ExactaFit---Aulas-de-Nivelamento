# M7: API REST (Aulas 8, 9 e 10)

A API da secretaria da escola. O sistema é o mesmo do M5, com as camadas de serviço, manager e
acesso a dados prontas; o M7 acrescenta uma segunda camada de apresentação, `secretaria/api`, que
recebe pedidos HTTP e chama os mesmos serviços que as telas do terminal chamam.

```text
M7/
├── secretaria/
│   ├── api/               a camada de apresentação HTTP (M7)
│   │   ├── app.py         a aplicação FastAPI: junta as rotas (Aula 9)
│   │   ├── schemas.py     o contrato: o JSON que entra e que sai (Aula 8)
│   │   ├── exemplos.py    mostra o JSON de cada schema de saída (Aula 8)
│   │   ├── dependencias.py  parâmetros que várias rotas compartilham (Aula 9)
│   │   ├── rotas/         alunos.py, turmas.py, cursos.py: uma rota por caso de uso (Aula 9)
│   │   │                  documentos.py: exemplo pronto de upload e download (Aula 9)
│   │   └── erros.py       as respostas de erro: 404, 409, 422, 503 e 500 (Aula 10)
│   ├── apresentacao/      as telas do terminal do M5, que continuam funcionando
│   ├── servicos/          os casos de uso (M5)
│   ├── managers/          as regras da escola (M5)
│   ├── acesso_orm/        o acesso a dados com o SQLAlchemy (M5)
│   ├── acesso_arquivos/   o acesso aos documentos guardados em M7/documentos (Aula 9)
│   ├── dominio.py, erros.py, schemas.py, config.py
├── ferramentas/
│   ├── biblioteca.py      uma API de exemplo, com os dados na memória (Aula 8)
│   ├── espera.py          demonstração de def e async def (Aula 9)
│   └── medir.py           vários pedidos ao mesmo tempo em cada rota de espera.py (Aula 9)
└── exercicios/            enunciados e arquivos .http das práticas
```

As camadas de baixo vêm do gabarito do M5 (fim da Aula 7, com os desafios), com dois acréscimos
nos serviços: `consultas.consultar_matricula`, para a rota de uma matrícula, e o tipo
`SiglaCurso` em `schemas.py`. A camada `acesso_dados` (sqlite3) saiu: a API usa o ORM. O exemplo
de documentos da Aula 9 acrescenta, já pronto, uma rota, um serviço, um manager e a camada
`acesso_arquivos`.

## Preparação

O ambiente virtual é o mesmo dos outros módulos, na raiz do repositório. Os comandos deste módulo
rodam dentro da pasta `M7`:

```bash
cd ExactaFit---Aulas-de-Nivelamento       # raiz do repositório
git pull
source .venv/bin/activate                 # Windows (PowerShell): .venv\Scripts\Activate.ps1
cd M7
pip install -r requirements-dev.txt
python ../M4/ferramentas/criar_banco.py escola.db
```

No VS Code, instale a extensão recomendada **REST Client** (`humao.rest-client`). Ela abre os
arquivos `.http` das práticas: cada pedido ganha um link "Send Request", e a resposta aparece ao
lado, com a linha de status, os cabeçalhos e o corpo.

## Os servidores

| Servidor | Comando (na pasta M7) | Endereço |
|---|---|---|
| API de exemplo da biblioteca (Aula 8) | `python ferramentas/biblioteca.py` | http://127.0.0.1:8001 |
| API da secretaria (Aulas 9 e 10) | `uvicorn secretaria.api.app:app --reload` | http://127.0.0.1:8000 |
| Demonstração de def e async def (Aula 9) | `python ferramentas/espera.py` | http://127.0.0.1:8002 |

Com o servidor da secretaria no ar, a documentação automática fica em
http://127.0.0.1:8000/docs. O `--reload` reinicia o servidor a cada arquivo salvo. Para parar,
`Ctrl+C` no terminal do servidor.

O banco é o da variável `DATABASE_URL`, como no M5. Sem ela, é o `escola.db` da pasta `M7`. Para
recomeçar com os dados originais, rode o `criar_banco.py` de novo.

## Demonstração: def e async def (Aula 9)

Suba `python ferramentas/espera.py` num terminal e deixe aberto. Noutro terminal:

1. Chame `curl http://127.0.0.1:8002/async-bloqueia` e, enquanto ele espera (5 s), chame
   `curl http://127.0.0.1:8002/agora` num terceiro terminal: `/agora` também fica parada, porque
   o servidor inteiro travou. Repita com `/def` e com `/async-espera`: `/agora` responde na hora.
2. Rode `python ferramentas/medir.py`: 5 pedidos de 1 s ao mesmo tempo em cada rota.

```text
5 pedidos de 1 segundo ao mesmo tempo em cada rota
/def             terminaram em (s): 1.0  1.0  1.0  1.0  1.0   total: 1.0 s
/async-bloqueia  terminaram em (s): 1.0  2.0  3.0  4.0  5.0   total: 5.0 s
/async-espera    terminaram em (s): 1.0  1.0  1.0  1.0  1.0   total: 1.0 s
```

Para essa demonstração, use terminais (ou o `medir.py`): o REST Client e o /docs mandam um
pedido por vez, e o navegador costuma segurar abas com o mesmo endereço até a primeira responder.

## O contrato da API

| Método | Caminho | Corpo | Sucesso |
|---|---|---|---|
| GET | `/alunos/{matricula}/boletim` | | 200, `BoletimSaida` |
| GET | `/turmas/{codigo}/{semestre}` | | 200, `RelatorioTurmaSaida` |
| GET | `/turmas/{codigo}/{semestre}/matriculas/{matricula}` | | 200, `MatriculaSaida` |
| PUT | `/turmas/{codigo}/{semestre}/matriculas/{matricula}/nota` | `NotaEntrada` | 200, `MatriculaSaida` |
| POST | `/turmas/{codigo}/{semestre}/matriculas` | `MatriculaEntrada` | 201, `MatriculaSaida` e `Location` |
| DELETE | `/turmas/{codigo}/{semestre}/matriculas/{matricula}` | | 204, sem corpo |
| GET | `/cursos/{sigla}/ranking?semestre=2026.1&top=3` | | 200, `RankingSaida` |

As rotas de documentos (`/alunos/{matricula}/documentos`) já vêm prontas: são o exemplo de upload
e download da Aula 9 (`exercicios/aula9/exemplo_documentos`).

Erros, a partir da Aula 10: 404 (não encontrado), 409 (regra da escola), 422 (entrada fora do
formato) e 503 (banco indisponível), todos com o schema `Erro`.

## Práticas

As práticas não usam testes automatizados: cada enunciado traz as respostas esperadas, e os
arquivos `.http` trazem os pedidos. Procure os `TODO` no código.

| Aula | Pasta | O que fazer |
|---|---|---|
| 8 | `exercicios/aula8/p1_http` | conversar com a API da biblioteca: métodos, caminhos, corpos e códigos |
| 8 | `exercicios/aula8/p2_contrato` | propor o contrato da API da secretaria (`CONTRATO.md`) |
| 8 | `exercicios/aula8/p3_schemas` | converter o domínio nos schemas de saída (`api/schemas.py`) |
| 8 | `exercicios/aula8/desafio` | contrato e schema da lista paginada de alunos |
| 9 | `exercicios/aula9/p1_primeira_rota` | o boletim pela API, e a documentação em /docs |
| 9 | `exercicios/aula9/p2_leitura` | relatório da turma, matrícula e ranking, com dependência e parâmetros de consulta |
| 9 | `exercicios/aula9/p3_escrita` | lançar nota (PUT), matricular (POST) e cancelar (DELETE) |
| 9 | `exercicios/aula9/exemplo_documentos` | exemplo pronto, sem TODO: upload e download de arquivos pelas camadas |
| 9 | `exercicios/aula9/desafio` | a lista paginada de alunos, em todas as camadas |
| 10 | `exercicios/aula10/p1_404` | o schema `Erro` e o 404 |
| 10 | `exercicios/aula10/p2_422` | o 422 em português, campo a campo |
| 10 | `exercicios/aula10/p3_409_503_500` | regras (409), banco fora do ar (503), erro inesperado (500) e /docs |
| 10 | `exercicios/aula10/desafio` | todo erro no mesmo formato, inclusive os do FastAPI |
| 10 | `exercicios/aula10/desafio_extra` | uma API separada de modelos: OCR de documentos e previsão de nota (porta 8003) |

Para conferir estilo e tipos: `ruff check .` e `mypy --strict secretaria`.

## Referências

- MDN, visão geral do HTTP: https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Guides/Overview
- MDN, códigos de status: https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Reference/Status
- FastAPI, tutorial: https://fastapi.tiangolo.com/pt/tutorial/
- REST Client: https://marketplace.visualstudio.com/items?itemName=humao.rest-client
