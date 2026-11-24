"""Verifica el catálogo y una consulta de BiblioUNSA a través de stdio."""
import asyncio
import json
from pathlib import Path
import sys

from mcp import Client, StdioServerParameters


RAIZ = Path(__file__).resolve().parents[1]
SERVIDOR = StdioServerParameters(
    command=sys.executable,
    args=["-X", "utf8", str(RAIZ / "servidor_mcp" / "bibliounsa_mcp.py")],
)


async def main() -> None:
    async with Client(SERVIDOR) as cliente:
        herramientas = (await cliente.list_tools()).tools
        recursos = (await cliente.list_resources()).resources
        plantillas = (await cliente.list_resource_templates()).resource_templates
        prompts = (await cliente.list_prompts()).prompts
        print("TOOLS", [t.name for t in herramientas])
        print("RECURSOS", [str(r.uri) for r in recursos])
        print("PLANTILLAS", [str(r.uri_template) for r in plantillas])
        print("PROMPTS", [p.name for p in prompts])

        consulta = await cliente.call_tool("prestamos_vencidos", {"hoy": "2026-11-23"})
        print("CONSULTA", json.dumps(consulta.structured_content, ensure_ascii=False))
        error = await cliente.call_tool("prestamos_vencidos", {"hoy": "ayer"})
        print("ERROR", json.dumps({
            "isError": error.is_error,
            "mensajes": [bloque.text for bloque in error.content if bloque.type == "text"],
        }, ensure_ascii=False))

        if consulta.is_error or consulta.structured_content is None or not error.is_error:
            raise SystemExit("La verificación del servidor MCP falló")


if __name__ == "__main__":
    asyncio.run(main())
