from fitness.seguridad import (
    autorizacion_insegura,
    autorizacion_segura,
    simular_intentos,
)


def test_modelo_inseguro_acepta_rol_falsificado():
    assert autorizacion_insegura("ADMINISTRADOR")


def test_autorizacion_segura_rechaza_estudiante():
    assert not autorizacion_segura("ESTUDIANTE")


def test_autorizacion_segura_acepta_bibliotecario():
    assert autorizacion_segura("BIBLIOTECARIO")


def test_qa05_cero_accesos_indebidos():
    resultado = simular_intentos(100)
    assert resultado["intentos"] == 100
    assert resultado["accesos_indebidos_antes"] == 100
    assert resultado["accesos_indebidos_despues"] == 0
