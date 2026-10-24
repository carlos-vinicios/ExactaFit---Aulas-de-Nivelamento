-- Conferência de q06, q07 e q08. Não edite este arquivo.
--
-- A partir da pasta M4, recrie o banco e rode as três alterações e esta conferência:
--   python ferramentas/criar_banco.py
--   python ferramentas/sql.py escola.db exercicios/aula4/p1_consultas/q06_inserir_professor.sql exercicios/aula4/p1_consultas/q07_atualizar_carga.sql exercicios/aula4/p1_consultas/q08_apagar_professor.sql exercicios/aula4/p1_consultas/conferir_alteracoes.sql
--
-- A saída esperada está no enunciado.md.

-- q06 e q08: Marina entrou, Otávio saiu, ninguém mais mudou
SELECT count(*) AS professores,
       sum(nome = 'Marina Duarte') AS marina,
       sum(nome = 'Otávio Rezende') AS otavio
FROM professor;

-- q07: nenhuma disciplina abaixo de 60 horas; as de 60 horas ou mais não mudaram
SELECT min(carga_horaria) AS menor_carga, sum(carga_horaria) AS total_horas FROM disciplina;
SELECT codigo, carga_horaria FROM disciplina WHERE codigo IN ('CC101', 'CC201', 'CC301') ORDER BY codigo;

-- As alterações não podem tocar as outras tabelas
SELECT (SELECT count(*) FROM turma) AS turmas,
       (SELECT count(*) FROM matricula) AS matriculas,
       (SELECT count(*) FROM aluno) AS alunos;
