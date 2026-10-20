"""E4 Observer: el servicio no conoce suscriptores concretos."""


class PublicadorEventos:
    def __init__(self):
        self._suscriptores = {}

    def suscribir(self, tipo, suscriptor):
        self._suscriptores.setdefault(tipo, []).append(suscriptor)

    def publicar(self, tipo, datos):
        for suscriptor in self._suscriptores.get(tipo, []):
            suscriptor.actualizar(datos)


class ConfirmadorReserva:
    def __init__(self, bandeja): self.bandeja = bandeja
    def actualizar(self, datos):
        self.bandeja.append(f"confirmacion:{datos['estudiante']}:{datos['ejemplar']}")


class AuditorReserva:
    def __init__(self, bandeja): self.bandeja = bandeja
    def actualizar(self, datos):
        self.bandeja.append(f"auditoria:reserva:{datos['ejemplar']}")
