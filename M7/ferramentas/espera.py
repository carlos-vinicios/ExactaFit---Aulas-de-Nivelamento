"""Servidor de demonstração da Aula 9: def, async def e o laço de eventos.

    python ferramentas/espera.py

Sobe em http://127.0.0.1:8002, com um processo só (sem --reload). Cada rota espera alguns
segundos (5, ou o valor de ?segundos=) de um jeito diferente:

* /def             espera com time.sleep numa rota def: o FastAPI a roda numa thread à parte;
* /async-bloqueia  espera com time.sleep numa rota async def: trava o laço de eventos;
* /async-espera    espera com await asyncio.sleep numa rota async def: libera o laço;
* /agora           responde na hora. Chame-a enquanto outra rota espera, noutro terminal.

Para medir com vários pedidos ao mesmo tempo: python ferramentas/medir.py
"""

import asyncio
import time
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query

app = FastAPI(title="Demonstração: def e async def", description="Exemplo da Aula 9.")

Segundos = Annotated[float, Query(gt=0, le=30)]


@app.get("/def")
def com_def(segundos: Segundos = 5) -> dict[str, str]:
    """Espera como uma consulta ao banco com uma biblioteca síncrona."""
    time.sleep(segundos)
    return {"rota": "def", "esperou": f"{segundos} s"}


@app.get("/async-bloqueia")
async def async_bloqueia(segundos: Segundos = 5) -> dict[str, str]:
    """O erro: código síncrono dentro de async def. Ninguém mais é atendido enquanto isso.

    O ruff aponta esse erro (ASYNC251); aqui ele fica de propósito, para a demonstração.
    """
    time.sleep(segundos)  # noqa: ASYNC251
    return {"rota": "async-bloqueia", "esperou": f"{segundos} s"}


@app.get("/async-espera")
async def async_espera(segundos: Segundos = 5) -> dict[str, str]:
    """Assíncrono de verdade: enquanto espera, o laço de eventos atende outros pedidos."""
    await asyncio.sleep(segundos)
    return {"rota": "async-espera", "esperou": f"{segundos} s"}


@app.get("/agora")
def agora() -> dict[str, str]:
    """Responde na hora, com o horário do servidor."""
    return {"hora": time.strftime("%H:%M:%S")}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8002)
