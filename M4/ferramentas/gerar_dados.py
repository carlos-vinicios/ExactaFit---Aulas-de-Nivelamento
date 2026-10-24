"""Gera dados/escola_dados.sql de forma determinística.

Os INSERTs usam subconsultas pelas chaves naturais (sigla, matrícula, código) em vez de ids
fixos. Assim o mesmo arquivo funciona no SQLite e no PostgreSQL, sem dessincronizar as
sequências de id do PostgreSQL.

Uso, a partir da pasta M4: python ferramentas/gerar_dados.py
"""

import random
import unicodedata
from pathlib import Path

SAIDA = Path(__file__).resolve().parents[1] / "dados" / "escola_dados.sql"

CURSOS = [
    ("CC", "Ciência da Computação"),
    ("SI", "Sistemas de Informação"),
    ("ES", "Engenharia de Software"),
]

PROFESSORES = [
    "Helena Prado",
    "Ricardo Moura",
    "Juliana Teixeira",
    "Marcos Vieira",
    "Patrícia Lopes",
    "Fernando Gomes",
    "Camila Rocha",
    "André Nogueira",
    "Otávio Rezende",  # recém-contratado: não tem turmas (usado na Aula 4)
]

# código, nome, carga horária, curso
DISCIPLINAS = [
    ("CC101", "Algoritmos", 80, "CC"),
    ("CC102", "Estruturas de Dados", 80, "CC"),
    ("CC201", "Banco de Dados", 60, "CC"),
    ("CC202", "Redes de Computadores", 60, "CC"),
    ("CC301", "Compiladores", 40, "CC"),  # sem turma (usado na Aula 4)
    ("SI101", "Fundamentos de Sistemas de Informação", 40, "SI"),
    ("SI102", "Programação Web", 80, "SI"),
    ("SI201", "Banco de Dados Aplicado", 60, "SI"),
    ("SI202", "Gestão de Projetos", 40, "SI"),
    ("ES101", "Engenharia de Requisitos", 60, "ES"),
    ("ES102", "Testes de Software", 60, "ES"),
    ("ES201", "Arquitetura de Software", 80, "ES"),
    ("ES202", "DevOps", 40, "ES"),
]

# disciplina -> professor (índice em PROFESSORES)
DOCENTE = {
    "CC101": 0,
    "CC102": 1,
    "CC201": 2,
    "CC202": 3,
    "SI101": 4,
    "SI102": 5,
    "SI201": 2,
    "SI202": 6,
    "ES101": 7,
    "ES102": 6,
    "ES201": 1,
    "ES202": 5,
}
TURMAS_2026_2 = ["CC102", "CC201", "SI102", "SI201", "ES102", "ES201"]

ALUNOS = {
    "CC": [
        "Ana Beatriz Souza",
        "Bruno Costa",
        "Carla Mendes",
        "Diego Ramos",
        "Elisa Fonseca",
        "Fábio Nunes",
        "Gabriela Lima",
        "Heitor Souza",
        "Íris Carvalho",
        "João Pedro Alves",
        "Karina Duarte",
        "Lucas Martins",
        "Mariana Silva",
        "Nícolas Pereira",
        "Olívia Santos",
    ],
    "SI": [
        "Paulo Henrique Dias",
        "Quésia Moraes",
        "Rafael Barros",
        "Sofia Ribeiro",
        "Tiago Andrade",
        "Úrsula Campos",
        "Vitor Hugo Pires",
        "Wesley Cardoso",
        "Yasmin Freitas",
        "Zeca Lacerda",
        "Amanda Souza",
        "Bernardo Melo",
        "Cecília Araújo",
        "Davi Monteiro",
        "Eduarda Castro",
    ],
    "ES": [
        "Felipe Azevedo",
        "Giovana Batista",
        "Henrique Coelho",
        "Isabela Farias",
        "Júlio César Reis",
        "Larissa Matos",
        "Mateus Correia",
        "Natália Pinto",
        "Otávio Machado",
        "Priscila Rangel",
        "Renato Bezerra",
        "Sabrina Vasconcelos",
        "Thiago Moreira",
        "Valentina Rocha",
        "William Torres",
    ],
}
# alunos que ingressaram em agosto de 2026 e ainda não têm matrícula (usados na Aula 4)
SEM_MATRICULA = {"Olívia Santos", "Eduarda Castro", "William Torres"}


