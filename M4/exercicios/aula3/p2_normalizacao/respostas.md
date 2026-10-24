# Prática 2: normalização

A biblioteca controla os empréstimos na planilha `emprestimos_planilha.csv` (abra no VS Code
com a extensão [Rainbow CSV](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv)
ou em qualquer editor de planilhas). Cada linha é um empréstimo. Os ISBNs são fictícios.

Responda abaixo de cada pergunta.

## 1. Redundância

Quais informações aparecem repetidas em várias linhas? Dê um exemplo citando os números dos
empréstimos.

>

## 2. Anomalias

A planilha já tem dois dados contraditórios. Encontre-os e diga qual anomalia os causou.

>

Descreva com um exemplo desta planilha:

* **Anomalia de inserção** (o que não dá para cadastrar sem inventar um empréstimo?):

>

* **Anomalia de atualização** (o que precisa mudar em várias linhas ao mesmo tempo?):

>

* **Anomalia de exclusão** (o que se perde ao apagar uma linha?):

>

## 3. Primeira forma normal (1FN)

Qual coluna viola a 1FN? Por quê? Como corrigir?

>

## 4. Dependências funcionais

Complete as dependências. A seta se lê "determina": conhecendo o lado esquerdo, existe um
único valor possível para o lado direito.

* `emprestimo` → data_emprestimo, data_devolucao, tombo, leitor_email
* `isbn` →
* `tombo` →
* `leitor_email` →

## 5. Segunda e terceira formas normais (2FN e 3FN)

Usando as dependências acima, explique por que a planilha não está na 3FN. Depois proponha a
decomposição em tabelas, indicando a chave primária e as chaves estrangeiras de cada uma.
Compare com o modelo que você desenhou na Prática 1.

>
