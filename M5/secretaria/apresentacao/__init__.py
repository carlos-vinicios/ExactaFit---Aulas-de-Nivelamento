"""Camada de apresentação: as telas do terminal.

Regras desta camada:
* é a única que lê o que a pessoa digitou e a única que imprime;
* chama um serviço por tela e mostra o resultado;
* transforma as exceções das camadas de baixo em mensagens curtas (terminal.executar).

No M7, uma API ocupa este lugar e chama os mesmos serviços.
"""
