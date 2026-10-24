-- Prática 1 da Aula 5: o mesmo SQL no SQLite e no PostgreSQL.
--
-- Rode este arquivo nos dois bancos, já migrados e com dados (veja roteiro.md):
--   python ferramentas/sql.py escola.db --continuar exercicios/aula5/p1_postgres/comparacao.sql
--   python ferramentas/sql.py postgresql://escola:escola@localhost:5432/escola --continuar exercicios/aula5/p1_postgres/comparacao.sql
--
-- Antes de rodar, escreva em respostas.md o que você espera de cada caso.

-- Caso 1: texto numa coluna inteira
INSERT INTO disciplina (codigo, nome, carga_horaria, curso_id) VALUES ('XX901', 'Teste 1', 'vinte', 1);

-- Caso 2: data que não existe
INSERT INTO aluno (matricula, nome, data_ingresso, curso_id) VALUES ('2099001', 'Teste 2', '2026-02-30', 1);

-- Caso 3: texto maior que o tamanho da coluna (sigla é VARCHAR(10) na migração 0001)
INSERT INTO curso (sigla, nome) VALUES ('MUITOLONGA123', 'Teste 3');

-- Caso 4: LIKE diferencia maiúsculas e minúsculas?
SELECT count(*) AS souza_minusculo FROM aluno WHERE nome LIKE '%souza%';

-- Caso 5: como cada banco devolve verdadeiro e falso
SELECT 1 = 1 AS igual, 1 = 2 AS diferente;

-- Caso 6: divisão de inteiros
SELECT 7 / 2 AS inteiros, 7 / 2.0 AS com_decimal;

-- Caso 7: arredondar um número de ponto flutuante
SELECT round(CAST(7.125 AS DOUBLE PRECISION), 2) AS arredondado;

-- Caso 8: o tipo que o banco guardou
SELECT carga_horaria FROM disciplina WHERE codigo LIKE 'XX9%';

-- Limpeza: desfaz o que tiver sido aceito acima
DELETE FROM disciplina WHERE codigo LIKE 'XX9%';
DELETE FROM aluno WHERE matricula = '2099001';
DELETE FROM curso WHERE nome = 'Teste 3';
