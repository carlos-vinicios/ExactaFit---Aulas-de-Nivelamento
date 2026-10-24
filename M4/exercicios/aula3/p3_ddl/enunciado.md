# Prática 3: do modelo para o SQL

Implemente o modelo da biblioteca no arquivo `biblioteca.sql`. O dicionário de dados no topo
do arquivo diz o nome, o tipo e as regras de cada coluna. A tabela `autor` já está pronta como
exemplo.

## Passos

1. Escreva o `CREATE TABLE` de `livro`, `livro_autor`, `exemplar`, `leitor` e `emprestimo`.
   Pense na ordem: uma tabela só pode referenciar outra que já foi criada.
2. Para cada regra do dicionário, escolha a restrição certa: `NOT NULL`, `UNIQUE`,
   `PRIMARY KEY`, `REFERENCES`, `CHECK`, `DEFAULT`, `ON DELETE CASCADE`.
3. Confira o esquema. A partir da pasta M4:

   ```bash
   python ferramentas/sql.py :memory: exercicios/aula3/p3_ddl/biblioteca.sql --continuar exercicios/aula3/p3_ddl/conferencia.sql
   ```

   O comando cria as suas tabelas num banco em memória e roda `conferencia.sql`, que tenta
   gravar e apagar dados: alguns comandos devem ser aceitos (`ok`) e outros recusados
   (`ERRO`). Compare a sua saída com `conferencia_esperada.txt`. O que importa é cada comando
   ter `ok` ou `ERRO` no mesmo lugar; o texto da mensagem de erro pode variar. Os comentários
   de `conferencia.sql` dizem qual regra cada grupo de comandos verifica.

   Dica: para comparar no VS Code, salve a saída num arquivo (acrescente
   `> minha_saida.txt` ao fim do comando), clique com o botão direito nele, escolha
   **Select for Compare** e depois **Compare with Selected** em `conferencia_esperada.txt`.
4. Experimente o esquema com seus próprios dados. Crie um arquivo `experimento.sql` com alguns
   comandos, por exemplo:

   ```sql
   INSERT INTO livro (isbn, titulo) VALUES ('978-0-00-000001-1', 'Dom Casmurro');
   INSERT INTO exemplar (tombo, livro_id) VALUES ('T0001', 1);
   SELECT * FROM exemplar;
   INSERT INTO exemplar (tombo, livro_id) VALUES ('T0002', 99);
   ```

   e rode os dois arquivos num banco gravado em disco:

   ```bash
   python ferramentas/sql.py biblioteca.db exercicios/aula3/p3_ddl/biblioteca.sql
   python ferramentas/sql.py biblioteca.db experimento.sql
   ```

   O `sql.py` liga `PRAGMA foreign_keys = ON`, executa os comandos em ordem, mostra o
   resultado de cada `SELECT` e para no primeiro erro. O último `INSERT` acima deve ser
   recusado. Para recomeçar do zero, apague o arquivo `biblioteca.db`.

   Para navegar pelas tabelas com o mouse, use a extensão
   [SQLite Viewer](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer)
   do VS Code ou o [DB Browser for SQLite](https://sqlitebrowser.org).

## Referências

* SQLite, CREATE TABLE: <https://www.sqlite.org/lang_createtable.html>
* SQLite, chaves estrangeiras: <https://www.sqlite.org/foreignkeys.html>
* SQLite, tipos de dados: <https://www.sqlite.org/datatype3.html>
