from fitness.rendimiento import simular_catalogo


def test_escenario_base_no_cumple():
    resultado = simular_catalogo("sin_optimizar")
    assert not resultado["cumple_qa01"]


def test_indice_mejora_rendimiento():
    base = simular_catalogo("sin_optimizar")
    indice = simular_catalogo("indice")
    assert indice["p95_ms"] < base["p95_ms"]


def test_indice_cache_cumple_presupuesto():
    resultado = simular_catalogo("indice_cache")
    assert resultado["p95_ms"] <= 500


def test_cache_mejora_sobre_indice():
    indice = simular_catalogo("indice")
    cache = simular_catalogo("indice_cache")
    assert cache["p95_ms"] < indice["p95_ms"]
