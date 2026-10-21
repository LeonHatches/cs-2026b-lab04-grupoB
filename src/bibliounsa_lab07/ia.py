"""E5 IA simulada: Strategy + Adapter + caché Decorator + guardrails Chain."""
from abc import ABC, abstractmethod
import re


class ProveedorLLM(ABC):
    @abstractmethod
    def completar(self, prompt):
        raise NotImplementedError


class ClienteLLMSimulado:
    def __init__(self, respuesta):
        self.respuesta = respuesta
        self.llamadas = 0

    def generar(self, texto_entrada):
        self.llamadas += 1
        return {"texto": self.respuesta}


class LLMAdapter(ProveedorLLM):
    def __init__(self, cliente): self.cliente = cliente
    def completar(self, prompt): return self.cliente.generar(texto_entrada=prompt)["texto"]


class ProveedorConCache(ProveedorLLM):
    def __init__(self, interno):
        self.interno = interno
        self._cache = {}

    def completar(self, prompt):
        if prompt not in self._cache:
            self._cache[prompt] = self.interno.completar(prompt)
        return self._cache[prompt]


class Guardrail(ABC):
    def __init__(self, siguiente=None): self.siguiente = siguiente

    def validar(self, texto):
        self._aplicar(texto)
        return self.siguiente.validar(texto) if self.siguiente else texto

    @abstractmethod
    def _aplicar(self, texto): raise NotImplementedError


class SinPreciosInventados(Guardrail):
    def _aplicar(self, texto):
        if re.search(r"S/\s*\d|precio\s*:\s*\d", texto, re.I):
            raise ValueError("La IA no debe inventar precios del catálogo")


class SinDisponibilidadGarantizada(Guardrail):
    def _aplicar(self, texto):
        if any(x in texto.lower() for x in ("disponibilidad garantizada", "stock garantizado", "100% disponible")):
            raise ValueError("La IA no puede asegurar disponibilidad")


class RecomendadorLibros:
    def __init__(self, proveedor: ProveedorLLM, guardrails=None):
        self.proveedor = proveedor
        self.guardrails = guardrails or SinPreciosInventados(SinDisponibilidadGarantizada())

    def recomendar(self, titulo):
        if not titulo.strip():
            raise ValueError("Título vacío")
        respuesta = self.proveedor.completar(f"Sugiere libros similares a: {titulo}")
        return self.guardrails.validar(respuesta)
