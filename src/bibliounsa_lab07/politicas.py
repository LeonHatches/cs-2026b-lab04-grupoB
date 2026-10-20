"""Strategy de multa por tipo de usuario, alineado con Tabla 7 (BiblioUNSA)."""
from abc import ABC, abstractmethod


class PoliticaMulta(ABC):
    @abstractmethod
    def calcular(self, dias_retraso):
        raise NotImplementedError


class MultaEstudiante(PoliticaMulta):
    def calcular(self, dias_retraso):
        return dias_retraso * 2.0


class MultaDocente(PoliticaMulta):
    def calcular(self, dias_retraso):
        return dias_retraso * 1.0


class FabricaMultas:
    def __init__(self):
        self._politicas = {"ESTUDIANTE": MultaEstudiante, "DOCENTE": MultaDocente}

    def registrar(self, tipo, politica):
        self._politicas[tipo] = politica

    def crear(self, tipo):
        if tipo not in self._politicas:
            raise ValueError("Tipo de usuario no soportado")
        return self._politicas[tipo]()
