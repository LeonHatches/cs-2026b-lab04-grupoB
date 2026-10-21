"""Servicio BiblioUNSA con Strategy, Adapter, Factory, State,
Observer y Decorator. E2-E4 del Laboratorio 07.
"""

from bibliounsa_lab07.adaptadores import FabricaMatricula
from bibliounsa_lab07.decoradores import MatriculaConReintentos
from bibliounsa_lab07.estados import Prestamo
from bibliounsa_lab07.eventos import (
    PublicadorEventos,
    ConfirmadorReserva,
    AuditorReserva,
)
from bibliounsa_lab07.externos import AcademicoLegado, CatalogoMemoria
from bibliounsa_lab07.politicas import FabricaMultas


class ServicioBiblioteca:
    def __init__(
        self,
        proveedor="LEGADO",
        academico=None,
        catalogo=None,
        fabrica_matricula=None,
        fabrica_multas=None,
        publicador=None,
    ):
        self.proveedor = proveedor
        self.academico = (
            academico if academico is not None
            else AcademicoLegado(vigentes={"U001"})
        )
        self.catalogo = (
            catalogo if catalogo is not None else CatalogoMemoria()
        )
        self.eventos = []
        self.fabrica_matricula = (
            fabrica_matricula if fabrica_matricula is not None
            else FabricaMatricula()
        )
        self.fabrica_multas = (
            fabrica_multas if fabrica_multas is not None
            else FabricaMultas()
        )

        # Observer: permite incorporar suscriptores externos.
        self.publicador = (
            publicador if publicador is not None
            else PublicadorEventos()
        )

        if publicador is None:
            self.publicador.suscribir(
                "reserva_creada", ConfirmadorReserva(self.eventos)
            )
            self.publicador.suscribir(
                "reserva_creada", AuditorReserva(self.eventos)
            )

    def reservar(self, estudiante_id, ejemplar_id):
        if not estudiante_id:
            raise ValueError("Estudiante inválido")

        if not ejemplar_id:
            raise ValueError("Ejemplar inválido")

        # Factory + Adapter.
        matricula = self.fabrica_matricula.crear(
            self.proveedor, self.academico
        )

        # Decorator: reintenta únicamente ante TimeoutError.
        matricula = MatriculaConReintentos(matricula, intentos=3)
        vigente = matricula.validar_vigente(estudiante_id)

        if not vigente:
            raise ValueError("Matrícula no vigente")

        if not self.catalogo.esta_disponible(ejemplar_id):
            raise ValueError("Ejemplar no disponible")

        self.catalogo.reservar_atomico(ejemplar_id)

        # Observer: publica el evento sin conocer los suscriptores.
        self.publicador.publicar(
            "reserva_creada",
            {
                "estudiante": estudiante_id,
                "ejemplar": ejemplar_id,
            },
        )

        return "RESERVADA"

    def calcular_multa(self, tipo_usuario, dias_retraso):
        if dias_retraso < 0:
            raise ValueError("Días de retraso inválidos")

        return self.fabrica_multas.crear(tipo_usuario).calcular(
            dias_retraso
        )
