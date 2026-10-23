# Desafio da Aula 2: relatório da turma reescrito

Reescreva `exercicios/aula2/p3_legado/relatorio_legado.py` em um arquivo novo nesta pasta,
`relatorio.py`, corrigindo os problemas que você registrou na Prática 3. O script legado não
deve ser alterado.

## Requisitos

1. Mesmo uso do legado: o caminho do CSV vem na linha de comando (`sys.argv`).
2. Ponto de entrada protegido por `if __name__ == "__main__":`.
3. Arquivo aberto com `with` e `encoding="utf-8"`; leitura com `csv.DictReader`.
4. Um tipo para o aluno (`dataclass`) e funções com type hints.
5. Nota validada (número de 0 a 10) e linha sem matrícula ou nome recusada.
6. Linhas inválidas não interrompem o relatório: são listadas no final, com o número da
   linha e o motivo, usando uma exceção própria.
7. Ordem do maior para o menor, numerada a partir de 1, com todos os alunos.
8. Sem variáveis globais que mudam durante a execução.
9. `ruff check` e `mypy` sem erros.

Dica: aproveite o que você já escreveu em `p1_funcoes/funcoes.py` e `p2_erros/erros.py`.

## Como verificar

```bash
python exercicios/aula2/desafio/relatorio.py exercicios/aula2/p3_legado/turma.csv
```

Saída esperada:

```text
=== MELHORES ALUNOS ===
 1  Carla Mendes      9.83  aprovado
 2  Gabriela Lima     8.50  aprovado
 3  Ana Beatriz       8.17  aprovado
 4  Íris Carvalho     7.17  aprovado
 5  Fábio Nunes       7.00  aprovado
 6  Elisa Fonseca     6.67  recuperação
 7  João Pedro        5.33  recuperação
 8  Bruno Costa       5.00  recuperação
 9  Diego Ramos       4.50  reprovado
10  Heitor Souza      3.83  reprovado
Média da turma: 6.60
```

```bash
python exercicios/aula2/desafio/relatorio.py exercicios/aula2/p3_legado/turma_com_erros.csv
```

Saída esperada (o texto dos motivos pode variar):

```text
=== MELHORES ALUNOS ===
 1  Carla Mendes      9.83  aprovado
 2  Ana Beatriz       8.17  aprovado
 3  Fábio Nunes       7.00  aprovado
Média da turma: 8.33
Linhas ignoradas: 5
  linha 3: n2: nota vazia
  linha 5: n1: could not convert string to float: 'dez'
  linha 7: n3: nota 11.0 fora do intervalo de 0 a 10
  linha 8: matrícula e nome são obrigatórios
  linha 10: n3: nota vazia
```

Sem argumento, o script deve mostrar como usar e terminar com código 2. Com um arquivo que
não existe, deve mostrar uma mensagem de erro curta, sem traceback.
