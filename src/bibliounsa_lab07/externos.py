"""Servicios EXCLUSIVAMENTE simulados: no contactan APIs reales de la UNSA."""

class AcademicoLegado:
    def __init__(self, vigentes=(), fallas=0):
        self.vigentes = set(vigentes)
        self.fallas = fallas
        self.llamadas = 0

    def validar_matricula(self, estudiante_id):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise TimeoutError("API académica simulada sin respuesta")
        return estudiante_id in self.vigentes


class AcademicoNuevo:
    def __init__(self, vigentes=(), fallas=0):
        self.vigentes = set(vigentes)
        self.fallas = fallas
        self.llamadas = 0

    def obtener_estado(self, codigo):
        self.llamadas += 1
        if self.llamadas <= self.fallas:
            raise TimeoutError("API académica simulada sin respuesta")
        return {"codigo": codigo, "matricula": "VIGENTE" if codigo in self.vigentes else "NO_VIGENTE"}


class CatalogoMemoria:
    """Simula unicidad de reserva activa; producción requeriría PostgreSQL."""
    def __init__(self, ejemplares=("LIB-01",)):
        self.disponibles = set(ejemplares)
        self.reservados = set()

    def esta_disponible(self, ejemplar_id):
        return ejemplar_id in self.disponibles

    def reservar_atomico(self, ejemplar_id):
        # Modelo secuencial para pruebas; NO sustituye transacciones reales.
        if ejemplar_id not in self.disponibles:
            raise ValueError("Ejemplar no disponible")
        self.disponibles.remove(ejemplar_id)
        self.reservados.add(ejemplar_id)
