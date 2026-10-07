"""Modelo mínimo complementario para verificar la máquina de estados E3."""
from dataclasses import dataclass
from enum import Enum
class EstadoPrestamo(Enum):
    RESERVADO="RESERVADO"
    PRESTADO="PRESTADO"
    VENCIDO="VENCIDO"
    CON_MULTA="CON_MULTA"
    DEVUELTO="DEVUELTO"
    CANCELADO="CANCELADO"
    EXPIRADO="EXPIRADO"
@dataclass
class Prestamo:
    estado: EstadoPrestamo = EstadoPrestamo.RESERVADO
    def reservar(self): self.estado=EstadoPrestamo.RESERVADO
    def registrar_prestamo(self): self.estado=EstadoPrestamo.PRESTADO
    def marcar_vencido(self): self.estado=EstadoPrestamo.VENCIDO
    def calcular_multa(self): self.estado=EstadoPrestamo.CON_MULTA
    def registrar_devolucion(self): self.estado=EstadoPrestamo.DEVUELTO
    def cancelar(self): self.estado=EstadoPrestamo.CANCELADO
    def expirar(self): self.estado=EstadoPrestamo.EXPIRADO
