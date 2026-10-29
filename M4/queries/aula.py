import os

import psycopg

# URL = "postgresql://escola:escola@localhost:5432/escola"
URL = os.environ.get("DATABASE_URL", "")
URL = URL.replace("+psycopg", "").strip()
print(URL, type(URL))

with psycopg.connect(URL) as con:
    linha = con.execute(
        "SELECT nome FROM aluno WHERE matricula = %s",
        ("2025001",),
    ).fetchone()


print(linha)
