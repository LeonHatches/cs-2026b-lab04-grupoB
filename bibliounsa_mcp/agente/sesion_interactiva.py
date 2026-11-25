"""Adaptación manual-interactiva del patrón decisión/acción/observación del Lab 10 a MCP.
El humano que controla el host elige cada llamada; no se simula un LLM autónomo.
La traza solo refleja decisiones realizadas por una persona ante la consola.
"""
import asyncio,sys,json,time
from pathlib import Path
from mcp import Client,StdioServerParameters
RAIZ=Path(__file__).resolve().parents[1]
SERVER=StdioServerParameters(command=sys.executable,args=[str(RAIZ/'cliente/espia.py'),str(RAIZ/'servidor_mcp/bibliounsa_mcp.py')])
async def main():
    registros=[]
    async with Client(SERVER) as client:
        for name,args in [('buscar_libro',{'texto':'algoritmos'}),('prestamos_vencidos',{'hoy':'2026-11-23'})]:
            r=await client.call_tool(name,args)
            registros.append({'herramienta':name,'args':args,'is_error':r.is_error,'observacion':r.structured_content or [getattr(x,'text','') for x in r.content]})
            print(name,registros[-1]['observacion'])
        # Primera tentativa intencionalmente inválida: demuestra error ToolError de dominio
        name='crear_reserva'; args={'usuario':'EST-001','libro_id':'LIB-001','matricula_vigente':False}
        r=await client.call_tool(name,args)
        registros.append({'herramienta':name,'args':args,'is_error':r.is_error})
        print('Observación de validación:',r.is_error,[getattr(x,'text','') for x in r.content])
        permiso=input('¿Autoriza crear un borrador de reserva ficticio? [s/n]: ').strip().lower()
        if permiso=='s':
            args['matricula_vigente']=True
            r=await client.call_tool(name,args)
            registros.append({'herramienta':name,'args':args,'is_error':r.is_error,'observacion':r.structured_content or [getattr(x,'text','') for x in r.content]})
            print('Creación:',registros[-1]['observacion'])
        else:
            registros.append({'herramienta':name,'bloqueada':True,'motivo':'Denegación humana'})
            print('Escritura BLOQUEADA por la persona')
    dest=RAIZ/'trazas/sesion_interactiva.jsonl';dest.parent.mkdir(exist_ok=True)
    dest.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in registros),encoding='utf8')
    print('Traza creada:',dest)
if __name__=='__main__':asyncio.run(main())
