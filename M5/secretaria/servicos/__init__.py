"""Camada de serviços: um caso de uso por função.

Regras desta camada:
* abre o banco e define a transação: tudo o que acontece dentro do `with dados.abrir()` é
  confirmado junto ou desfeito junto;
* busca os dados pela camada de acesso a dados e pede as decisões aos managers;
* levanta NaoEncontradoError quando o aluno, a turma ou a matrícula não existem;
* não lê o teclado e não imprime nada.
"""
