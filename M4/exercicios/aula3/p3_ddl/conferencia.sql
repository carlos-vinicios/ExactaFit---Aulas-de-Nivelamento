-- Conferência da Prática 3. Não edite este arquivo.
--
-- Rode a partir da pasta M4, num banco em memória (nada fica gravado):
--   python ferramentas/sql.py :memory: exercicios/aula3/p3_ddl/biblioteca.sql --continuar exercicios/aula3/p3_ddl/conferencia.sql
--
-- Cada comando tenta gravar ou apagar dados. Compare a sua saída com conferencia_esperada.txt:
-- cada comando deve ter "ok" ou "ERRO" no mesmo lugar. O texto da mensagem de erro pode variar.

-- Dados de apoio: devem ser aceitos
INSERT INTO autor (id, nome) VALUES (1, 'Machado de Assis');
INSERT INTO livro (id, isbn, titulo, ano) VALUES (1, '978-0-00-000001-1', 'Dom Casmurro', 1899);
INSERT INTO livro_autor (livro_id, autor_id) VALUES (1, 1);
INSERT INTO exemplar (id, tombo, livro_id) VALUES (1, 'T0001', 1);
INSERT INTO leitor (id, nome, email) VALUES (1, 'Lara Pinheiro', 'lara@campus.edu');

-- livro: ISBN obrigatório, ISBN único, título obrigatório, ano entre 1450 e 2100
INSERT INTO livro (titulo) VALUES ('Sem ISBN');
INSERT INTO livro (isbn, titulo) VALUES ('978-0-00-000001-1', 'Outro');
INSERT INTO livro (isbn) VALUES ('978-0-00-000002-2');
INSERT INTO livro (isbn, titulo, ano) VALUES ('978-0-00-000003-3', 'Futuro', 3000);

-- livro_autor: o par não se repete, um livro pode ter dois autores, o autor precisa existir
INSERT INTO livro_autor (livro_id, autor_id) VALUES (1, 1);
INSERT INTO autor (id, nome) VALUES (2, 'Outro Autor');
INSERT INTO livro_autor (livro_id, autor_id) VALUES (1, 2);
INSERT INTO livro_autor (livro_id, autor_id) VALUES (1, 99);

-- exemplar: livro existente e obrigatório, tombo único, estado padrão 'bom', estados válidos
INSERT INTO exemplar (tombo, livro_id) VALUES ('T0100', 99);
INSERT INTO exemplar (tombo) VALUES ('T0101');
INSERT INTO exemplar (tombo, livro_id) VALUES ('T0001', 1);
SELECT tombo, estado FROM exemplar;
INSERT INTO exemplar (tombo, livro_id, estado) VALUES ('T0002', 1, 'perdido');

-- leitor: e-mail obrigatório e único
INSERT INTO leitor (nome) VALUES ('Sem Email');
INSERT INTO leitor (nome, email) VALUES ('Outra Lara', 'lara@campus.edu');

-- emprestimo: válido, devolução registrada depois, leitor existente, datas obrigatórias e coerentes
INSERT INTO emprestimo (exemplar_id, leitor_id, data_emprestimo, data_prevista)
VALUES (1, 1, '2026-03-02', '2026-03-16');
UPDATE emprestimo SET data_devolucao = '2026-03-10' WHERE exemplar_id = 1;
INSERT INTO emprestimo (exemplar_id, leitor_id, data_emprestimo, data_prevista)
VALUES (1, 99, '2026-03-02', '2026-03-16');
INSERT INTO emprestimo (exemplar_id, leitor_id, data_emprestimo) VALUES (1, 1, '2026-03-02');
INSERT INTO emprestimo (exemplar_id, leitor_id, data_emprestimo, data_prevista, data_devolucao)
VALUES (1, 1, '2026-03-02', '2026-03-16', '2026-03-01');

-- apagar: livro com exemplares não sai; sem exemplares, sai e leva as autorias junto
DELETE FROM livro WHERE id = 1;
DELETE FROM emprestimo;
DELETE FROM exemplar WHERE livro_id = 1;
DELETE FROM livro WHERE id = 1;
SELECT (SELECT count(*) FROM livro_autor) AS autorias, (SELECT count(*) FROM autor) AS autores;
