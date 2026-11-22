"""Ejecuta ISSUE-01 sobre una copia temporal del código de práctica."""

import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory

from agente.herramientas import Herramientas
from agente.modelos import ModeloGrabado, ModeloInteractivo
from agente.nucleo import Agente
from agente.politica import Politica, aprobar_en_consola
from agente.traza import generar_diagrama


ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / "trabajo"
OBJETIVO = "ISSUE-01: corregir el conteo de domingos en el cálculo de días de multa."


def contexto_interactivo(herramientas):
    catalogo = "\n".join(f"- {firma}" for firma in herramientas.catalogo().values())
    return f"""{OBJETIVO}
Trabaja sobre una copia de práctica de BiblioUNSA. Lee issues/ISSUE-01.md, reproduce
el fallo con tests/test_issue_01.py y revisa el código antes de proponer un cambio.
Edita únicamente el código de ISSUE-01 en src/ y comprueba la regresión antes de cerrar.
Las herramientas requieren el JSON de abajo y las ediciones requieren aprobación humana.

Herramientas disponibles:
{catalogo}

Devuelve una sola decisión por turno, en una línea de JSON sin Markdown.
Para actuar: {{"pensamiento":"motivo breve", "accion":"nombre", "args":{{}}}}
Para terminar: {{"pensamiento":"motivo breve", "final":"resultado verificado"}}
Al recibir una observación, elige la siguiente acción usando su resultado.
"""


def ejecutar_issue01(interactivo=False):
    if interactivo:
        marca = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        nombre = f"issue01_interactivo_{marca}"
        decisiones = ROOT / "trayectorias" / f"{nombre}.json"
        modelo = ModeloInteractivo(decisiones)
        politica = Politica(aprobar_edicion=aprobar_en_consola)
        print(f"Decisiones de la sesión: {decisiones}")
    else:
        nombre = "issue01_demo"
        modelo = ModeloGrabado(ROOT / "trayectorias" / f"{nombre}.json")
        politica = Politica()
        print("Demostración determinista de ISSUE-01")

    traza = ROOT / "trazas" / f"{nombre}.jsonl"
    with TemporaryDirectory(prefix="bibliounsa-lab10-") as temporal:
        trabajo = Path(temporal) / "copia"
        shutil.copytree(ORIGINAL, trabajo, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        herramientas = Herramientas(trabajo, ORIGINAL)
        objetivo = contexto_interactivo(herramientas) if interactivo else OBJETIVO
        agente = Agente("ejecutor", modelo, herramientas, politica, objetivo, traza)
        try:
            resultado = agente.ejecutar()
        finally:
            diff = traza.with_suffix(".diff")
            cambios = herramientas.ver_cambios()
            diff.write_text(cambios + "\n", encoding="utf-8")
            diagrama = generar_diagrama(traza)
            print(f"Traza: {traza}\nDiff: {diff}\nDiagrama: {diagrama}")

    for evento in agente.eventos:
        if evento.get("accion") == "ejecutar_pruebas" and evento["estado"] == "OBSERVANDO":
            print(f"Paso {evento['paso']} · {evento['args'].get('objetivo', 'tests')}")
            print(evento["observacion"])
    acciones = [evento for evento in agente.eventos if evento["tipo"] == "accion"]
    invalidas = sum(evento["estado"] == "CONTRATO_INVALIDO" for evento in acciones)
    print(f"Acciones registradas: {len(acciones)} | Rechazos de contrato: {invalidas}")
    print(resultado)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--modo", choices=["demo", "interactivo"], default="demo")
    args = parser.parse_args()
    try:
        ejecutar_issue01(interactivo=args.modo == "interactivo")
    except (EOFError, KeyboardInterrupt):
        parser.exit(130, "Sesión interrumpida. Se conservó la evidencia registrada.\n")


if __name__ == "__main__":
    main()
