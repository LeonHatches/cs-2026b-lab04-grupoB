"""Decorator: reintentar solamente fallos transitorios y cachear respuestas LLM."""
from bibliounsa_lab07.adaptadores import ServicioMatricula


class MatriculaConReintentos(ServicioMatricula):
    def __init__(self, interno: ServicioMatricula, intentos=3):
        self.interno = interno
        self.intentos = intentos

    def validar_vigente(self, estudiante_id):
        for intento in range(self.intentos):
            try:
                return self.interno.validar_vigente(estudiante_id)
            except TimeoutError:
                if intento == self.intentos - 1:
                    raise
