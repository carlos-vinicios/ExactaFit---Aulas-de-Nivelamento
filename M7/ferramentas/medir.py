"""Mede a Aula 9: vários pedidos ao mesmo tempo em cada rota de ferramentas/espera.py.

    python ferramentas/espera.py      (num terminal, e deixe aberto)
    python ferramentas/medir.py       (noutro terminal: as três rotas)
    python ferramentas/medir.py def   (só uma rota)

Dispara 5 pedidos de 1 segundo ao mesmo tempo e mostra quando cada um terminou. Com as rotas que
não travam o servidor, os 5 terminam juntos, perto de 1 s; com /async-bloqueia, um por segundo.
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlopen

BASE = "http://127.0.0.1:8002"
ROTAS = ["def", "async-bloqueia", "async-espera"]
PEDIDOS = 5


def medir(rota: str) -> None:
    inicio = time.perf_counter()

    def pedir(_: int) -> float:
        with urlopen(f"{BASE}/{rota}?segundos=1", timeout=60) as resposta:
            resposta.read()
        return time.perf_counter() - inicio

    with ThreadPoolExecutor(PEDIDOS) as executor:
        fins = sorted(executor.map(pedir, range(PEDIDOS)))
    tempos = "  ".join(f"{fim:.1f}" for fim in fins)
    print(f"/{rota:<15} terminaram em (s): {tempos}   total: {fins[-1]:.1f} s")


def main() -> None:
    print(f"{PEDIDOS} pedidos de 1 segundo ao mesmo tempo em cada rota")
    for rota in sys.argv[1:] or ROTAS:
        medir(rota)


if __name__ == "__main__":
    main()
