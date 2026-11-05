# Aula 7, Prática 1: o schema do lançamento de nota

Ponto de partida: a pasta `secretaria` com as práticas da Aula 6 feitas. Se faltou alguma,
copie a pasta `secretaria` do gabarito da Aula 6, que o professor distribui no início da aula.

Na Aula 6, a nota `dez` foi recusada pela apresentação e a nota `11` pelo manager. As duas são
erros de **formato** do pedido, e não regras da escola. Nesta prática, o formato passa a ser
conferido num só lugar, o schema, logo na entrada da apresentação, antes de o pedido chegar ao
serviço.

## 1. O schema

Em `secretaria/schemas.py`, os tipos `MatriculaAluno`, `CodigoDisciplina` e `Semestre` já estão
prontos. Complete a classe `LancamentoNota` (procure `TODO Aula 7, Prática 1`).

Experimente no terminal, a partir da pasta `M5`, antes de ligar o schema às camadas:

```python
>>> from secretaria.schemas import LancamentoNota
>>> LancamentoNota(matricula="2025001", codigo=" cc201 ", semestre="2026.2", nota="8,5")
LancamentoNota(matricula='2025001', codigo='CC201', semestre='2026.2', nota=8.5)
>>> LancamentoNota(matricula="20251", codigo="CC201", semestre="2026.3", nota=11)
```

O segundo exemplo deve levantar `ValidationError` com três problemas: matrícula, semestre e
nota. Leia a mensagem inteira.

## 2. Ligar o schema às camadas

1. **Apresentação**, `apresentacao/lancar_nota.py`: em `main()`, a nota segue como texto (saem
   `numero()` e a conversão); em `lancar()`, monte o pedido com
   `LancamentoNota.model_validate({...})`, com os quatro textos digitados, e passe o pedido ao
   serviço.
2. **Apresentação**, `apresentacao/terminal.py`: em `executar()`, trate `ValidationError` (de
   `pydantic`), com uma linha `erro: campo: mensagem` por problema. A função abaixo traduz as
   mensagens do Pydantic que aparecem em inglês; copie-a para `terminal.py`:

   ```python
   def erros_de_validacao(erro: ValidationError) -> list[str]:
       """Mensagens em português para os erros de validação do Pydantic."""
       traducoes = {
           "float_parsing": "deve ser um número, como 8.5",
           "greater_than_equal": "deve ser no mínimo {ge}",
           "less_than_equal": "deve ser no máximo {le}",
           "missing": "é obrigatório",
       }
       mensagens = []
       for item in erro.errors():
           campo = item["loc"][0]
           modelo = traducoes.get(item["type"])
           texto = modelo.format(**item.get("ctx", {})) if modelo else item["msg"]
           mensagens.append(f"erro: {campo}: {texto.removeprefix('Value error, ')}")
       return mensagens
   ```

3. **Serviço**, `servicos/notas.py`: `lancar_nota(pedido: LancamentoNota)` recebe o schema no
   lugar dos quatro valores soltos.
4. **Manager**, `managers/avaliacao.py`: tire de `preparar_nota` a conferência de 0 a 10. Ela
   agora é garantida pelo schema. As regras do semestre e da casa decimal continuam ali.

## Saída esperada

Com o banco recém-criado (`python ../M4/ferramentas/criar_banco.py escola.db`), nesta ordem:

```text
$ python -m secretaria.apresentacao.lancar_nota 2025001 cc201 2026.2 8,46
Nota 8.5 lançada: 2025001 Ana Beatriz Souza, CC201 Banco de Dados (2026.2), aprovado

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 11
erro: nota: deve ser no máximo 10

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC201 2026.2 dez
erro: nota: deve ser um número, como 8.5

$ python -m secretaria.apresentacao.lancar_nota 20251 CC2010 2026.3 -1
erro: matricula: deve ter 7 dígitos, como 2025001
erro: codigo: deve ter 2 letras e 3 dígitos, como CC201
erro: semestre: deve estar no formato AAAA.1 ou AAAA.2, como 2026.2
erro: nota: deve ser no mínimo 0

$ python -m secretaria.apresentacao.lancar_nota 2025001 CC101 2026.1 9
não permitido: o semestre 2026.1 está encerrado; notas só podem ser lançadas em 2026.2
```

Repare: os quatro problemas do quarto pedido aparecem de uma vez, e o último pedido, que tem o
formato certo, só é recusado pela regra do semestre, no manager.

## Para pensar

* O schema mora em `secretaria/schemas.py`, e não dentro da apresentação. Quem mais vai usá-lo
  quando a apresentação for uma API, no M7?
* O serviço confia que `pedido.nota` está entre 0 e 10. O que garante isso, se o serviço não
  confere?
