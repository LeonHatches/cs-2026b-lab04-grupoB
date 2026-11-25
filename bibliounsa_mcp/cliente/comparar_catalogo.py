"""E6: comparación reproducible de catálogo completo y resumen compacto."""
import asyncio
import json
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parents[1]
RESUMENES = {
    "buscar_libro": "Busca libros por título o autor.",
    "prestamos_vencidos": "Lista préstamos vencidos según una fecha.",
    "crear_reserva": "Crea borrador ficticio; requiere autorización humana.",
}

def medir(obj):
    texto = json.dumps(obj, ensure_ascii=False, sort_keys=True)
    return {
        "caracteres": len(texto),
        "bytes": len(texto.encode("utf-8")),
        "tokens_aprox": round(len(texto) / 4),
    }

async def main():
    servidor = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "servidor_mcp/bibliounsa_mcp.py")],
    )

    async with Client(servidor) as cliente:
        tools = (await cliente.list_tools()).tools

    completo = [
        {
            "name": t.name,
            "description": t.description,
            "inputSchema": t.input_schema,
        }
        for t in tools
    ]

    compacto = [
        {
            "name": t.name,
            "summary": RESUMENES.get(t.name, t.description),
            "parameters": list(t.input_schema.get("properties", {})),
        }
        for t in tools
    ]

    antes = medir(completo)
    despues = medir(compacto)

    ahorro = round(
        100 * (antes["caracteres"] - despues["caracteres"])
        / antes["caracteres"], 2
    )

    resultado = {
        "metodologia": "Comparación de catálogo completo frente a índice resumido para contexto del agente",
        "original": antes,
        "compacto": despues,
        "reduccion_caracteres_pct": ahorro,
        "advertencia": "Optimización propuesta; no modifica el protocolo ni el catálogo servido por MCP",
    }

    destino = ROOT / "trazas/catalogo_comparacion.json"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(
        json.dumps(resultado, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    informe = ROOT / "docs/costo-contexto.md"
    informe.write_text(
        "# E6 — Costo de contexto\n\n"
        "Comparación reproducible de los metadatos obtenidos del servidor MCP.\n\n"
        f"- Catálogo original: {antes['tokens_aprox']} tokens aproximados.\n"
        f"- Índice compacto: {despues['tokens_aprox']} tokens aproximados.\n"
        f"- Reducción de caracteres: {ahorro}%.\n\n"
        "Los tokens se estiman como caracteres/4. El índice compacto es una propuesta "
        "para orientar la selección de herramientas del agente, no una modificación "
        "desplegada del servidor. Los esquemas MCP completos siguen disponibles.\n",
        encoding="utf-8",
    )

    print(json.dumps(resultado, ensure_ascii=False, indent=2))

asyncio.run(main())
