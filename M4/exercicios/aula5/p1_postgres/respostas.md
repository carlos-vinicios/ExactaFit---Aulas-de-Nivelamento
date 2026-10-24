# Prática 1: comparação SQLite e PostgreSQL

Preencha a previsão antes de rodar `comparacao.sql`. Nas colunas de resultado, escreva
"aceitou", "recusou" ou o valor devolvido.

| Caso | Previsão | SQLite | PostgreSQL | Por que são diferentes (ou iguais)? |
|---|---|---|---|---|
| 1. texto em coluna inteira | | | | |
| 2. data inexistente | | | | |
| 3. texto maior que VARCHAR(10) | | | | |
| 4. LIKE com minúsculas | | | | |
| 5. verdadeiro e falso | | | | |
| 6. divisão de inteiros | | | | |
| 7. round em ponto flutuante | | | | |
| 8. o que ficou gravado | | | | |

## Perguntas

1. Uma colega desenvolve no SQLite da própria máquina, mas o sistema roda em PostgreSQL no
   servidor. Que risco os casos 1, 2 e 3 mostram? O que você recomendaria?

>

2. Os casos 1, 2 e 3 teriam resultado diferente no SQLite se as tabelas fossem `STRICT`?
   Leia <https://www.sqlite.org/stricttables.html> e responda para cada caso.

>
