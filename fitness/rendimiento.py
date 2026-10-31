"""Simulación reproducible de rendimiento del catálogo BiblioUNSA."""

import math
import random
import statistics


def simular_catalogo(tactica="sin_optimizar", solicitudes=1200, semilla=42):
    rnd = random.Random(semilla)
    latencias = []

    for _ in range(solicitudes):
        if tactica == "sin_optimizar":
            latencia = rnd.uniform(450, 850)
        elif tactica == "indice":
            latencia = rnd.uniform(160, 350)
        elif tactica == "indice_cache":
            latencia = rnd.uniform(45, 160)
        else:
            raise ValueError("Táctica no reconocida")

        latencias.append(latencia)

    latencias.sort()
    posicion = math.ceil(0.95 * len(latencias)) - 1

    return {
        "tactica": tactica,
        "solicitudes": solicitudes,
        "carga_objetivo_rps": 12,
        "p95_ms": round(latencias[posicion], 2),
        "promedio_ms": round(statistics.mean(latencias), 2),
        "cumple_qa01": latencias[posicion] <= 500,
    }


if __name__ == "__main__":
    for tactica in ("sin_optimizar", "indice", "indice_cache"):
        resultado = simular_catalogo(tactica)
        print(
            f"{resultado['tactica']}: "
            f"p95={resultado['p95_ms']} ms | "
            f"promedio={resultado['promedio_ms']} ms | "
            f"cumple QA-01={resultado['cumple_qa01']}"
        )
