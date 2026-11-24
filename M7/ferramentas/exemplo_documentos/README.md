# Aula 9, exemplo: upload e download de documentos

Um exemplo pronto, para ler e experimentar: rotas que recebem e devolvem arquivos. A secretaria
passa a guardar documentos dos alunos (um atestado, um comprovante), em PDF, PNG ou JPEG.

| Método | Caminho | Corpo | Sucesso |
|---|---|---|---|
| POST | `/alunos/{matricula}/documentos` | multipart/form-data, campo `arquivo` | 201, `DocumentoSaida` e `Location` |
| GET | `/alunos/{matricula}/documentos` | | 200, `list[DocumentoSaida]` |
| GET | `/alunos/{matricula}/documentos/{nome}` | | 200, o próprio arquivo |

## O fluxo, camada por camada

O upload segue o mesmo caminho das outras rotas; só o formato do corpo e o lugar onde os dados
ficam mudam:

1. **Cliente**: envia o pedido com `Content-Type: multipart/form-data`. O corpo tem partes
   separadas por uma linha de fronteira (`--limite`); a parte `arquivo` traz o nome, o tipo e os
   bytes do arquivo. É o mesmo formato de um formulário HTML com campo de arquivo.
2. **FastAPI** (com o pacote `python-multipart`): lê as partes e entrega o arquivo à rota como
   `UploadFile`, com `filename`, `content_type` e `file`. Se o campo `arquivo` faltar, responde
   422 antes da rota.
3. **Rota** (`api/rotas/documentos.py`): lê os bytes (`arquivo.file.read()`, porque a rota é
   `def`) e chama o serviço com a matrícula, o nome, o tipo e o conteúdo. Não decide nada.
4. **Serviço** (`servicos/documentos.py`): limpa o nome, confere no banco se o aluno existe, pede
   ao manager que confira as regras e manda gravar.
5. **Manager** (`managers/documentos.py`): as regras da escola. Só PDF, PNG ou JPEG, com extensão
   que corresponda ao tipo, de até 2 MB, sem repetir o nome. E o nome nunca vira caminho:
   `../../config.py` vira `config.py`.
6. **Acesso a arquivos** (`acesso_arquivos/`): uma camada de acesso a dados em que os dados ficam
   numa pasta, e não no banco: `documentos/2025001/atestado.pdf`. Devolve um `Documento` de
   `dominio.py`; nenhum caminho de arquivo sai dela.
7. **Rota de novo**: converte o `Documento` em `DocumentoSaida` (JSON) e responde 201 com
   `Location`. No download, responde com os bytes, o tipo de mídia (`application/pdf`) e o
   cabeçalho `Content-Disposition`, que manda o navegador baixar o arquivo com esse nome.

## Experimente

O `requirements.txt` ganhou o pacote `python-multipart`. Instale de novo, na pasta `M7`:

```bash
pip install -r requirements-dev.txt
```

Suba a API e envie os pedidos de `documentos.http`, em ordem. O pedido 1 manda o arquivo
`atestado.pdf` desta pasta; a linha `< ./atestado.pdf` diz ao REST Client para pôr o conteúdo do
arquivo naquele ponto do corpo. Em /docs, a rota de envio mostra um botão para escolher o arquivo.

```text
POST /alunos/2025001/documentos

HTTP/1.1 201 Created
location: /alunos/2025001/documentos/atestado.pdf

{
  "nome": "atestado.pdf",
  "tipo": "application/pdf",
  "tamanho": 684
}

GET /alunos/2025001/documentos

HTTP/1.1 200 OK

[
  {
    "nome": "atestado.pdf",
    "tipo": "application/pdf",
    "tamanho": 684
  }
]

GET /alunos/2025001/documentos/atestado.pdf

HTTP/1.1 200 OK
content-type: application/pdf
content-disposition: attachment; filename*=utf-8''atestado.pdf

(corpo binário: 684 bytes)
```

Os pedidos 4 e 5 quebram regras da escola (tipo não aceito e nome repetido): por enquanto, a API
responde 500. Depois da Aula 10, as mesmas regras respondem assim:

```text
POST /alunos/2025001/documentos

HTTP/1.1 409 Conflict

{
  "erro": "regra_de_negocio",
  "mensagem": "tipo text/plain não aceito; envie PDF, PNG ou JPEG",
  "detalhes": []
}

POST /alunos/2025001/documentos

HTTP/1.1 409 Conflict

{
  "erro": "regra_de_negocio",
  "mensagem": "o aluno já tem um documento chamado atestado.pdf",
  "detalhes": []
}
```

Os arquivos enviados ficam em `M7/documentos/` (fora do Git). Para recomeçar, apague essa pasta.

## Para pensar

* Por que a rota lê `arquivo.file.read()`, e não `await arquivo.read()`? Em que tipo de rota o
  `await` funcionaria?
* O serviço confere o aluno no banco antes de gravar o arquivo. O que aconteceria se fosse ao
  contrário e o aluno não existisse?
* O nome do arquivo vem do cliente. Por que ele não pode ir direto para o caminho no disco?
