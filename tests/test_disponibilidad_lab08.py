"""E2: pruebas de conservación, revalidación y recuperación de solicitudes."""
import pytest

from fitness.disponibilidad import simular


def test_sin_cola_se_pierden_las_20_solicitudes_de_la_caida():
    r = simular(cola_persistente=False)
    assert r['duracion_caida_min'] == 20
    assert r['solicitudes_afectadas'] == 20
    assert r['perdidas'] == 20
    assert r['exitos_finales'] == 80


def test_cola_recupera_solicitudes_sin_perdida_en_cuatro_minutos():
    r = simular()
    assert r['pendientes_al_restaurar'] == r['pendientes_recuperadas'] == 20
    assert r['pendientes_finales'] == r['perdidas'] == 0
    assert r['exitos_finales'] == 100
    assert r['recuperacion_min'] == 4


def test_sin_reprocesar_no_se_validan_las_matriculas_en_cola():
    r = simular(recuperar=False)
    assert r['pendientes_finales'] == 20
    assert r['pendientes_recuperadas'] == 0
    assert r['exitos_finales'] == 80
    assert r['perdidas'] == 0


def test_capacidad_insuficiente_incumple_recuperacion_de_cinco_minutos():
    r = simular(capacidad_recuperacion=3)
    assert r['recuperacion_min'] == 7
    assert r['perdidas'] == 0


@pytest.mark.parametrize('cola', [False, True])
@pytest.mark.parametrize('recuperar', [False, True])
def test_se_conserva_el_total_sin_duplicaciones(cola, recuperar):
    r = simular(cola_persistente=cola, recuperar=recuperar)
    assert r['exitos_finales'] + r['perdidas'] + r['pendientes_finales'] == r['solicitudes_total']
    assert len(r['estados']) == r['solicitudes_total']
    ids_validados = [solicitud for solicitud, _ in r['validaciones']]
    assert len(ids_validados) == len(set(ids_validados))


def test_sin_caida_no_se_encolan_solicitudes():
    r = simular(falla_desde=30, falla_hasta=30)
    assert r['solicitudes_afectadas'] == r['pendientes_recuperadas'] == 0
    assert r['exitos_finales'] == 100


def test_intervalo_semiabierto_y_carga_menor_que_la_caida():
    r = simular(cantidad=31)
    assert r['solicitudes_afectadas'] == r['pendientes_recuperadas'] == 1
    assert r['exitos_finales'] == 31


@pytest.mark.parametrize('argumentos', [
    {'cantidad': -1}, {'falla_desde': -1}, {'falla_hasta': 29},
    {'capacidad_recuperacion': 0}, {'capacidad_recuperacion': 2.5},
])
def test_rechaza_parametros_invalidos(argumentos):
    with pytest.raises(ValueError):
        simular(**argumentos)


def test_reproceso_ocurre_al_regresar_api_sin_esperar_fin_de_llegadas():
    r = simular()
    respuestas = dict(r['validaciones'])
    assert respuestas[30] == 51
    assert respuestas[49] == r['minuto_ultima_recuperacion'] == 54
    assert all(not 30 <= minuto < 50 for _, minuto in r['validaciones'])


def test_matricula_no_vigente_se_rechaza_tambien_al_reprocesar():
    r = simular(matriculas_no_vigentes=(30, 49))
    assert r['estados'][30] == r['estados'][49] == 'RECHAZADA'
    assert r['rechazadas'] == 2 and r['exitos_finales'] == 98
    assert r['pendientes_recuperadas'] == 20 and r['perdidas'] == 0
    assert r['exitos_finales'] + r['rechazadas'] == r['solicitudes_total']


def test_matricula_no_vigente_fuera_de_caida_tampoco_se_valida():
    r = simular(matriculas_no_vigentes=(0,))
    assert r['estados'][0] == 'RECHAZADA'
    assert r['rechazadas'] == 1 and r['exitos_finales'] == 99


def test_pendiente_sin_reproceso_conserva_su_estado_sin_elegibilidad_asumida():
    r = simular(recuperar=False, matriculas_no_vigentes=(30,))
    assert r['estados'][30] == 'PENDIENTE_VALIDACION'
    assert r['rechazadas'] == 0
    assert 30 not in dict(r['validaciones'])


def test_intervalo_vacio_permite_cantidad_cero():
    r = simular(cantidad=0)
    assert r['estados'] == {} and r['validaciones'] == []
    assert r['recuperacion_min'] == r['exitos_finales'] == 0


def test_no_vigente_debe_identificar_una_solicitud_existente():
    with pytest.raises(ValueError):
        simular(matriculas_no_vigentes=(100,))
