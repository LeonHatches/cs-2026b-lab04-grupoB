"""E6: aprobación humana real sobre una copia temporal."""
from pathlib import Path
from shutil import copytree
from tempfile import TemporaryDirectory
from datetime import datetime
from agente.nucleo import Agente
from agente.herramientas import Herramientas
from agente.politica import Politica, aprobar_en_consola

ROOT = Path(__file__).resolve().parent
RUTA = "src/bibliounsa_lab10/dominio.py"
ANTES = '    if not disponible:\n        return "NO_DISPONIBLE"'
DESPUES = (
    '    if not matricula_vigente:\n'
    '        return "MATRICULA_NO_VIGENTE"\n' + ANTES
)

class ModeloE6:
    def __init__(self):
        self.paso = 0

    def decidir(self, historial):
        self.paso += 1
        if self.paso == 1:
            return {
                "pensamiento": "Solicitar autorización humana",
                "accion": "editar_archivo",
                "args": {
                    "ruta": RUTA,
                    "antes": ANTES,
                    "despues": DESPUES
                }
            }
        return {
            "pensamiento": "Registrar el resultado de la política",
            "final": "Interacción humana finalizada"
        }

with TemporaryDirectory() as temporal:
    copia = Path(temporal) / "copia"
    copytree(ROOT / "trabajo", copia)
    h = Herramientas(copia)
    original = (copia / RUTA).read_text(encoding="utf-8")

    traza = ROOT / "trazas" / (
        "e6_humano_" + datetime.now().strftime("%Y%m%d_%H%M%S%f") + ".jsonl"
    )

    agente = Agente(
        "ejecutor_e6",
        ModeloE6(),
        h,
        Politica(aprobar_edicion=aprobar_en_consola),
        "Verificar aprobación humana para ISSUE-02",
        traza
    )

    print("=== E6: INTERVENCIÓN HUMANA ===")
    agente.ejecutar()

    evento = next(
        e for e in agente.eventos
        if e.get("tipo") == "accion"
        and e.get("accion") == "editar_archivo"
    )

    actual = (copia / RUTA).read_text(encoding="utf-8")
    print("\n=== RESULTADO ===")
    print("Estado:", evento["estado"])
    print("Observación:", evento["observacion"])
    print("Código original intacto:", actual == original)
    print("Traza guardada:", traza)

    if evento["estado"] == "OBSERVANDO":
        print("\nPruebas después de aprobar:")
        print(h.ejecutar_pruebas("tests/test_issue_02.py"))
