-- Conferência do desafio da Aula 5. Não edite este arquivo.
--
-- Rode a partir da pasta M4, com o banco migrado até a 0003 (veja o enunciado.md):
--   python ferramentas/sql.py escola.db --continuar exercicios/aula5/desafio/conferir.sql
-- Funciona também no PostgreSQL: troque escola.db pela URL postgresql://...

-- Situação calculada a partir da nota, nas matrículas que já existiam
SELECT situacao, count(*) AS matriculas FROM matricula GROUP BY situacao ORDER BY situacao;
SELECT DISTINCT situacao AS com_nota_6_ou_mais FROM matricula WHERE nota >= 6;

-- Uma matrícula nova começa como cursando
INSERT INTO matricula (aluno_id, turma_id)
VALUES ((SELECT id FROM aluno WHERE matricula = '2026005'),
        (SELECT t.id FROM turma AS t JOIN disciplina AS d ON d.id = t.disciplina_id
         WHERE d.codigo = 'CC102' AND t.semestre = '2026.2'));
SELECT situacao AS matricula_nova FROM matricula
WHERE aluno_id = (SELECT id FROM aluno WHERE matricula = '2026005');

-- Só três valores são aceitos
UPDATE matricula SET situacao = 'trancado';

-- Desfaz a matrícula de teste, para o banco voltar ao que era
DELETE FROM matricula WHERE aluno_id = (SELECT id FROM aluno WHERE matricula = '2026005');
SELECT count(*) AS matriculas FROM matricula;
