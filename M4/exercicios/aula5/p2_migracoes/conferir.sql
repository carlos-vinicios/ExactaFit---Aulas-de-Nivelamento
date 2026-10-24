-- Conferência da Prática 2 da Aula 5 (SQLite). Não edite este arquivo.
--
-- Rode a partir da pasta M4, depois de cada passo de upgrade ou downgrade:
--   python ferramentas/sql.py escola.db exercicios/aula5/p2_migracoes/conferir.sql
--
-- As saídas esperadas, depois do upgrade e depois do downgrade, estão no enunciado.md.

-- Revisão aplicada no banco
SELECT version_num AS revisao FROM alembic_version;

-- Colunas da tabela aluno
SELECT name AS coluna, type AS tipo, "notnull" AS obrigatoria FROM pragma_table_info('aluno');

-- Índices da tabela aluno (unico = 1: criado por uma restrição UNIQUE ou CREATE UNIQUE INDEX)
SELECT name AS indice, "unique" AS unico FROM pragma_index_list('aluno') ORDER BY name;

-- Os dados sobreviveram à ida e volta?
SELECT (SELECT count(*) FROM aluno) AS alunos, (SELECT count(*) FROM matricula) AS matriculas;
