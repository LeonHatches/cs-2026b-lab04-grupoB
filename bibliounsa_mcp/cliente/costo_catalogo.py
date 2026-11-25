"""Costo estimado del catálogo; mide texto UTF-8 y una aproximación tokens=caracteres/4."""
import json,sys
from pathlib import Path
from mcp import Client,StdioServerParameters
import asyncio
ROOT=Path(__file__).resolve().parents[1]
async def main():
    async with Client(StdioServerParameters(command=sys.executable,args=[str(ROOT/'servidor_mcp/bibliounsa_mcp.py')])) as c:
        tools=(await c.list_tools()).tools
        rows=[]
        for t in tools:
            payload={'name':t.name,'description':t.description,'inputSchema':t.input_schema}
            txt=json.dumps(payload,ensure_ascii=False,sort_keys=True)
            rows.append({'herramienta':t.name,'caracteres':len(txt),'tokens_aprox':round(len(txt)/4),'bytes':len(txt.encode())})
        dest=ROOT/'trazas/catalogo_costo.json';dest.parent.mkdir(exist_ok=True)
        dest.write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
        print(json.dumps(rows,indent=2,ensure_ascii=False))
if __name__=='__main__':asyncio.run(main())
