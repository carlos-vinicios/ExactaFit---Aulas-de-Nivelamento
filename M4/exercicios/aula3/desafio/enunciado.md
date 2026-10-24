# Desafio da Aula 3: reservas

Quando todos os exemplares de um livro estão emprestados, o leitor pode **reservar o livro**
(não um exemplar específico). A biblioteca quer guardar o histórico de reservas.

Regras:

1. Uma reserva liga um leitor a um livro e tem a data em que foi feita.
2. O status da reserva é `ativa`, `atendida` ou `cancelada`. Uma reserva nova começa `ativa`.
3. Um leitor **não pode ter duas reservas ativas para o mesmo livro**. Reservas atendidas ou
   canceladas não contam: o mesmo leitor pode reservar o mesmo livro de novo no mês seguinte.

Acrescente ao final do seu `exercicios/aula3/p3_ddl/biblioteca.sql` a tabela `reserva` com as
colunas `id`, `livro_id`, `leitor_id`, `data_reserva` e `status`, e o que mais for preciso para
garantir a regra 3 no próprio banco.

A regra 3 não cabe num `UNIQUE (livro_id, leitor_id)` comum. Por quê? Pesquise **índice
parcial** na documentação do SQLite: <https://www.sqlite.org/partialindex.html>.

Confira com:

```bash
python ferramentas/sql.py :memory: exercicios/aula3/p3_ddl/biblioteca.sql --continuar exercicios/aula3/desafio/conferencia.sql
```

e compare a saída com `conferencia_esperada.txt`, desta pasta: `ok` e `ERRO` devem aparecer
nos mesmos lugares.

Entrega: o arquivo `biblioteca.sql`, com as duas conferências (Prática 3 e desafio) iguais às
esperadas, e um parágrafo no topo do arquivo, em comentário, explicando por que o `UNIQUE`
comum não resolve.
