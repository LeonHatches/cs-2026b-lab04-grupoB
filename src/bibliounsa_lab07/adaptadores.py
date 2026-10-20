"""Strategy (puerto común), Adapter (dos SDK) y Factory (registro)."""
from abc import ABC, abstractmethod


class ServicioMatricula(ABC):
    @abstractmethod
    def validar_vigente(self, estudiante_id):
        """Devuelve bool o lanza TimeoutError (solo en fallo transitorio)."""
        raise NotImplementedError


class MatriculaLegadoAdapter(ServicioMatricula):
    def __init__(self, sdk):
        self.sdk = sdk

    def validar_vigente(self, estudiante_id):
        return self.sdk.validar_matricula(estudiante_id)


class MatriculaNuevoAdapter(ServicioMatricula):
    def __init__(self, sdk):
        self.sdk = sdk

    def validar_vigente(self, estudiante_id):
        respuesta = self.sdk.obtener_estado(codigo=estudiante_id)
        return respuesta["matricula"] == "VIGENTE"


class FabricaMatricula:
    def __init__(self):
        self._creadores = {}
        self.registrar("LEGADO", MatriculaLegadoAdapter)
        self.registrar("NUEVO", MatriculaNuevoAdapter)

    def registrar(self, nombre, creador):
        self._creadores[nombre] = creador

    def crear(self, nombre, sdk):
        if nombre not in self._creadores:
            raise ValueError("Proveedor académico no soportado")
        return self._creadores[nombre](sdk)
