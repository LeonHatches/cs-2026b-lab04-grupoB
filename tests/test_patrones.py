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
