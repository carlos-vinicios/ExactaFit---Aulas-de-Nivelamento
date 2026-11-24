"""Schemas da API: o formato do JSON que entra e que sai. São o contrato da API (Aula 8).

Os tipos de dominio.py circulam entre as camadas de dentro; os schemas daqui são o que o cliente
da API vê. As funções ..._saida, no fim do arquivo, convertem um no outro: são o único ponto em
que o formato do JSON encosta no domínio.
"""

from pydantic import BaseModel, ConfigDict

from secretaria.dominio import (
    Aluno,
    Boletim,
    Documento,
    Linha,
    PosicaoRanking,
    RelatorioTurma,
    Situacao,
    Turma,
)
from secretaria.schemas import MatriculaAluno, Nota


class Saida(BaseModel):
    """Base dos schemas de saída: objetos imutáveis."""

    model_config = ConfigDict(frozen=True)


class AlunoSaida(Saida):
    matricula: str
    nome: str
    curso: str


class TurmaSaida(Saida):
    codigo: str
    disciplina: str
    semestre: str
    professor: str
    curso: str


class LinhaBoletim(Saida):
    semestre: str
    codigo: str
    disciplina: str
    nota: float | None
    situacao: Situacao


class BoletimSaida(Saida):
    """Boletim de um aluno: as disciplinas cursadas e a média das notas lançadas."""

    aluno: AlunoSaida
    disciplinas: list[LinhaBoletim]
    media: float | None


class LinhaTurma(Saida):
    matricula: str
    nome: str
    nota: float | None
    situacao: Situacao


class RelatorioTurmaSaida(Saida):
    """Relatório de uma turma: alunos, média e quantos em cada situação."""

    turma: TurmaSaida
    alunos: list[LinhaTurma]
    media: float | None
    contagem: dict[Situacao, int]


class MatriculaSaida(Saida):
    """Uma matrícula: o aluno, a turma, a nota e a situação."""

    aluno: AlunoSaida
    turma: TurmaSaida
    nota: float | None
    situacao: Situacao


class PosicaoSaida(Saida):
    posicao: int
    matricula: str
    nome: str
    media: float


class RankingSaida(Saida):
    """As maiores médias de um curso num semestre."""

    curso: str
    semestre: str
    posicoes: list[PosicaoSaida]


class DocumentoSaida(Saida):
    """Um documento guardado do aluno (exemplo de upload da Aula 9)."""

    nome: str
    tipo: str
    tamanho: int


# Entrada: o que vem no corpo das requisições. Matrícula, código e semestre vêm no caminho.
class NotaEntrada(BaseModel):
    """Corpo do lançamento de nota."""

    model_config = ConfigDict(extra="forbid")

    nota: Nota


class MatriculaEntrada(BaseModel):
    """Corpo da matrícula numa turma."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    matricula: MatriculaAluno


# Conversões: do domínio para o contrato.
def aluno_saida(aluno: Aluno) -> AlunoSaida:
    return AlunoSaida(matricula=aluno.matricula, nome=aluno.nome, curso=aluno.curso)


def documento_saida(documento: Documento) -> DocumentoSaida:
    return DocumentoSaida(
        nome=documento.nome, tipo=documento.tipo, tamanho=documento.tamanho
    )


def turma_saida(turma: Turma) -> TurmaSaida:
    return TurmaSaida(
        codigo=turma.codigo,
        disciplina=turma.disciplina,
        semestre=turma.semestre,
        professor=turma.professor,
        curso=turma.curso,
    )


def boletim_saida(boletim: Boletim) -> BoletimSaida:
    disciplinas = [
        LinhaBoletim(
            semestre=linha.matricula.turma.semestre,
            codigo=linha.matricula.turma.codigo,
            disciplina=linha.matricula.turma.disciplina,
            nota=linha.matricula.nota,
            situacao=linha.situacao,
        )
        for linha in boletim.linhas
    ]
    return BoletimSaida(
        aluno=aluno_saida(boletim.aluno), disciplinas=disciplinas, media=boletim.media
    )


def relatorio_saida(relatorio: RelatorioTurma) -> RelatorioTurmaSaida:
    """Siga boletim_saida: uma LinhaTurma por linha do relatório."""
    raise NotImplementedError("TODO Aula 8, Prática 3")


def matricula_saida(linha: Linha) -> MatriculaSaida:
    """Uma Linha do domínio (matrícula e situação) no formato de MatriculaSaida."""
    raise NotImplementedError("TODO Aula 8, Prática 3")


def ranking_saida(
    curso: str, semestre: str, posicoes: list[PosicaoRanking]
) -> RankingSaida:
    """O curso e o semestre do pedido, e uma PosicaoSaida para cada posição."""
    raise NotImplementedError("TODO Aula 8, Prática 3")
