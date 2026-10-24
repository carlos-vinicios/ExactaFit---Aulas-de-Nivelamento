-- Esquema do banco da escola (SQLite).
-- Usado nas Aulas 3 e 4. Na Aula 5 o mesmo esquema é criado por migrações (pasta migracoes/).
--
-- Atenção: no SQLite, chaves estrangeiras só são verificadas com
--   PRAGMA foreign_keys = ON;
-- executado em cada conexão. A função escola.db.conectar() faz isso.

CREATE TABLE curso (
    id    INTEGER PRIMARY KEY,
    sigla TEXT    NOT NULL UNIQUE,
    nome  TEXT    NOT NULL UNIQUE
);

CREATE TABLE aluno (
    id            INTEGER PRIMARY KEY,
    matricula     TEXT    NOT NULL UNIQUE,
    nome          TEXT    NOT NULL,
    email         TEXT    UNIQUE,
    data_ingresso TEXT    NOT NULL,              -- 'AAAA-MM-DD'
    curso_id      INTEGER NOT NULL REFERENCES curso (id)
);

CREATE TABLE professor (
    id    INTEGER PRIMARY KEY,
    nome  TEXT    NOT NULL,
    email TEXT    NOT NULL UNIQUE
);

CREATE TABLE disciplina (
    id            INTEGER PRIMARY KEY,
    codigo        TEXT    NOT NULL UNIQUE,
    nome          TEXT    NOT NULL,
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    curso_id      INTEGER NOT NULL REFERENCES curso (id)
);

CREATE TABLE turma (
    id            INTEGER PRIMARY KEY,
    disciplina_id INTEGER NOT NULL REFERENCES disciplina (id),
    professor_id  INTEGER NOT NULL REFERENCES professor (id),
    semestre      TEXT    NOT NULL,              -- '2026.1'
    UNIQUE (disciplina_id, semestre)
);

CREATE TABLE matricula (
    aluno_id INTEGER NOT NULL REFERENCES aluno (id) ON DELETE CASCADE,
    turma_id INTEGER NOT NULL REFERENCES turma (id),
    nota     REAL    CHECK (nota BETWEEN 0 AND 10),   -- NULL: semestre em andamento
    PRIMARY KEY (aluno_id, turma_id)
);
