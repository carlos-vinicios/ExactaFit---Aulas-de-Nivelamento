# Prática 3: SQL a partir do Python

Complete as quatro funções de `consultas.py`. Elas recebem uma conexão do módulo `sqlite3` e
executam consultas com **parâmetros**:

```python
con.execute("SELECT nome FROM aluno WHERE matricula = ?", (matricula,))
```

Nunca monte o SQL com f-string. Veja o que acontece com a versão errada:

```python
matricula = "x' OR '1'='1"
f"SELECT nome FROM aluno WHERE matricula = '{matricula}'"
# SELECT nome FROM aluno WHERE matricula = 'x' OR '1'='1'   -> devolve todos os alunos
```

O programa tenta exatamente isso nas linhas "injeção" da saída.

## Como conferir

A partir da pasta M4:

```bash
python exercicios/aula4/p3_python/consultas.py
```

Compare com a saída esperada, escrita no início do arquivo. Cada função ainda não feita
aparece como "ainda não implementada". O programa cria um banco novo numa pasta temporária a
cada execução, então o seu `escola.db` não muda.

Confira também os tipos: `mypy exercicios/aula4/p3_python/consultas.py`.

Para experimentar no terminal, com as funções carregadas:

```bash
python -i exercicios/aula4/p3_python/consultas.py
```

```python
>>> import sqlite3
>>> con = sqlite3.connect("escola.db")      # o banco criado por ferramentas/criar_banco.py
>>> buscar_aluno(con, "2025001")
```

## Referências

* Módulo sqlite3, com a seção sobre placeholders: <https://docs.python.org/pt-br/3/library/sqlite3.html#sqlite3-placeholders>
* Transações e o `with con:`: <https://docs.python.org/pt-br/3/library/sqlite3.html#sqlite3-connection-context-manager>
* Injeção de SQL (OWASP): <https://owasp.org/www-community/attacks/SQL_Injection>