def sem_acento(texto: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


def email(nome: str, dominio: str) -> str:
    partes = sem_acento(nome).lower().split()
    return f"{partes[0]}.{partes[-1]}@{dominio}"


def q(texto: str) -> str:
    return "'" + texto.replace("'", "''") + "'"


def gerar() -> str:
    rnd = random.Random(2026)
    linhas = [
        "-- Dados de exemplo da escola. Gerado por scripts/gerar_dados.py; não edite à mão.",
        "-- Funciona no SQLite e no PostgreSQL.",
        "",
    ]

    linhas.append("INSERT INTO curso (sigla, nome) VALUES")
    linhas.append(",\n".join(f"    ({q(s)}, {q(n)})" for s, n in CURSOS) + ";")
    linhas.append("")

    linhas.append("INSERT INTO professor (nome, email) VALUES")
    linhas.append(
        ",\n".join(f"    ({q(n)}, {q(email(n, 'escola.edu'))})" for n in PROFESSORES)
        + ";"
    )
    linhas.append("")

    linhas.append(
        "INSERT INTO disciplina (codigo, nome, carga_horaria, curso_id) VALUES"
    )
    linhas.append(
        ",\n".join(
            f"    ({q(c)}, {q(n)}, {h}, (SELECT id FROM curso WHERE sigla = {q(s)}))"
            for c, n, h, s in DISCIPLINAS
        )
        + ";"
    )
    linhas.append("")

    turmas: list[tuple[str, str]] = []
    for codigo, *_ in DISCIPLINAS:
        if codigo in DOCENTE:
            turmas.append((codigo, "2026.1"))
            if codigo in TURMAS_2026_2:
                turmas.append((codigo, "2026.2"))
    linhas.append("INSERT INTO turma (disciplina_id, professor_id, semestre) VALUES")
    linhas.append(
        ",\n".join(
            f"    ((SELECT id FROM disciplina WHERE codigo = {q(c)}), "
            f"(SELECT id FROM professor WHERE email = {q(email(PROFESSORES[DOCENTE[c]], 'escola.edu'))}), {q(sem)})"
            for c, sem in turmas
        )
        + ";"
    )
    linhas.append("")

    alunos: list[tuple[str, str, str, str]] = []  # matricula, nome, data, curso
    seq = {"2025": 0, "2026": 0}
    for sigla, nomes in ALUNOS.items():
        for i, nome in enumerate(nomes):
            if nome in SEM_MATRICULA:
                ano, data = "2026", "2026-08-03"
            elif i % 3 == 2:
                ano, data = "2026", "2026-02-09"
            else:
                ano, data = "2025", "2025-02-10"
            seq[ano] += 1
            alunos.append((f"{ano}{seq[ano]:03d}", nome, data, sigla))
    alunos.sort()
    linhas.append(
        "INSERT INTO aluno (matricula, nome, email, data_ingresso, curso_id) VALUES"
    )
    linhas.append(
        ",\n".join(
            f"    ({q(m)}, {q(n)}, {q(email(n, 'aluno.escola.edu'))}, {q(d)}, "
            f"(SELECT id FROM curso WHERE sigla = {q(s)}))"
            for m, n, d, s in alunos
        )
        + ";"
    )
    linhas.append("")

    matriculas: list[tuple[str, str, str, str]] = []
    for matricula, nome, _, sigla in alunos:
        if nome in SEM_MATRICULA:
            continue
        do_curso = [c for c, *_, s in DISCIPLINAS if s == sigla and c in DOCENTE]
        for codigo in sorted(rnd.sample(do_curso, 3)):
            nota = min(10.0, max(0.0, round(rnd.gauss(7.0, 1.8), 1)))
            matriculas.append((matricula, codigo, "2026.1", f"{nota:.1f}"))
        do_semestre = [c for c in do_curso if c in TURMAS_2026_2]
        for codigo in sorted(rnd.sample(do_semestre, 2)):
            matriculas.append((matricula, codigo, "2026.2", "NULL"))
    linhas.append("INSERT INTO matricula (aluno_id, turma_id, nota) VALUES")
    linhas.append(
        ",\n".join(
            f"    ((SELECT id FROM aluno WHERE matricula = {q(m)}), "
            f"(SELECT t.id FROM turma t JOIN disciplina d ON d.id = t.disciplina_id "
            f"WHERE d.codigo = {q(c)} AND t.semestre = {q(s)}), {n})"
            for m, c, s, n in matriculas
        )
        + ";"
    )
    linhas.append("")
    return "\n".join(linhas)


if __name__ == "__main__":
    SAIDA.write_text(gerar(), encoding="utf-8")
    print(f"gerado: {SAIDA}")
