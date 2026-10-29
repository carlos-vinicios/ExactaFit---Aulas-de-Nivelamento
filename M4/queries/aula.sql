-- SELECT * FROM alembic_version;

-- PRAGMA foreign_keys = ON;

-- DELETE FROM professor
-- WHERE nome = 'Helena Prado';


-- SELECT count(*)
-- FROM aluno AS a
-- JOIN matricula AS m ON m.aluno_id = a.id
-- WHERE a.curso_id = 1;

-- SELECT 
--     aluno_id
-- FROM matricula
-- GROUP BY aluno_id
-- HAVING avg(nota) > 7;

-- SELECT
--     *
-- FROM disciplina;

-- SELECT 
--     codigo, nome, carga_horaria
-- FROM disciplina
-- WHERE 
--     curso_id = 3
-- ORDER BY carga_horaria ASC, codigo
-- LIMIT 3;

-- SELECT
--     *
-- FROM aluno
-- WHERE
--     nota IS NOT NULL
-- ORDER BY nome ASC;

-- SELECT count(*)
-- FROM matricula;

-- SELECT count(*)
-- FROM matricula
-- WHERE nota IS NULL;

-- SELECT count(*)
-- FROM matricula
-- WHERE 
--     nota < 6 OR nota >= 6;

-- SELECT
--     sigla || ' - ' || nome as nome_sigla
-- FROM curso;

-- SELECT 
--     codigo, nome, carga_horaria
-- FROM disciplina
-- WHERE 
--     carga_horaria > 60
-- ORDER BY carga_horaria ASC, codigo
-- LIMIT 3;

-- SELECT 
--     *
-- FROM matricula
-- -- WHERE 
-- --     nota BETWEEN 5 AND 7
-- ORDER BY nota ASC;



-- SELECT 
--     a.nome, c.sigla, c.nome
-- FROM aluno AS a
-- JOIN curso AS c ON c.id = a.curso_id
-- ORDER BY a.matricula
-- LIMIT 4;

-- SELECT p.nome, count(*) AS turmas
-- FROM turma AS t
-- JOIN professor AS p ON p.id = t.professor_id
-- GROUP BY p.id, p.nome
-- HAVING count(*) >= 3
-- ORDER BY turmas DESC, p.nome;

