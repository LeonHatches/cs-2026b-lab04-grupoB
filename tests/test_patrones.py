import pytest

from bibliounsa_lab07.decoradores import MatriculaConReintentos
from bibliounsa_lab07.estados import Prestamo
from bibliounsa_lab07.eventos import (
    PublicadorEventos, ConfirmadorReserva, AuditorReserva
)
from bibliounsa_lab07.ia import (
    ClienteLLMSimulado, LLMAdapter, ProveedorConCache,
    RecomendadorLibros
)

"""E2: extensión y adaptación sin modificar el servicio."""
from bibliounsa_lab07.adaptadores import ServicioMatricula, FabricaMatricula
from bibliounsa_lab07.externos import AcademicoLegado
from bibliounsa_lab07.politicas import FabricaMultas, PoliticaMulta
from bibliounsa_lab07.servicio import ServicioBiblioteca


class MatriculaInventada(ServicioMatricula):
    def __init__(self, sdk): self.sdk = sdk
    def validar_vigente(self, estudiante_id): return estudiante_id == "U001"


def test_factory_extiende_proveedor_sin_cambiar_servicio():
    f = FabricaMatricula(); f.registrar("TERCERO", MatriculaInventada)
    s = ServicioBiblioteca(proveedor="TERCERO", academico=object(), fabrica_matricula=f)
    assert s.reservar("U001", "LIB-01") == "RESERVADA"


def test_adapter_nuevo_traduce_respuesta_de_sdk():
    from bibliounsa_lab07.adaptadores import MatriculaNuevoAdapter
    from bibliounsa_lab07.externos import AcademicoNuevo
    adaptador = MatriculaNuevoAdapter(AcademicoNuevo(vigentes={"U001"}))
    assert adaptador.validar_vigente("U001")
    assert not adaptador.validar_vigente("U002")


def test_strategy_multa_nueva_sin_condicionales():
    class MultaVisitante(PoliticaMulta):
        def calcular(self, dias_retraso): return dias_retraso * 4
    f = FabricaMultas(); f.registrar("VISITANTE", MultaVisitante)
    s = ServicioBiblioteca(fabrica_multas=f)
    assert s.calcular_multa("VISITANTE", 3) == 12


def test_decorator_solo_reintenta_timeout():
    sdk = AcademicoLegado(vigentes={"U001"}, fallas=2)
    from bibliounsa_lab07.adaptadores import MatriculaLegadoAdapter
    r = MatriculaConReintentos(MatriculaLegadoAdapter(sdk), 3)
    assert r.validar_vigente("U001") and sdk.llamadas == 3


def test_decorator_no_reintenta_matricula_no_vigente():
    sdk = AcademicoLegado(vigentes=())
    from bibliounsa_lab07.adaptadores import MatriculaLegadoAdapter
    r = MatriculaConReintentos(MatriculaLegadoAdapter(sdk), 3)
    assert not r.validar_vigente("U001") and sdk.llamadas == 1


def test_state_rechaza_devolucion_sin_prestamo():
    p = Prestamo()
    with pytest.raises(ValueError): p.registrar_devolucion()


def test_state_rutas_alternas_del_lab05():
    p = Prestamo(); p.cancelar(); assert p.estado == "CANCELADO"
    q = Prestamo(); q.expirar(); assert q.estado == "EXPIRADO"
    r = Prestamo(); r.registrar_prestamo(); r.registrar_devolucion(); assert r.estado == "DEVUELTO"


def test_observer_permita_agregar_suscriptor_sin_modificar_servicio():
    bandeja = []
    pub = PublicadorEventos()
    pub.suscribir("reserva_creada", ConfirmadorReserva(bandeja))
    pub.suscribir("reserva_creada", AuditorReserva(bandeja))
    s = ServicioBiblioteca(publicador=pub)
    s.reservar("U001", "LIB-01")
    assert bandeja == ["confirmacion:U001:LIB-01", "auditoria:reserva:LIB-01"]


def test_ia_cache_no_repite_llamada():
    cliente = ClienteLLMSimulado("Recomiendo textos introductorios de algoritmos.")
    r = RecomendadorLibros(ProveedorConCache(LLMAdapter(cliente)))
    assert r.recomendar("Algoritmos") == r.recomendar("Algoritmos")
    assert cliente.llamadas == 1


@pytest.mark.parametrize("respuesta", [
    "Disponible a solo S/ 25", "Este libro tiene disponibilidad garantizada",
    "Stock garantizado en la biblioteca", "Libro 100% disponible",
])
def test_ia_guardrails_bloquean_alucinaciones(respuesta):
    r = RecomendadorLibros(LLMAdapter(ClienteLLMSimulado(respuesta)))
    with pytest.raises(ValueError): r.recomendar("Estructuras de datos")


def test_ia_simulada_valida_sin_api():
    r = RecomendadorLibros(LLMAdapter(ClienteLLMSimulado("Consulta otros textos de estructuras de datos.")))
    assert "estructuras de datos" in r.recomendar("Algoritmos")
