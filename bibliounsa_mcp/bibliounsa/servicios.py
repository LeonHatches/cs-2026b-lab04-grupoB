"""Lógica del caso BiblioUNSA; el adaptador MCP no duplica reglas del dominio."""
from __future__ import annotations
from datetime import date
from pathlib import Path
import json,re
from bibliounsa.datos import LIBROS,PRESTAMOS

class ErrorDominio(ValueError):
    pass

def buscar_libro(texto: str) -> list[dict]:
    if not isinstance(texto,str) or not 2 <= len(texto.strip()) <= 80:
        raise ErrorDominio('La búsqueda debe tener entre 2 y 80 caracteres')
    q=texto.strip().casefold()
    return [dict(l) for l in LIBROS if q in l['titulo'].casefold() or q in l['autor'].casefold()][:20]

def prestamos_vencidos(hoy: str) -> dict:
    if not isinstance(hoy, str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', hoy):
        raise ErrorDominio('Fecha inválida: use AAAA-MM-DD')
    try:
        fecha = date.fromisoformat(hoy)
    except ValueError:
        raise ErrorDominio('Fecha inválida: use AAAA-MM-DD') from None
    v=[{"id":x['id'],"libro":x['libro'],"vencimiento":x['vencimiento']} for x in PRESTAMOS
       if x['estado']=='PRESTADO' and date.fromisoformat(x['vencimiento'])<fecha]
    return {'fecha':hoy,'cantidad':len(v),'prestamos':v}

def crear_reserva(usuario: str, libro_id: str, matricula_vigente: bool, carpeta: Path) -> dict:
    """Única operación persistente: crear un registro nuevo; nunca sobrescribir ni borrar."""
    if not isinstance(usuario,str) or not re.fullmatch(r'EST-[0-9]{3}',usuario):
        raise ErrorDominio('usuario inválido: formato EST-001')
    if not isinstance(libro_id,str) or not re.fullmatch(r'LIB-[0-9]{3}',libro_id):
        raise ErrorDominio('libro_id inválido: formato LIB-001')
    if type(matricula_vigente) is not bool:
        raise ErrorDominio('matricula_vigente debe ser booleana')
    if not matricula_vigente: raise ErrorDominio('Matrícula no vigente: no se permite reservar')
    libro=next((x for x in LIBROS if x['id']==libro_id),None)
    if libro is None: raise ErrorDominio('Libro no encontrado')
    if libro['ejemplares']<=0: raise ErrorDominio('Libro sin ejemplares disponibles')
    carpeta=Path(carpeta)
    carpeta.mkdir(parents=True,exist_ok=True)
    for n in range(1,10000):
        id_reserva=f'RES-{n:04d}'
        archivo=carpeta/f'{id_reserva}.json'
        try:
            with archivo.open('x',encoding='utf-8') as fd:
                registro={'id':id_reserva,'usuario':usuario,'libro_id':libro_id,'estado':'BORRADOR'}
                json.dump(registro,fd,ensure_ascii=False,indent=2)
                return registro
        except FileExistsError:
            continue
    raise ErrorDominio('Se alcanzó el límite de reservas de prueba')
