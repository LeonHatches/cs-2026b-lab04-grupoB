"""Proveedor de Promptfoo que reproduce archivos UTF-8 sin editar su contenido."""
from pathlib import Path
import re


RAIZ = Path(__file__).resolve().parent


def call_api(prompt, options, context):
    config = options.get('config') or {}
    tarea = config.get('tarea', 'criterios')
    caso = (context.get('vars') or {}).get('id')
    version = re.match(r'\A# VERSION: (v[123])(?:\r?\n|\Z)', prompt)
    if tarea not in {'criterios', 'sql'} or not version:
        return {'error': 'La tarea o la cabecera de versión no son válidas'}
    if not isinstance(caso, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', caso):
        return {'error': 'Identificador de caso inválido'}

    archivo = RAIZ / tarea / 'grabaciones' / version[1] / f'{caso}.txt'
    try:
        salida = archivo.read_bytes().decode('utf-8')
    except (OSError, UnicodeDecodeError):
        return {'error': f'Grabación ausente o no legible en UTF-8: {version[1]}/{caso}.txt'}
    if not salida.strip():
        return {'error': f'Grabación vacía: {version[1]}/{caso}.txt'}
    return {'output': salida}
