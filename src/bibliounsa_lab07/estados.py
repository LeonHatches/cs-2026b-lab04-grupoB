"""E3 State: transiciones del préstamo tomadas del diagrama de Lab 05."""


class EstadoPrestamoBase:
    nombre = "?"

    def _invalida(self):
        raise ValueError("Transición inválida")

    def registrar_prestamo(self, prestamo): self._invalida()
    def marcar_vencido(self, prestamo): self._invalida()
    def calcular_multa(self, prestamo, dias_retraso): self._invalida()
    def registrar_devolucion(self, prestamo): self._invalida()
    def cancelar(self, prestamo): self._invalida()
    def expirar(self, prestamo): self._invalida()


class Reservado(EstadoPrestamoBase):
    nombre = "RESERVADO"
    def registrar_prestamo(self, prestamo): prestamo.cambiar_a(Prestado())
    def cancelar(self, prestamo): prestamo.cambiar_a(Cancelado())
    def expirar(self, prestamo): prestamo.cambiar_a(Expirado())


class Prestado(EstadoPrestamoBase):
    nombre = "PRESTADO"
    def marcar_vencido(self, prestamo): prestamo.cambiar_a(Vencido())
    def registrar_devolucion(self, prestamo): prestamo.cambiar_a(Devuelto())


class Vencido(EstadoPrestamoBase):
    nombre = "VENCIDO"
    def calcular_multa(self, prestamo, dias_retraso):
        if dias_retraso <= 0:
            raise ValueError("Transición inválida")
        prestamo.cambiar_a(ConMulta())


class ConMulta(EstadoPrestamoBase):
    nombre = "CON_MULTA"
    def registrar_devolucion(self, prestamo): prestamo.cambiar_a(Devuelto())


class Devuelto(EstadoPrestamoBase): nombre = "DEVUELTO"
class Cancelado(EstadoPrestamoBase): nombre = "CANCELADO"
class Expirado(EstadoPrestamoBase): nombre = "EXPIRADO"


class Prestamo:
    def __init__(self):
        self._estado = Reservado()

    @property
    def estado(self):
        return self._estado.nombre

    def cambiar_a(self, estado):
        self._estado = estado

    def registrar_prestamo(self): self._estado.registrar_prestamo(self)
    def marcar_vencido(self): self._estado.marcar_vencido(self)
    def calcular_multa(self, dias_retraso): self._estado.calcular_multa(self, dias_retraso)
    def registrar_devolucion(self): self._estado.registrar_devolucion(self)
    def cancelar(self): self._estado.cancelar(self)
    def expirar(self): self._estado.expirar(self)
