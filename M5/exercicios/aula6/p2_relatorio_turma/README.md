# Aula 6, Prática 2: o relatório da turma, camada por camada

Ponto de partida: a sua `PROPOSTA.md` da Prática 1. A tela `apresentacao/turma.py` está pronta;
faltam as camadas de baixo. Procure `TODO Aula 6, Prática 2` e compare cada esqueleto com o que
você propôs: arquivo, nome, parâmetros e tipo de retorno.

Implemente de baixo para cima. Depois de cada passo, rode a tela: o aviso
`ainda não implementado` sobe uma camada.

```text
$ python -m secretaria.apresentacao.turma CC201 2026.1
ainda não implementado (TODO Aula 6, Prática 2)
```

1. **Acesso a dados**, `acesso_dados/matriculas.py`: `matriculas_da_turma`. Use `SQL_MATRICULA`
   e `matricula_da_linha()`, como em `matriculas_do_aluno`, filtrando pela turma e ordenando
   pelo nome do aluno. A função já está na interface da camada (`acesso_dados/__init__.py`).
2. **Manager**, `managers/relatorios.py`: `montar_relatorio_turma`. Reaproveite `classificar()`
   e `media()` de `avaliacao.py`. A contagem tem as três situações, mesmo as que ficam com zero.
3. **Serviço**, `servicos/consultas.py`: `relatorio_turma`. Siga `consultar_boletim`: abra o
   banco, busque a turma com `turma_existente`, busque as matrículas e peça o relatório ao
   manager.

## Saída esperada

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

$ python -m secretaria.apresentacao.turma cc201 2026.2
CC201 Banco de Dados, 2026.2, docente: Juliana Teixeira

matrícula  nome                   nota  situação
2025001    Ana Beatriz Souza         -  cursando
...
2026003    Íris Carvalho             -  cursando

14 alunos: 0 aprovados, 0 reprovados, 14 cursando
Média da turma: sem notas lançadas

$ python -m secretaria.apresentacao.turma CC301 2026.1
erro: turma CC301 (2026.1) não encontrada
```

Íris aparece no fim porque o SQLite ordena os textos pelo código de cada caractere, e o `Í`
vem depois das letras sem acento.

## Para pensar

* A tela transforma `cc201` em `CC201` antes de chamar o serviço. Por que essa conversão fica na
  apresentação, e não no serviço ou no acesso a dados?
* O relatório e o boletim usam o mesmo `classificar()`. Se a nota de aprovação mudar para 7,
  quantos arquivos você precisa alterar?
* A sua proposta previu um tipo novo em `dominio.py`? O `RelatorioTurma` já estava lá: por que
  vale a pena um tipo próprio, em vez de devolver uma tupla `(turma, linhas, media, contagem)`?
