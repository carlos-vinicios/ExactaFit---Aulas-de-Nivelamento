# Aula 2, Prática 3: análise do código legado

Você recebeu `relatorio_legado.py`. Quem escreveu não está mais na equipe. O comentário no
topo diz "funciona, não mexer", mas a coordenação relata que o relatório tem erros.

Não edite o arquivo nesta prática: o objetivo é entender e registrar, não corrigir.

## 1. Reconhecimento, sem executar

1. Qual é o ponto de entrada? O que acontece se outro módulo fizer `import relatorio_legado`?
2. Quais nomes são globais? Quais funções leem e quais alteram cada um?
3. Descreva o caminho de um dado: linha do CSV, função `le`, função `calc`, `print`.
   Qual é o tipo do dado em cada etapa (str, list de quê)?
4. De onde vem `mean`? Como descobrir isso sem conhecer o módulo de antemão?

## 2. Hipóteses

Liste o que pode estar errado, ainda sem executar. Use o que vimos na aula: tipos,
argumentos padrão, `try`/`except`, `with`.

## 3. Ferramentas

```bash
ruff check exercicios/aula2/p3_legado/relatorio_legado.py
```

Quais avisos confirmam suas hipóteses? Algum problema da lista ficou de fora do Ruff?

## 4. Experimentos

Rode a partir da pasta `aula-python`:

```bash
python exercicios/aula2/p3_legado/relatorio_legado.py exercicios/aula2/p3_legado/turma.csv
python exercicios/aula2/p3_legado/relatorio_legado.py exercicios/aula2/p3_legado/turma_com_erros.csv
```

No Windows, a primeira execução pode falhar com `UnicodeDecodeError`. Isso também é um
problema do script: anote e continue os experimentos com o modo UTF-8 do Python:

```bash
python -X utf8 exercicios/aula2/p3_legado/relatorio_legado.py exercicios/aula2/p3_legado/turma.csv
```

Compare com o resultado correto de `turma.csv`:

| Aluno | Média | Situação |
|---|---|---|
| Carla Mendes | 9.83 | aprovado |
| Gabriela Lima | 8.50 | aprovado |
| Ana Beatriz | 8.17 | aprovado |
| Íris Carvalho | 7.17 | aprovado |
| Fábio Nunes | 7.00 | aprovado |
| Elisa Fonseca | 6.67 | recuperação |
| João Pedro | 5.33 | recuperação |
| Bruno Costa | 5.00 | recuperação |
| Diego Ramos | 4.50 | reprovado |
| Heitor Souza | 3.83 | reprovado |

Regras: aprovado com média a partir de 7, recuperação a partir de 5. Média da turma: 6.60.

- Quantos alunos o script lista? Algum aluno não aparece?
- Bruno Costa (média 5,0) aparece com a situação certa?
- O título diz "MELHORES ALUNOS". A ordem corresponde ao título?
- Com o arquivo com erros, o que acontece? Em qual linha do script o programa para?

## 5. Registro dos problemas

Registre pelo menos cinco problemas na tabela abaixo. Para cada um: linha, descrição, como
comprovar (comando, experimento ou aviso do Ruff) e a correção que você proporia.

| # | Linha | Problema | Como comprovar | Correção proposta |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
