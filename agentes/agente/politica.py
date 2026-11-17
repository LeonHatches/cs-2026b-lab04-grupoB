"""Mínimo privilegio por rol, límites de pasos, edición aprobada por humanos."""
import re
from dataclasses import dataclass, field
from typing import Callable, Optional

@dataclass
class Decision:
    permitido: bool
    motivo: str = ""

@dataclass
class Politica:
    herramientas_permitidas: set = field(default_factory=lambda: {
        "listar_archivos", "leer_archivo", "buscar", "ejecutar_pruebas", "editar_archivo",
        "ver_cambios", "mapa_repo", "anotar", "leer_notas"})
    rutas_protegidas: tuple = ("tests/", "issues/", "conftest.py")
    max_pasos: int = 12
    aprobar_edicion: Optional[Callable[[dict], bool]] = None

    def evaluar(self, accion: str, args: dict, paso: int, *, al_solicitar_aprobacion=None) -> Decision:
        if paso > self.max_pasos:
            return Decision(False, f"Se alcanzó el máximo de {self.max_pasos} pasos")
        if accion not in self.herramientas_permitidas:
            return Decision(False, f"Herramienta no permitida: {accion}")
        if accion == "editar_archivo":
            ruta = args.get("ruta", "")
            if not isinstance(ruta, str) or ruta.startswith(self.rutas_protegidas):
                return Decision(False, f"Ruta protegida: {ruta}")
            if not ruta.startswith("src/") or not ruta.endswith(".py"):
                return Decision(False, f"Edición fuera de src/: {ruta}")
            if self.aprobar_edicion is not None:
                if al_solicitar_aprobacion is not None:
                    al_solicitar_aprobacion()
                if not self.aprobar_edicion(args):
                    return Decision(False, "El revisor humano rechazó la edición")
        return Decision(True)

def aprobar_en_consola(args: dict) -> bool:
    """Intervención humana: solo 's' aprueba; cualquier otro valor no."""
    print("\nEDICIÓN PROPUESTA", args.get("ruta"), "\nANTES:", args.get("antes"), "\nDESPUÉS:", args.get("despues"))
    return input("¿Aprueba la edición? [s/n]: ").strip().lower() == "s"
