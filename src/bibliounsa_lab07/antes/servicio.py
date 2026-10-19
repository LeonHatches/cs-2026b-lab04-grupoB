"""E1: versión deliberadamente acoplada del flujo de reserva BiblioUNSA.

Se preserva para comparar y ejecutar las MISMAS pruebas de caracterización.
"""
from bibliounsa_lab07.externos import AcademicoLegado, AcademicoNuevo, CatalogoMemoria


class ServicioBiblioteca:
    def __init__(self, proveedor="LEGADO", academico=None, catalogo=None):
        self.proveedor = proveedor
        self.academico = academico or AcademicoLegado(vigentes={"U001"})
        self.catalogo = catalogo or CatalogoMemoria()
        self.eventos = []

    def reservar(self, estudiante_id, ejemplar_id):
        if not estudiante_id:
            raise ValueError("Estudiante inválido")
        if not ejemplar_id:
            raise ValueError("Ejemplar inválido")
        vigente = False
        # Olor E1: variantes, formato de SDK y reintentos mezclados en el dominio.
        if self.proveedor == "LEGADO":
            for intento in range(3):
                try:
                    vigente = self.academico.validar_matricula(estudiante_id)
                    break
                except TimeoutError:
                    if intento == 2:
                        raise
        elif self.proveedor == "NUEVO":
            for intento in range(3):
                try:
                    respuesta = self.academico.obtener_estado(codigo=estudiante_id)
                    vigente = respuesta["matricula"] == "VIGENTE"
                    break
                except TimeoutError:
                    if intento == 2:
                        raise
        else:
            raise ValueError("Proveedor académico no soportado")
        if not vigente:
            raise ValueError("Matrícula no vigente")
        if not self.catalogo.esta_disponible(ejemplar_id):
            raise ValueError("Ejemplar no disponible")
        self.catalogo.reservar_atomico(ejemplar_id)
        # Olor: notificaciones y auditoría acopladas al caso de uso.
        self.eventos.append(f"confirmacion:{estudiante_id}:{ejemplar_id}")
        self.eventos.append(f"auditoria:reserva:{ejemplar_id}")
        return "RESERVADA"

    def calcular_multa(self, tipo_usuario, dias_retraso):
        if dias_retraso < 0:
            raise ValueError("Días de retraso inválidos")
        # Olor: el tipo de usuario determina una política mediante condicionales.
        if tipo_usuario == "ESTUDIANTE":
            return dias_retraso * 2.0
        elif tipo_usuario == "DOCENTE":
            return dias_retraso * 1.0
        else:
            raise ValueError("Tipo de usuario no soportado")


class Prestamo:
    """E1: condicionales sobre estados; después se refactorizan a State."""
    def __init__(self):
        self.estado = "RESERVADO"

    def registrar_prestamo(self):
        if self.estado != "RESERVADO":
            raise ValueError("Transición inválida")
        self.estado = "PRESTADO"

    def marcar_vencido(self):
        if self.estado != "PRESTADO":
            raise ValueError("Transición inválida")
        self.estado = "VENCIDO"

    def calcular_multa(self, dias_retraso):
        if self.estado != "VENCIDO" or dias_retraso <= 0:
            raise ValueError("Transición inválida")
        self.estado = "CON_MULTA"

    def registrar_devolucion(self):
        if self.estado not in ("PRESTADO", "CON_MULTA"):
            raise ValueError("Transición inválida")
        self.estado = "DEVUELTO"

    def cancelar(self):
        if self.estado != "RESERVADO":
            raise ValueError("Transición inválida")
        self.estado = "CANCELADO"

    def expirar(self):
        if self.estado != "RESERVADO":
            raise ValueError("Transición inválida")
        self.estado = "EXPIRADO"
