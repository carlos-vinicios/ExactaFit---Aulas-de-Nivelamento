"""Camada de managers: as regras de negócio da escola.

Regras desta camada:
* recebe e devolve os tipos de dominio.py;
* não abre banco, não escreve SQL e não imprime nada;
* quando uma regra não permite o pedido, levanta RegraDeNegocioError.
"""
