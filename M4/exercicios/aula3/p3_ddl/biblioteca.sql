-- Prática 3: esquema da biblioteca em SQL (SQLite)
--
-- Escreva o CREATE TABLE de cada tabela seguindo o dicionário de dados abaixo.
-- A conferência usa exatamente estes nomes de tabelas e colunas.
--
-- Confira com (a partir da pasta M4, num banco em memória):
--   python ferramentas/sql.py :memory: exercicios/aula3/p3_ddl/biblioteca.sql --continuar exercicios/aula3/p3_ddl/conferencia.sql
-- e compare a saída com exercicios/aula3/p3_ddl/conferencia_esperada.txt.
--
-- Lembre: no SQLite as chaves estrangeiras só são verificadas com PRAGMA foreign_keys = ON
-- (o ferramentas/sql.py liga esse pragma ao conectar).
--
-- ============================================================================================
-- Dicionário de dados
-- ============================================================================================
--
-- autor
--   id             inteiro, chave primária
--   nome           texto, obrigatório
--   nacionalidade  texto, opcional
--
-- livro
--   id             inteiro, chave primária
--   isbn           texto, obrigatório, único
--   titulo         texto, obrigatório
--   ano            inteiro, opcional, entre 1450 e 2100
--   editora        texto, opcional
--
-- livro_autor      (associativa: resolve o N:N entre livro e autor)
--   livro_id       referência a livro; ao apagar o livro, apaga a autoria junto
--   autor_id       referência a autor
--   chave primária composta (livro_id, autor_id)
--
-- exemplar
--   id             inteiro, chave primária
--   tombo          texto, obrigatório, único
--   livro_id       referência a livro, obrigatório; NÃO pode apagar um livro que tem exemplares
--   estado         texto, obrigatório, padrão 'bom', só aceita 'bom', 'regular' ou 'danificado'
--
-- leitor
--   id             inteiro, chave primária
--   nome           texto, obrigatório
--   email          texto, obrigatório, único
--   telefone       texto, opcional
--
-- emprestimo
--   id              inteiro, chave primária
--   exemplar_id     referência a exemplar, obrigatório
--   leitor_id       referência a leitor, obrigatório
--   data_emprestimo texto no formato AAAA-MM-DD, obrigatório
--   data_prevista   texto no formato AAAA-MM-DD, obrigatório
--   data_devolucao  texto no formato AAAA-MM-DD, opcional (vazio enquanto não devolvido);
--                   quando preenchida, não pode ser anterior a data_emprestimo
--
-- ============================================================================================

-- Exemplo pronto: a tabela autor.
CREATE TABLE autor (
    id            INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    nacionalidade TEXT
);

-- Escreva as demais tabelas abaixo, na ordem em que podem ser criadas
-- (uma tabela só pode referenciar outra que já exista).
