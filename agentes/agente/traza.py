"""Genera el recorrido Mermaid de una traza JSONL de ISSUE-01."""

import argparse
from html import escape
import json
from pathlib import Path


def generar_diagrama(origen):
    eventos = [
        json.loads(linea)
        for linea in origen.read_text(encoding="utf-8").splitlines()
        if linea.strip()
    ]
    lineas = ["flowchart TD", '    inicio["ISSUE-01"]']
    anterior = "inicio"
    for indice, evento in enumerate(eventos, 1):
        if evento["tipo"] not in {"accion", "final"}:
            continue
        nodo = f"e{indice}"
        estado = evento["estado"]
        accion = evento.get("accion")
        etiqueta = f"Paso {evento['paso']} · {estado}"
        if accion and accion != "(ninguna)":
            etiqueta += f" · {accion}"
        lineas.append(f'    {anterior} --> {nodo}["{escape(etiqueta)}"]')
        anterior = nodo
    destino = origen.with_suffix(".mmd")
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return destino


if __name__ == "__main__":
    trazas = Path(__file__).resolve().parents[1] / "trazas"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("traza", type=Path, nargs="?", default=trazas / "issue01_demo.jsonl")
    print(generar_diagrama(parser.parse_args().traza))
