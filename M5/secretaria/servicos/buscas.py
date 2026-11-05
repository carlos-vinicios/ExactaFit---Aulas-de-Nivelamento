"""Buscas que todo serviço faz: o registro existe ou o pedido para aqui."""

from secretaria import acesso_dados as dados
from secretaria.dominio import Aluno, Matricula, Turma
from secretaria.erros import NaoEncontradoError


def aluno_existente(con: dados.Conexao, matricula: str) -> Aluno:
    aluno = dados.buscar_aluno(con, matricula)
    if aluno is None:
        raise NaoEncontradoError(f"aluno {matricula} não encontrado")
    return aluno


def turma_existente(con: dados.Conexao, codigo: str, semestre: str) -> Turma:
    turma = dados.buscar_turma(con, codigo, semestre)
    if turma is None:
        raise NaoEncontradoError(f"turma {codigo} ({semestre}) não encontrada")
    return turma


def matricula_existente(con: dados.Conexao, aluno: Aluno, turma: Turma) -> Matricula:
    matricula = dados.buscar_matricula(con, aluno.id, turma.id)
    if matricula is None:
        raise NaoEncontradoError(
            f"{aluno.matricula} não está matriculado em {turma.codigo} ({turma.semestre})"
        )
    return matricula
