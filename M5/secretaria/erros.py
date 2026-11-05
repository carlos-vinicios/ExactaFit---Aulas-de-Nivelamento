"""Exceções do sistema. Nascem nas camadas de baixo; a apresentação decide a mensagem."""


class SecretariaError(Exception):
    """Base de todos os erros do sistema."""


class NaoEncontradoError(SecretariaError):
    """Aluno, turma ou matrícula que não existe no banco."""


class RegraDeNegocioError(SecretariaError):
    """O pedido está no formato certo, mas uma regra da escola não permite atendê-lo."""


class BancoIndisponivelError(SecretariaError):
    """Não foi possível abrir ou usar o banco de dados."""
