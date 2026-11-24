"""A aplicação FastAPI: junta as rotas de cada recurso (Aula 9).

    uvicorn secretaria.api.app:app --reload

A documentação automática fica em http://127.0.0.1:8000/docs, gerada a partir das rotas e dos
schemas.
"""

from fastapi import FastAPI

from . import erros
from .rotas import alunos, cursos, documentos, turmas

app = FastAPI(
    title="API da secretaria",
    version="1.0",
    description="Boletins, turmas, matrículas, notas e documentos da escola (M7).",
)
app.include_router(alunos.rotas)
app.include_router(turmas.rotas)
app.include_router(cursos.rotas)
app.include_router(documentos.rotas)
erros.registrar(app)


@app.get("/saude", tags=["saúde"])
def saude() -> dict[str, str]:
    """Responde se a API está no ar."""
    return {"status": "ok"}
