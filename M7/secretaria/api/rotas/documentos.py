"""Rotas dos documentos de um aluno: exemplo de upload e download (Aula 9).

O corpo do upload não é JSON: é multipart/form-data, o formato dos formulários com arquivo. O
FastAPI entrega o arquivo como UploadFile (precisa do pacote python-multipart).
"""

from typing import Annotated
from urllib.parse import quote

from fastapi import APIRouter, File, Response, UploadFile, status

from secretaria.schemas import MatriculaAluno
from secretaria.servicos import documentos

from ..schemas import DocumentoSaida, documento_saida

rotas = APIRouter(prefix="/alunos/{matricula}/documentos", tags=["documentos"])


@rotas.post("", status_code=status.HTTP_201_CREATED)
def enviar(
    matricula: MatriculaAluno,
    arquivo: Annotated[UploadFile, File()],
    resposta: Response,
) -> DocumentoSaida:
    """Guarda um documento do aluno: PDF, PNG ou JPEG, até 2 MB."""
    conteudo = arquivo.file.read()  # rota def: lê pelo arquivo comum, sem await
    documento = documentos.guardar_documento(
        matricula, arquivo.filename or "", arquivo.content_type or "", conteudo
    )
    resposta.headers["Location"] = (
        f"/alunos/{matricula}/documentos/{quote(documento.nome)}"
    )
    return documento_saida(documento)


@rotas.get("")
def listar(matricula: MatriculaAluno) -> list[DocumentoSaida]:
    """Os documentos guardados do aluno."""
    return [documento_saida(d) for d in documentos.listar_documentos(matricula)]


@rotas.get("/{nome}", response_class=Response)
def baixar(matricula: MatriculaAluno, nome: str) -> Response:
    """O arquivo, com o tipo de mídia certo, para baixar."""
    documento, conteudo = documentos.ler_documento(matricula, nome)
    disposicao = f"attachment; filename*=utf-8''{quote(documento.nome)}"
    return Response(
        conteudo, media_type=documento.tipo, headers={"Content-Disposition": disposicao}
    )
