from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID


# Enumeraciones del diagrama (miembros sin modificaciones).
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


class EstadoPrestamo(Enum):
    RESERVADO = "RESERVADO"
    PRESTADO = "PRESTADO"
    VENCIDO = "VENCIDO"
    CON_MULTA = "CON_MULTA"
    DEVUELTO = "DEVUELTO"
    CANCELADO = "CANCELADO"
    EXPIRADO = "EXPIRADO"


@dataclass
class Estudiante:
    id: UUID
    correo_institucional: str
    # Estudiante (1) -- (0..*) Reserva
    reservas: list[Reserva] = field(default_factory=list, repr=False)

    def puede_solicitar_reserva(self) -> bool:
        raise NotImplementedError


@dataclass
class Libro:
    isbn: str
    titulo: str
    autor: str
    # Libro (1) o-- (0..*) Ejemplar
    ejemplares: list[Ejemplar] = field(default_factory=list, repr=False)

    def consultar_ejemplares(self) -> list[Ejemplar]:
        raise NotImplementedError


@dataclass
class Ejemplar:
    id: UUID
    codigo_qr: str
    libro: Libro
    disponibilidad: DisponibilidadEjemplar = DisponibilidadEjemplar.DISPONIBLE
    # Ejemplar (1) -- (0..*) Reserva: historial
    historial_reservas: list[Reserva] = field(default_factory=list, repr=False)

    def verificar_disponible(self) -> bool:
        return self.disponibilidad == DisponibilidadEjemplar.DISPONIBLE

    def marcar_reservado(self) -> None:
        if not self.verificar_disponible():
            raise ValueError("El ejemplar no está disponible para reservar.")
        self.disponibilidad = DisponibilidadEjemplar.RESERVADO

    def liberar(self) -> None:
        self.disponibilidad = DisponibilidadEjemplar.DISPONIBLE


@dataclass
class Prestamo:
    estado: EstadoPrestamo = EstadoPrestamo.RESERVADO
    # Reserva (0..1) --> (0..1) Prestamo: genera
    reserva: Reserva | None = field(default=None, repr=False)

    def reservar(self) -> None:
        self.estado = EstadoPrestamo.RESERVADO

    def registrar_prestamo(self) -> None:
        self.estado = EstadoPrestamo.PRESTADO
        if self.reserva is not None:
            self.reserva.ejemplar.disponibilidad = DisponibilidadEjemplar.PRESTADO

    def marcar_vencido(self) -> None:
        self.estado = EstadoPrestamo.VENCIDO

    def calcular_multa(self) -> None:
        self.estado = EstadoPrestamo.CON_MULTA

    def registrar_devolucion(self) -> None:
        self.estado = EstadoPrestamo.DEVUELTO
        if self.reserva is not None:
            self.reserva.ejemplar.liberar()

    def cancelar(self) -> None:
        self.estado = EstadoPrestamo.CANCELADO
        if self.reserva is not None:
            self.reserva.ejemplar.liberar()

    def expirar(self) -> None:
        self.estado = EstadoPrestamo.EXPIRADO
        if self.reserva is not None:
            self.reserva.ejemplar.liberar()


@dataclass
class Reserva:
    id: UUID
    fecha_creacion: datetime
    # Cada reserva pertenece a un estudiante y a un ejemplar.
    estudiante: Estudiante
    ejemplar: Ejemplar
    estado: EstadoReserva = EstadoReserva.SOLICITADA
    prestamo: Prestamo | None = field(default=None, repr=False)

    def confirmar(self) -> None:
        if self.estado not in (EstadoReserva.SOLICITADA, EstadoReserva.VALIDANDO):
            raise ValueError("La reserva no se puede confirmar en su estado actual.")
        self.ejemplar.marcar_reservado()
        self.estado = EstadoReserva.RESERVADA

    def cancelar(self) -> None:
        if self.estado in (
            EstadoReserva.CANCELADA,
            EstadoReserva.EXPIRADA,
            EstadoReserva.CONVERTIDA_PRESTAMO,
        ):
            raise ValueError("La reserva no se puede cancelar en su estado actual.")
        if self.estado == EstadoReserva.RESERVADA:
            self.ejemplar.liberar()
        self.estado = EstadoReserva.CANCELADA

    def expirar(self) -> None:
        if self.estado in (
            EstadoReserva.CANCELADA,
            EstadoReserva.EXPIRADA,
            EstadoReserva.CONVERTIDA_PRESTAMO,
        ):
            raise ValueError("La reserva no se puede expirar en su estado actual.")
        if self.estado == EstadoReserva.RESERVADA:
            self.ejemplar.liberar()
        self.estado = EstadoReserva.EXPIRADA

    def registrar_prestamo(self) -> None:
        if self.estado != EstadoReserva.RESERVADA:
            raise ValueError("Solo una reserva confirmada puede generar un préstamo.")
        if self.prestamo is None:
            self.prestamo = Prestamo(reserva=self)
        self.prestamo.registrar_prestamo()
        self.estado = EstadoReserva.CONVERTIDA_PRESTAMO


@dataclass
class ResultadoReserva:
    exito: bool
    mensaje: str


# Puertos: interfaces expresadas mediante ABC.
class ServicioMatricula(ABC):
    @abstractmethod
    def validar_vigente(self, estudiante_id: UUID) -> bool:
        raise NotImplementedError


class RepositorioReservas(ABC):
    @abstractmethod
    def reservar_atomicamente(self, estudiante_id: UUID, ejemplar_id: UUID) -> Reserva:
        """La unicidad de reserva activa se garantiza con transacción PostgreSQL."""
        raise NotImplementedError

    @abstractmethod
    def buscar(self, id: UUID) -> Reserva:
        raise NotImplementedError

    @abstractmethod
    def guardar(self, reserva: Reserva) -> None:
        raise NotImplementedError


class RepositorioEjemplares(ABC):
    @abstractmethod
    def buscar(self, id: UUID) -> Ejemplar:
        raise NotImplementedError


class NotificadorReservas(ABC):
    @abstractmethod
    def enviar_confirmacion(self, reserva: Reserva) -> None:
        raise NotImplementedError


# Adaptador: realiza el puerto ServicioMatricula.
@dataclass
class ApiAcademicaAdapter(ServicioMatricula):
    def validar_vigente(self, estudiante_id: UUID) -> bool:
        raise NotImplementedError


@dataclass
class ServicioReservas:
    # Dependencias hacia los cuatro puertos.
    repositorio_reservas: RepositorioReservas
    repositorio_ejemplares: RepositorioEjemplares
    servicio_matricula: ServicioMatricula
    notificador_reservas: NotificadorReservas

    def reservar(self, estudiante_id: UUID, ejemplar_id: UUID) -> Reserva:
        raise NotImplementedError

    def cancelar_reserva(self, reserva_id: UUID) -> None:
        raise NotImplementedError


@dataclass
class ReservaController:
    servicio_reservas: ServicioReservas

    def crear_reserva(self, estudiante_id: UUID, ejemplar_id: UUID) -> ResultadoReserva:
        raise NotImplementedError
