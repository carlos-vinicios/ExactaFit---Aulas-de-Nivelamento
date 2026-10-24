# Prática 1: modelagem conceitual

Leia a descrição abaixo e construa o modelo entidade-relacionamento da biblioteca.

## Descrição

A Biblioteca do Campus quer substituir a planilha em que controla os empréstimos.

A biblioteca possui **livros**. De cada livro guardamos o ISBN, o título, o ano de publicação
e a editora. Dois livros diferentes nunca têm o mesmo ISBN.

Cada livro foi escrito por um ou mais **autores**, e um autor pode ter escrito vários livros
do acervo. Do autor guardamos o nome e a nacionalidade.

A biblioteca pode ter várias cópias físicas do mesmo livro. Cada cópia é um **exemplar**, que
recebe um código de tombo (etiqueta colada na lombada, único na biblioteca) e tem um estado de
conservação: bom, regular ou danificado.

Os **leitores** se cadastram com nome, e-mail e telefone. O e-mail é usado para login e não pode
se repetir.

Um leitor faz **empréstimos** de exemplares. Cada empréstimo registra a data em que foi feito,
a data prevista para devolução e a data em que o exemplar foi devolvido (vazia enquanto o
exemplar não volta). Ao longo do tempo, o mesmo exemplar é emprestado muitas vezes, e o mesmo
leitor faz muitos empréstimos.

## O que fazer

1. Liste as entidades e os atributos de cada uma.
2. Liste os relacionamentos. Para cada um, escreva a cardinalidade (1:1, 1:N ou N:N) e uma
   frase que a justifique, por exemplo: "um livro tem vários exemplares; um exemplar é de um
   único livro, logo 1:N".
3. Marque a chave primária de cada entidade. Onde houver chave natural candidata (ISBN,
   tombo, e-mail), diga se ela será a chave primária ou apenas única, e por quê.
4. Resolva o relacionamento N:N com uma tabela associativa.
5. Desenhe o diagrama em Mermaid no arquivo `modelo.md` e confira a visualização.

## Como visualizar o diagrama

* No VS Code, instale a extensão
  [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
  e abra a pré-visualização com `Ctrl+Shift+V`.
* Ou cole o bloco no [Mermaid Live Editor](https://mermaid.live).
* Sintaxe do diagrama ER: <https://mermaid.js.org/syntax/entityRelationshipDiagram.html>

O modelo que você construir aqui será implementado em SQL na Prática 3.
