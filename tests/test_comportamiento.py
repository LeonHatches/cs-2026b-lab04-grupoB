"""E1-E2: las mismas pruebas corren sobre antes y después (sin servicios reales)."""
import importlib
import pytest
from bibliounsa_lab07.externos import AcademicoLegado, AcademicoNuevo, CatalogoMemoria


@pytest.fixture(params=["bibliounsa_lab07.antes.servicio"])
def modulo(request):
    return importlib.import_module(request.param)


def crear(modulo, proveedor="LEGADO", vigentes=("U001",), fallas=0, disponibles=("LIB-01",)):
    sdk = (AcademicoLegado if proveedor == "LEGADO" else AcademicoNuevo)(vigentes, fallas)
    cat = CatalogoMemoria(disponibles)
    return modulo.ServicioBiblioteca(proveedor, sdk, cat), sdk, cat


def test_reserva_legado_confirmada_con_dos_eventos(modulo):
    s, _, cat = crear(modulo)
    assert s.reservar("U001", "LIB-01") == "RESERVADA"
    assert s.eventos == ["confirmacion:U001:LIB-01", "auditoria:reserva:LIB-01"]
    assert not cat.esta_disponible("LIB-01")


def test_reserva_academico_nuevo(modulo):
    s, _, _ = crear(modulo, proveedor="NUEVO")
    assert s.reservar("U001", "LIB-01") == "RESERVADA"


def test_matricula_no_vigente_no_emite_eventos(modulo):
    s, _, cat = crear(modulo, vigentes=())
    with pytest.raises(ValueError, match="Matrícula no vigente"):
        s.reservar("U001", "LIB-01")
    assert s.eventos == [] and cat.esta_disponible("LIB-01")


def test_ejemplar_no_disponible(modulo):
    s, _, _ = crear(modulo, disponibles=())
    with pytest.raises(ValueError, match="Ejemplar no disponible"):
        s.reservar("U001", "LIB-01")
    assert s.eventos == []


def test_reserva_duplicada_no_produce_mas_eventos(modulo):
    s, _, _ = crear(modulo)
    s.reservar("U001", "LIB-01")
    with pytest.raises(ValueError, match="Ejemplar no disponible"):
        s.reservar("U001", "LIB-01")
    assert len(s.eventos) == 2


def test_dos_timeouts_y_tercer_intento_ok(modulo):
    s, sdk, _ = crear(modulo, fallas=2)
    assert s.reservar("U001", "LIB-01") == "RESERVADA"
    assert sdk.llamadas == 3


def test_tres_timeouts_propagados(modulo):
    s, sdk, cat = crear(modulo, fallas=3)
    with pytest.raises(TimeoutError):
        s.reservar("U001", "LIB-01")
    assert sdk.llamadas == 3 and cat.esta_disponible("LIB-01")


def test_proveedor_no_soportado(modulo):
    with pytest.raises(ValueError, match="Proveedor académico no soportado"):
        s, _, _ = crear(modulo, proveedor="OTRO")
        s.reservar("U001", "LIB-01")


def test_tipo_estudiante_multa(modulo):
    s, _, _ = crear(modulo)
    assert s.calcular_multa("ESTUDIANTE", 3) == 6.0


def test_tipo_docente_multa(modulo):
    s, _, _ = crear(modulo)
    assert s.calcular_multa("DOCENTE", 3) == 3.0


def test_multa_no_negativa(modulo):
    s, _, _ = crear(modulo)
    with pytest.raises(ValueError, match="Días de retraso inválidos"):
        s.calcular_multa("ESTUDIANTE", -1)


def test_usuario_invalido_no_registra_reserva(modulo):
    s, _, cat = crear(modulo)
    with pytest.raises(ValueError, match="Estudiante inválido"):
        s.reservar("", "LIB-01")
    assert cat.esta_disponible("LIB-01")


def test_prestamo_ciclo_vida(modulo):
    p = modulo.Prestamo()
    assert p.estado == "RESERVADO"
    p.registrar_prestamo(); p.marcar_vencido(); p.calcular_multa(2)
    p.registrar_devolucion()
    assert p.estado == "DEVUELTO"


def test_prestamo_transicion_invalida(modulo):
    p = modulo.Prestamo()
    with pytest.raises(ValueError, match="Transición inválida"):
        p.registrar_devolucion()
    assert p.estado == "RESERVADO"


def test_ejemplar_invalido_no_consulta_matricula(modulo):
    s, sdk, cat = crear(modulo)
    with pytest.raises(ValueError, match="Ejemplar inválido"):
        s.reservar("U001", "")
    assert sdk.llamadas == 0 and s.eventos == []
    assert cat.esta_disponible("LIB-01")


@pytest.mark.parametrize("proveedor", ["LEGADO", "NUEVO"])
def test_matricula_rechazada_no_se_reintenta(modulo, proveedor):
    s, sdk, cat = crear(modulo, proveedor=proveedor, vigentes=())
    with pytest.raises(ValueError, match="Matrícula no vigente"):
        s.reservar("U001", "LIB-01")
    assert sdk.llamadas == 1 and cat.esta_disponible("LIB-01")
    assert s.eventos == []


def test_nuevo_reintenta_solo_hasta_tres_consultas(modulo):
    s, sdk, _ = crear(modulo, proveedor="NUEVO", fallas=2)
    assert s.reservar("U001", "LIB-01") == "RESERVADA"
    assert sdk.llamadas == 3


def test_error_no_transitorio_se_propaga_sin_reintentar(modulo):
    class AcademicoConError:
        llamadas = 0

        def validar_matricula(self, estudiante_id):
            self.llamadas += 1
            raise RuntimeError("Respuesta académica inválida")

    sdk = AcademicoConError()
    cat = CatalogoMemoria()
    s = modulo.ServicioBiblioteca(academico=sdk, catalogo=cat)
    with pytest.raises(RuntimeError, match="Respuesta académica inválida"):
        s.reservar("U001", "LIB-01")
    assert sdk.llamadas == 1 and cat.esta_disponible("LIB-01")
    assert s.eventos == []


def test_multa_cero_y_tipo_desconocido(modulo):
    s, _, _ = crear(modulo)
    assert s.calcular_multa("ESTUDIANTE", 0) == 0
    with pytest.raises(ValueError, match="Tipo de usuario no soportado"):
        s.calcular_multa("OTRO", 1)


def test_conflicto_atomico_no_confirma_ni_notifica(modulo):
    class CatalogoConConflicto(CatalogoMemoria):
        def reservar_atomico(self, ejemplar_id):
            raise ValueError("Conflicto de reserva")

    s = modulo.ServicioBiblioteca(catalogo=CatalogoConConflicto())
    with pytest.raises(ValueError, match="Conflicto de reserva"):
        s.reservar("U001", "LIB-01")
    assert s.eventos == []
