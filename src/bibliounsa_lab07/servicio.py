"""E2: Adapter, Strategy y Factory para el flujo simulado de reserva.

Los reintentos y avisos conservan su forma inicial hasta E3-E4.
"""
from bibliounsa_lab07.adaptadores import FabricaMatricula
from bibliounsa_lab07.antes.servicio import Prestamo  # Ciclo inicial; E3 aplicará State.
from bibliounsa_lab07.externos import AcademicoLegado, CatalogoMemoria
from bibliounsa_lab07.politicas import FabricaMultas


class ServicioBiblioteca:
    def __init__(self, proveedor="LEGADO", academico=None, catalogo=None,
                 fabrica_matricula=None, fabrica_multas=None):
        self.proveedor = proveedor
        self.academico = academico if academico is not None else AcademicoLegado(vigentes={"U001"})
        self.catalogo = catalogo if catalogo is not None else CatalogoMemoria()
        self.eventos = []
        self.fabrica_matricula = fabrica_matricula if fabrica_matricula is not None else FabricaMatricula()
        self.fabrica_multas = fabrica_multas if fabrica_multas is not None else FabricaMultas()

    def reservar(self, estudiante_id, ejemplar_id):
        if not estudiante_id:
            raise ValueError("Estudiante inválido")
        if not ejemplar_id:
            raise ValueError("Ejemplar inválido")
        matricula = self.fabrica_matricula.crear(self.proveedor, self.academico)
        for intento in range(3):
            try:
                vigente = matricula.validar_vigente(estudiante_id)
                break
            except TimeoutError:
                if intento == 2:
                    raise
        if not vigente:
            raise ValueError("Matrícula no vigente")
        if not self.catalogo.esta_disponible(ejemplar_id):
            raise ValueError("Ejemplar no disponible")
        self.catalogo.reservar_atomico(ejemplar_id)
        self.eventos.append(f"confirmacion:{estudiante_id}:{ejemplar_id}")
        self.eventos.append(f"auditoria:reserva:{ejemplar_id}")
        return "RESERVADA"

    def calcular_multa(self, tipo_usuario, dias_retraso):
        if dias_retraso < 0:
            raise ValueError("Días de retraso inválidos")
        return self.fabrica_multas.crear(tipo_usuario).calcular(dias_retraso)
