"""E4: núcleo del Lab 10 conectado a herramientas MCP reales.

Las decisiones del modelo son guiadas para una prueba reproducible.
La autorización de escritura corresponde exclusivamente a la persona.
"""
import sys
from pathlib import Path

from mcp import StdioServerParameters

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "agentes"))

from agente.nucleo import Agente
from agente.politica import Politica, Decision
from bibliounsa_mcp.agente.herramientas_mcp import HerramientasMCP


class PoliticaMCP(Politica):
    def evaluar(self, accion, args, paso, *, al_solicitar_aprobacion=None):
        veredicto = super().evaluar(
            accion, args, paso,
            al_solicitar_aprobacion=al_solicitar_aprobacion,
        )
        if not veredicto.permitido or accion != "crear_reserva":
            return veredicto

        if al_solicitar_aprobacion:
            al_solicitar_aprobacion()

        print("\nESCRITURA MCP PROPUESTA:", accion, args)
        respuesta = input("¿Autoriza crear la reserva? [s/n]: ").strip().lower()

        if respuesta != "s":
            return Decision(False, "El humano rechazó crear_reserva")

        return veredicto


class ModeloGuiado:
    def __init__(self):
        self.paso = 0
        self.acciones = [
            ("buscar_libro", {"texto": "Algoritmos"}),
            ("prestamos_vencidos", {"hoy": "ayer"}),
            ("prestamos_vencidos", {"hoy": "2026-11-23"}),
            ("crear_reserva", {
                "usuario": "EST-001",
                "libro_id": "LIB-001",
                "matricula_vigente": True,
            }),
        ]

    def decidir(self, historial):
        self.paso += 1

        if self.paso <= len(self.acciones):
            accion, args = self.acciones[self.paso - 1]
            return {
                "pensamiento": "Verificar la integración y la política MCP",
                "accion": accion,
                "args": args,
            }

        return {
            "pensamiento": "Concluir la prueba de integración",
            "final": "Flujo MCP del agente finalizado",
        }


def main():
    servidor = StdioServerParameters(
        command=sys.executable,
        args=[
            "-X", "utf8",
            str(ROOT / "bibliounsa_mcp/servidor_mcp/bibliounsa_mcp.py"),
        ],
    )

    herramientas = HerramientasMCP(servidor)

    try:
        politica = PoliticaMCP(
            herramientas_permitidas={
                "buscar_libro",
                "prestamos_vencidos",
                "crear_reserva",
            },
            max_pasos=6,
        )

        traza = ROOT / "bibliounsa_mcp/trazas/e4_agente_lab10.jsonl"

        agente = Agente(
            nombre="agente_lab10_con_mcp",
            modelo=ModeloGuiado(),
            herramientas=herramientas,
            politica=politica,
            objetivo="Consultar BiblioUNSA y pedir permiso antes de reservar",
            traza_archivo=traza,
        )

        print("NÚCLEO:", Agente.__module__)
        print("HERRAMIENTAS MCP:", list(herramientas.catalogo()))

        resultado = agente.ejecutar()

        print("\n=== RESULTADOS DEL AGENTE ===")
        for evento in agente.eventos:
            if evento.get("tipo") == "accion":
                print(
                    evento.get("accion"),
                    "| ESTADO:", evento.get("estado"),
                    "| BLOQUEADA:", evento.get("bloqueada"),
                    "| OBSERVACIÓN:", evento.get("observacion", "")[:120],
                )

        print("FINAL:", resultado)
        print("TRAZA:", traza)

    finally:
        herramientas.cerrar()


if __name__ == "__main__":
    main()
