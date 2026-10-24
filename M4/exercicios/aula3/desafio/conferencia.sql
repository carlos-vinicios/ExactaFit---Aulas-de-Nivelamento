-- Conferência do desafio da Aula 3. Não edite este arquivo.
--
-- Rode a partir da pasta M4, num banco em memória:
--   python ferramentas/sql.py :memory: exercicios/aula3/p3_ddl/biblioteca.sql --continuar exercicios/aula3/desafio/conferencia.sql
--
-- Compare com conferencia_esperada.txt: "ok" e "ERRO" devem aparecer nos mesmos lugares.

-- Dados de apoio
INSERT INTO livro (id, isbn, titulo) VALUES (1, '978-0-00-000001-1', 'Dom Casmurro');
INSERT INTO livro (id, isbn, titulo) VALUES (2, '978-0-00-000002-2', 'Pense em Python');
INSERT INTO leitor (id, nome, email) VALUES (1, 'Lara Pinheiro', 'lara@campus.edu');
INSERT INTO leitor (id, nome, email) VALUES (2, 'Caio Teles', 'caio@campus.edu');

-- Reserva nova começa ativa
INSERT INTO reserva (livro_id, leitor_id, data_reserva) VALUES (1, 1, '2026-04-01');
SELECT livro_id, leitor_id, status FROM reserva;

-- Status inválido, livro inexistente, data obrigatória
INSERT INTO reserva (livro_id, leitor_id, data_reserva, status) VALUES (2, 2, '2026-04-01', 'esquecida');
INSERT INTO reserva (livro_id, leitor_id, data_reserva) VALUES (99, 1, '2026-04-01');
INSERT INTO reserva (livro_id, leitor_id) VALUES (2, 2);

-- Regra 3: no máximo uma reserva ativa por leitor e livro
INSERT INTO reserva (livro_id, leitor_id, data_reserva) VALUES (1, 1, '2026-04-02');
INSERT INTO reserva (livro_id, leitor_id, data_reserva) VALUES (1, 2, '2026-04-02');
INSERT INTO reserva (livro_id, leitor_id, data_reserva) VALUES (2, 1, '2026-04-02');

-- O histórico pode repetir o par
INSERT INTO reserva (livro_id, leitor_id, data_reserva, status) VALUES (1, 1, '2026-03-01', 'atendida');
INSERT INTO reserva (livro_id, leitor_id, data_reserva, status) VALUES (1, 1, '2026-03-10', 'cancelada');
INSERT INTO reserva (livro_id, leitor_id, data_reserva, status) VALUES (1, 1, '2026-03-20', 'cancelada');

-- Reativar uma reserva cancelada daria duas ativas para o mesmo par
UPDATE reserva SET status = 'ativa' WHERE data_reserva = '2026-03-10';
SELECT status, count(*) AS reservas FROM reserva GROUP BY status ORDER BY status;
