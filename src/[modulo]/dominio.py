"""Esqueleto didáctico de diseño BiblioUNSA (Lab 05). No es un backend listo para producción."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

class DisponibilidadEjemplar(Enum):
    DISPONIBLE = "DISPONIBLE"
    RESERVADO = "RESERVADO"
    PRESTADO = "PRESTADO"

class EstadoReserva(Enum):
    SOLICITADA = "SOLICITADA"
    VALIDANDO = "VALIDANDO"
    RESERVADA = "RESERVADA"
    RECHAZADA = "RECHAZADA"
    CANCELADA = "CANCELADA"
    EXPIRADA = "EXPIRADA"
    CONVERTIDA_PRESTAMO = "CONVERTIDA_PRESTAMO"

@dataclass
class Estudiante:
    id: UUID
    correo_institucional: str
    def puede_solicitar_reserva(self) -> bool:
        return self.correo_institucional.endswith("@unsa.edu.pe")

@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    ejemplares: list[Ejemplar] = field(default_factory=list)
    def consultar_ejemplares(self) -> list[Ejemplar]:
        return self.ejemplares

@dataclass
class Ejemplar:
    id: UUID
    codigo_qr: str
    disponibilidad: DisponibilidadEjemplar = DisponibilidadEjemplar.DISPONIBLE
    def verificar_disponible(self) -> bool:
        return self.disponibilidad == DisponibilidadEjemplar.DISPONIBLE
    def marcar_reservado(self) -> None:
        if not self.verificar_disponible():
            raise ValueError("Ejemplar no disponible")
        self.disponibilidad = DisponibilidadEjemplar.RESERVADO
    def liberar(self) -> None:
        self.disponibilidad = DisponibilidadEjemplar.DISPONIBLE

@dataclass
class Reserva:
    estudiante: Estudiante
    ejemplar: Ejemplar
    id: UUID = field(default_factory=uuid4)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    estado: EstadoReserva = EstadoReserva.SOLICITADA
    def confirmar(self) -> None:
        self.ejemplar.marcar_reservado()
        self.estado = EstadoReserva.RESERVADA
    def cancelar(self) -> None:
        self.estado = EstadoReserva.CANCELADA
        self.ejemplar.liberar()
    def expirar(self) -> None:
        self.estado = EstadoReserva.EXPIRADA
        self.ejemplar.liberar()
    def registrar_prestamo(self) -> None:
        if self.estado != EstadoReserva.RESERVADA:
            raise ValueError("Reserva no confirmada")
        self.estado = EstadoReserva.CONVERTIDA_PRESTAMO
        self.ejemplar.disponibilidad = DisponibilidadEjemplar.PRESTADO

class ServicioMatricula(ABC):
    @abstractmethod
    def validar_vigente(self, estudiante_id: UUID) -> bool: ...

class ApiAcademicaAdapter(ServicioMatricula):
    def validar_vigente(self, estudiante_id: UUID) -> bool:
        raise NotImplementedError("Conectar a la API académica, no a su BD")

class RepositorioReservas(ABC):
    @abstractmethod
    def reservar_atomicamente(self, estudiante_id: UUID, ejemplar_id: UUID) -> Reserva: ...
    @abstractmethod
    def buscar(self, reserva_id: UUID) -> Reserva: ...
    @abstractmethod
    def guardar(self, reserva: Reserva) -> None: ...

class RepositorioEjemplares(ABC):
    @abstractmethod
    def buscar(self, ejemplar_id: UUID) -> Ejemplar: ...

class NotificadorReservas(ABC):
    @abstractmethod
    def enviar_confirmacion(self, reserva: Reserva) -> None: ...

@dataclass
class ResultadoReserva:
    exito: bool
    mensaje: str

class ServicioReservas:
    def __init__(self, matricula: ServicioMatricula, ejemplares: RepositorioEjemplares,
                 reservas: RepositorioReservas, notificador: NotificadorReservas):
        self.matricula, self.ejemplares = matricula, ejemplares
        self.reservas, self.notificador = reservas, notificador
    def reservar(self, estudiante_id: UUID, ejemplar_id: UUID) -> Reserva:
        if not self.matricula.validar_vigente(estudiante_id):
            raise ValueError("Matrícula no vigente")
        ejemplar = self.ejemplares.buscar(ejemplar_id)
        if not ejemplar.verificar_disponible():
            raise ValueError("Ejemplar no disponible")
        # La exclusión concurrente real requiere transacción PostgreSQL.
        reserva = self.reservas.reservar_atomicamente(estudiante_id, ejemplar_id)
        self.notificador.enviar_confirmacion(reserva)
        return reserva
    def cancelar_reserva(self, reserva_id: UUID) -> None:
        reserva = self.reservas.buscar(reserva_id)
        reserva.cancelar()
        self.reservas.guardar(reserva)

class ReservaController:
    def __init__(self, servicio: ServicioReservas):
        self.servicio = servicio
    def crear_reserva(self, estudiante_id: UUID, ejemplar_id: UUID) -> ResultadoReserva:
        try:
            self.servicio.reservar(estudiante_id, ejemplar_id)
            return ResultadoReserva(True, "Reserva registrada")
        except (ValueError, TimeoutError) as exc:
            return ResultadoReserva(False, str(exc))
