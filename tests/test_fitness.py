"""Fitness functions de calidad para BiblioUNSA."""

from fitness.rendimiento import simular_catalogo
from fitness.disponibilidad import simular as simular_caida
from fitness.seguridad import simular_intentos


def test_ff03_p95_simulado_con_cache_bajo_500ms():
    resultado = simular_catalogo(tactica="indice_cache")

    assert resultado["p95_ms"] <= 500


def test_ff04_no_hay_reservas_perdidas_tras_reconexion():
    resultado = simular_caida(cola_persistente=True)

    assert resultado["perdidas"] == 0
    assert resultado["pendientes_finales"] == 0


def test_ff05_restriccion_acceso_estudiante():
    resultado = simular_intentos(total=100)

    assert resultado["accesos_indebidos_despues"] == 0
    assert resultado["accesos_indebidos_antes"] == 100