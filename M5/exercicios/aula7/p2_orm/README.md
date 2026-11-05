# Aula 7, Prática 2: trocar a camada de acesso a dados pelo ORM

A pasta `secretaria/acesso_orm` é uma segunda camada de acesso a dados, com o SQLAlchemy ORM.
Ela usa os modelos da Aula 5 (`acesso_orm/modelos`, um por arquivo) e tem **a mesma interface**
de `acesso_dados`: as mesmas funções, com os mesmos parâmetros, devolvendo os mesmos tipos de
`dominio.py`.

## 1. Comparar as duas camadas

1. Abra lado a lado `acesso_dados/__init__.py` e `acesso_orm/__init__.py`. O que é igual?
2. Compare `acesso_orm/modelos` com `M4/modelo_de_dados/modelos`: são os mesmos modelos.
3. Compare `buscar_aluno` nas duas camadas. Onde o objeto do ORM vira o `Aluno` de
   `dominio.py`? Por que ele não pode sair da camada como está?

## 2. Completar a camada

Procure `TODO Aula 7, Prática 2` em `acesso_orm/matriculas.py` e implemente:

* `matriculas_da_turma`: como `matriculas_do_aluno`, filtrando pela turma e ordenando pelo nome
  do aluno;
* `gravar_nota`: `sessao.get_one(modelos.Matricula, (aluno_id, turma_id))` e uma atribuição à
  nota. Não há `UPDATE` escrito à mão: a sessão percebe a mudança e grava no commit, no fim do
  `abrir()`.

Se você fez o desafio da Aula 6, implemente também `matriculas_do_curso` e acrescente-a à
interface (`acesso_orm/__init__.py`).

## 3. A troca

Nos arquivos de `secretaria/servicos` que importam a camada de dados (`buscas.py`,
`consultas.py`, `notas.py` e `matriculas.py`), troque a linha do import:

```python
from secretaria import acesso_dados as dados  # antes: sqlite3
from secretaria import acesso_orm as dados  # depois: SQLAlchemy ORM
```

Nenhuma outra linha muda: nem nos serviços, nem nos managers, nem na apresentação. Rode as
mesmas telas das práticas anteriores. Com o banco recém-criado, a saída é idêntica:

```text
$ python -m secretaria.apresentacao.turma CC201 2026.1
CC201 Banco de Dados, 2026.1, docente: Juliana Teixeira

matrícula  nome                   nota  situação
2025002    Bruno Costa             9.1  aprovado
2026001    Carla Mendes            9.6  aprovado
2025003    Diego Ramos             8.3  aprovado
2025004    Elisa Fonseca           8.0  aprovado
2026002    Fábio Nunes             7.1  aprovado
2025005    Gabriela Lima           7.9  aprovado
2025006    Heitor Souza            8.3  aprovado
2025007    João Pedro Alves        5.6  reprovado
2026004    Lucas Martins           8.6  aprovado
2025009    Mariana Silva           5.6  reprovado
2026003    Íris Carvalho           7.4  aprovado

11 alunos: 9 aprovados, 2 reprovados, 0 cursando
Média da turma: 7.77

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 8.5
Nota 8.5 lançada: 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2), aprovado

$ python -m secretaria.apresentacao.boletim 2025001
Ana Beatriz Souza (2025001), curso CC

semestre  disciplina                       nota  situação
2026.1    CC101 Algoritmos                  9.9  aprovado
2026.1    CC102 Estruturas de Dados         4.5  reprovado
2026.1    CC202 Redes de Computadores       5.6  reprovado
2026.2    CC102 Estruturas de Dados           -  cursando
2026.2    CC201 Banco de Dados              8.5  aprovado

Média das notas lançadas: 7.12
```

## 4. O mesmo sistema no PostgreSQL (opcional)

Com o acesso pelo ORM, o sistema funciona com qualquer banco da `DATABASE_URL`. Siga a seção
"PostgreSQL (Aula 7)" do `README.md` da pasta `M5` e rode a tela da turma de novo. A saída é a
mesma, com uma diferença: Íris Carvalho aparece entre Heitor e João. O PostgreSQL ordena os
textos pelas regras do idioma, e o SQLite pelo código de cada caractere.

Depois, ainda com a `DATABASE_URL` do PostgreSQL, volte um dos serviços para `acesso_dados` e
rode a tela. O que acontece? Qual camada percebeu o problema? Desfaça a volta e, para usar o
SQLite de novo, abra um terminal novo.
