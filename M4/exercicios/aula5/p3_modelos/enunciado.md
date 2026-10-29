# Prática 3: modelos SQLAlchemy

Os modelos do banco da escola estão em `modelo_de_dados/modelos/`, um arquivo por tabela. Todos os
comandos rodam a partir da pasta M4, com o `.venv` ativo e o banco migrado e semeado:

```bash
alembic upgrade head
python ferramentas/semear.py      # só num banco recém-criado
```

## Parte A: explorar

1. Rode os três scripts de demonstração e leia o código de cada um:

   ```bash
   python -m modelo_de_dados.uso_consultas
   python -m modelo_de_dados.uso_relacionamentos
   python -m modelo_de_dados.uso_alteracoes
   ```

2. Abra `modelo_de_dados/modelos/aluno.py` ao lado de `migracoes/versions/0001_esquema_inicial.py`.
   Encontre no modelo o que corresponde a `nullable=False`, `unique=True` e
   `sa.ForeignKey("curso.id")`. O que existe no modelo e não existe na migração?
3. Em `modelo_de_dados/conexao.py`, troque `echo=False` por `echo=True`, rode
   `uso_relacionamentos` de novo e observe o SQL que o SQLAlchemy gera. Volte para `echo=False`.

## Parte B: o modelo acompanha a migração

A migração 0002 da Prática 2 criou a coluna `aluno.telefone`, mas o modelo ainda não a conhece.

1. Com a 0002 aplicada (`alembic current` mostra `0002 (head)`), acrescente ao modelo `Aluno`:

   ```python
   telefone: Mapped[str | None] = mapped_column(String(20))
   ```

2. Rode `python -m modelo_de_dados.uso_consultas`: funciona.
3. Rode `alembic downgrade 0001` e o mesmo script de novo. A última linha do erro é:

   ```text
   sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: aluno.telefone
   ```

4. Volte com `alembic upgrade head`.

Pergunta: num sistema em produção, a migração e o modelo novo entram juntos? Em que ordem eles
chegam ao banco e ao programa?

## Parte C: consultas e alterações com os modelos

Complete as quatro funções de `exercicios/aula5/p3_modelos/consultas_orm.py`, procurando os
`TODO`. Use os modelos e `select()`; nada de SQL escrito à mão.

```bash
python -m exercicios.aula5.p3_modelos.consultas_orm
```

Saída esperada com as quatro funções prontas (está também no início do arquivo):

```text
1) alunos_do_curso
   ES: 15 alunos; os três primeiros: Felipe Azevedo, Giovana Batista, Henrique Coelho
   XX: []
2) turmas_do_professor
   Juliana Teixeira: CC201 (2026.1), SI201 (2026.1), CC201 (2026.2), SI201 (2026.2)
   Otávio Rezende: []
3) media_da_turma
   CC201 (2026.1): 7.77
   CC201 (2026.2): None
4) lancar_nota
   8.5 em CC201 (2026.2): gravada; lida de novo: 8.5
   10.5: ValueError: nota fora do intervalo de 0 a 10: 10.5
   CC999 (2026.2): LookupError: 2025001 não está matriculado em CC999 (2026.2)
```

Compare com a Prática 3 da Aula 4 (`exercicios/aula4/p3_python/consultas.py`): as mesmas
perguntas, antes com SQL e parâmetros `?`, agora com objetos. Os modelos montam o SQL com
parâmetros, então a proteção contra injeção continua valendo.

Confira também os tipos: `mypy exercicios/aula5/p3_modelos/consultas_orm.py`.
