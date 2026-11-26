# Desafio extra da Aula 10: uma API de modelos

A coordenação quer duas coisas que não são cadastro:

* **ler documentos digitalizados** (atestados, requerimentos) e saber de qual aluno são;
* **prever a nota** de quem está cursando 2026.2, para conversar antes com quem pode reprovar.

Modelos assim costumam ficar numa **API separada** da secretaria: as dependências são pesadas
(Tesseract, scikit-learn), o OCR ocupa a CPU, e o modelo muda num ritmo diferente do cadastro. É
a ideia de serviços separados da Aula 6, com o que você já sabe de upload (Aula 9) e de erros
(Aula 10).

## O que construir

Um pacote novo, `M7/modelos_api/`, com uma aplicação FastAPI própria, na porta 8003, e as mesmas
camadas da secretaria: `api/`, `servicos/`, `managers/` e uma camada de acesso aos modelos no
lugar do banco. **A API de modelos não importa nada do pacote `secretaria`.**

| Método | Caminho | Corpo | Sucesso |
|---|---|---|---|
| POST | `/ocr` | multipart, campo `arquivo` (PNG ou JPEG) | 200: o arquivo, o texto lido e as matrículas encontradas |
| POST | `/previsoes/nota` | JSON: `frequencia` (0 a 100) e `media_anterior` (0 a 10) | 200: a nota prevista e a situação prevista |
| POST | `/previsoes/notas` | multipart, campo `arquivo`: CSV com `matricula,frequencia,media_anterior` | 200: uma previsão por linha |
| GET | `/previsoes/modelo` | | 200: a fórmula do modelo e o R² |

Requisitos:

1. **OCR**: use o Tesseract pelo pacote `pytesseract`, em português (`lang="por"`). Abra a imagem
   da memória, sem gravar no disco (`Image.open(BytesIO(conteudo))`, do Pillow). Procure no texto
   as matrículas (7 dígitos) e devolva-as numa lista, sem repetir.
2. **Regressão**: um script `python -m modelos_api.treinar <historico.csv>` treina uma
   `LinearRegression` do scikit-learn que prevê `nota_final` a partir de `frequencia` e
   `media_anterior`, separa 20% das linhas para teste (`train_test_split`, `random_state=42`),
   mostra a fórmula e o R² no teste e grava o modelo com `joblib`. A API carrega o modelo gravado:
   ela não treina a cada pedido.
3. **Regras**: a nota prevista fica entre 0 e 10, com uma casa; a situação prevista segue a regra
   da escola (aprovado a partir de 6). O OCR só aceita PNG e JPEG de até 5 MB.
4. **Erros no formato `Erro` da Aula 10**, em português: 415 para arquivo de tipo não aceito; 422
   para JSON ou CSV fora do formato (no CSV, dizendo a linha de cada problema); 503 quando o modelo
   ainda não foi treinado ou o Tesseract não está instalado.
5. **Rotas `def`**: o OCR e a previsão ocupam a CPU e usam bibliotecas síncronas (slide 8 da Aula 9).
6. Um arquivo `desafio_extra.http`, nesta pasta, com um pedido para cada rota e para cada erro.

## Preparação

O Tesseract é um programa, e não um pacote Python: instale-o no sistema, com o idioma português.

```bash
sudo apt install tesseract-ocr tesseract-ocr-por      # Ubuntu e WSL
brew install tesseract tesseract-lang                 # macOS
```

Depois, na pasta `M7`:

```bash
pip install -r exercicios/aula10/desafio_extra/requirements.txt
python exercicios/aula10/desafio_extra/gerar_imagens.py
tesseract exercicios/aula10/desafio_extra/atestado_2025001.png - -l por
```

O último comando confere a instalação: ele imprime o texto do atestado.

Os arquivos desta pasta:

| Arquivo | Conteúdo |
|---|---|
| `historico_notas.csv` | 240 linhas fictícias de turmas anteriores: frequência, média anterior e nota final |
| `alunos_cc_2026_2.csv` | os 14 alunos de CC com turma em 2026.2: a média real de 2026.1 (do `escola.db`) e uma frequência fictícia |
| `gerar_imagens.py` | gera três documentos digitalizados fictícios em PNG, para o OCR |
| `requirements.txt` | os pacotes do desafio, além dos do M7 |

## Para conferir

* O OCR de `atestado_2025001.png` encontra a matrícula `2025001`, e o de
  `aviso_sem_matricula.png` não encontra nenhuma.
* O treino com `historico_notas.csv` dá, aproximadamente,
  `nota = -1.958 + 0.061 * frequencia + 0.529 * media_anterior`, com R² de 0.502 no teste.
* Com frequência 82 e média anterior 6.7, a nota prevista é 6.6 (aprovado).
* No lote de `alunos_cc_2026_2.csv`, só 2025006 (5.6) e 2025008 (5.5) ficam com previsão abaixo
  de 6.

Entrega: o pacote `modelos_api` e o `desafio_extra.http`. Confira com `ruff check .` e
`mypy --strict modelos_api` (o `pytesseract`, o `joblib` e o `scikit-learn` não têm tipos: use
`# type: ignore[import-untyped]` na linha de cada import).

## Para pensar

* Por que essas rotas ficam numa API separada, e não como rotas novas da secretaria?
* O R² de 0.5 diz que o modelo explica metade da variação das notas no teste. O que isso muda
  na forma de apresentar a previsão à coordenação?
* Uma previsão de "reprovado" pode ser usada para decidir algo sobre o aluno sem uma pessoa
  olhar o caso? Onde, no sistema, essa decisão deveria ficar?
