"""Aula 1, Prática 1: tour pelo VS Code.

Faça cada tarefa usando o atalho indicado e marque [x] quando conseguir.
Atalhos para Windows e Linux. No macOS, troque Ctrl por Cmd e Alt por Option.
Nesta prática não é preciso executar o arquivo: a execução vem no Bloco 3,
depois de preparar o ambiente virtual.
"""

NOTA_APROVACAO = 7.0


def media(notas: list[float]) -> float:
    """Média simples das notas."""
    return sum(notas) / len(notas)


def situacao(valor: float) -> str:
    """Devolve 'aprovado' ou 'reprovado'."""
    return "aprovado" if valor >= NOTA_APROVACAO else "reprovado"


notas = [6.0, 8.0, 7.5]
resultado = media(notas)
print(f"média = {resultado:.2f}, situação: {situacao(resultado)}")

# NAVEGAÇÃO
# [ ] 1. Cursor sobre `media` na linha 23 e F12: o editor vai para a definição.
# [ ] 2. Cursor sobre `notas` e Shift+F12: lista de todas as referências.
# [ ] 3. Cursor sobre `notas` e F2: renomeie para `notas_bimestre`. Todas as ocorrências mudam?
# [ ] 4. Passe o mouse sobre `situacao`: o que o tooltip mostra sobre parâmetros e retorno?
# [ ] 5. Ctrl+P, digite "relatorio" e abra exercicios/aula1/p2_ambiente/relatorio.py.
# [ ] 6. Ainda em relatorio.py, Ctrl+Shift+O e escolha a função `media_da_turma`.
# [ ] 7. Ctrl+Shift+F e procure por "NOTA_APROVACAO" no projeto inteiro.

# EDIÇÃO
# [ ] 8. Selecione as linhas 22 a 24 e use Ctrl+/ para comentar e descomentar.
# [ ] 9. Com o cursor na linha 24, use Alt+Seta para cima e Alt+Seta para baixo.
# [ ] 10. Desarrume a linha abaixo (espaços extras) e salve com Ctrl+S.
#         Com a extensão Ruff instalada, a formatação é corrigida ao salvar.
exemplo = [1, 2, 3]

# PAINÉIS E LAYOUT
# [ ] 11. Ctrl+Shift+M abre o painel Problems. Volte a relatorio.py: que avisos aparecem?
# [ ] 12. Ctrl+\ divide o editor: deixe tour.py de um lado e relatorio.py do outro.
# [ ] 13. Ctrl+B esconde e mostra a barra lateral; Ctrl+` abre e fecha o terminal integrado.
