# Aula 6, Prática 1: o mapa das camadas

Antes de escrever código numa arquitetura em camadas, é preciso saber por onde passa um pedido:
quem chama quem, o que cada camada recebe e o que devolve. Nesta prática você segue uma chamada
que já funciona e, depois, propõe a estrutura de uma funcionalidade nova.

## Preparação

Siga a seção "Preparação" do `README.md` da pasta `M5`. No fim, esta tela deve funcionar:

```text
$ python -m secretaria.apresentacao.boletim 2025001
Ana Beatriz Souza (2025001), curso CC

semestre  disciplina                       nota  situação
2026.1    CC101 Algoritmos                  9.9  aprovado
2026.1    CC102 Estruturas de Dados         4.5  reprovado
2026.1    CC202 Redes de Computadores       5.6  reprovado
2026.2    CC102 Estruturas de Dados           -  cursando
2026.2    CC201 Banco de Dados                -  cursando

Média das notas lançadas: 6.67
```

## Parte A: seguir uma chamada

Abra `secretaria/apresentacao/boletim.py` e siga o caminho do pedido até o SQL e de volta. No VS
Code, `F12` (Ir para Definição) abre a função sob o cursor.

Preencha a tabela de `MAPA.md`, um passo por linha, na ordem em que as funções são chamadas. A
primeira linha já está preenchida.

## Parte B: as fronteiras

Responda em `MAPA.md`:

1. Quais tipos de `dominio.py` cruzam a fronteira entre o acesso a dados e o serviço? E entre o
   serviço e a apresentação?
2. Em que arquivo a conexão com o banco é aberta, e quem decide quando ela é aberta e fechada?
3. Abra `secretaria/acesso_dados/__init__.py`. O que ele lista, e por que o serviço importa a
   camada inteira (`from secretaria import acesso_dados as dados`) em vez de cada arquivo?
4. Rode a tela com uma matrícula que não existe:

   ```text
   $ python -m secretaria.apresentacao.boletim 1999999
   erro: aluno 1999999 não encontrado
   ```

   Em qual camada o erro nasce, e em qual ele vira essa mensagem?

## Parte C: proposta de uma funcionalidade nova

A secretaria quer o relatório de uma turma:

```text
$ python -m secretaria.apresentacao.turma CC201 2026.1
CC201 Banco de Dados, 2026.1, docente: Juliana Teixeira

matrícula  nome                   nota  situação
2025002    Bruno Costa             9.1  aprovado
...
2026003    Íris Carvalho           7.4  aprovado

11 alunos: 9 aprovados, 2 reprovados, 0 cursando
Média da turma: 7.77
```

**Antes de abrir os arquivos da Prática 2**, preencha `PROPOSTA.md`: para cada camada, de baixo
para cima, o arquivo, a função com os tipos dos parâmetros e do retorno, e o que ela faz. A tela
(`apresentacao/turma.py`) já existe e é o ponto de partida: veja o que ela espera receber.

Na Prática 2, compare a sua proposta com o esqueleto que está no código.
