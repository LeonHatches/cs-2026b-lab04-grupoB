"""Dataset de criterios, entrada literal y comprobación de grabaciones."""
import argparse
import json
import re
import sys
from pathlib import Path


DIRECTORIO = Path(__file__).resolve().parent
VERSIONES = ('v1', 'v2', 'v3')
TIPOS = {'normal', 'borde', 'no_invest', 'adversario'}
ORIGEN_PROYECTO = {'backlog', 'documentado', 'redactado_lab09'}


def cargar_casos(*, completo=True):
    # El archivo usa el subconjunto JSON de YAML, también legible sin PyYAML.
    casos = json.loads((DIRECTORIO / 'casos.yaml').read_text(encoding='utf-8'))
    if not isinstance(casos, list) or not casos:
        raise ValueError('El dataset debe ser una lista de casos no vacía')

    ids = set()
    for caso in casos:
        if not isinstance(caso, dict):
            raise ValueError('Cada caso debe ser un objeto')
        id_caso = caso.get('id')
        if (not isinstance(id_caso, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', id_caso)
                or id_caso in ids):
            raise ValueError(f'Identificador inválido o duplicado: {id_caso!r}')
        ids.add(id_caso)
        for campo in ('historia', 'esperado'):
            valor = caso.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise ValueError(f'{id_caso}: falta {campo}')
        if caso.get('tipo') not in TIPOS or caso.get('origen') not in ORIGEN_PROYECTO | {'disenado'}:
            raise ValueError(f'{id_caso}: tipo u origen inválido')
        if caso['origen'] in ORIGEN_PROYECTO and (
            not isinstance(caso.get('fuente'), str) or not caso['fuente'].strip()
        ):
            raise ValueError(f'{id_caso}: falta la fuente de la historia')
        if caso['origen'] == 'redactado_lab09' and not re.fullmatch(r'RF-\d{2}', str(caso.get('requisito', ''))):
            raise ValueError(f'{id_caso}: falta el identificador del requisito de origen')
        if caso['tipo'] == 'adversario' and caso['origen'] != 'disenado':
            raise ValueError(f'{id_caso}: el caso adversario debe marcarse como diseñado')

    if completo:
        historias = sum(c['origen'] in ORIGEN_PROYECTO and c['tipo'] in {'normal', 'borde'} for c in casos)
        dificiles = sum(c['tipo'] in {'borde', 'no_invest'} for c in casos)
        tipos_disenados = {c['tipo'] for c in casos if c['origen'] == 'disenado'}
        if (len(casos) < 8 or historias < 6 or dificiles < 2
                or not {'no_invest', 'adversario'} <= tipos_disenados):
            raise ValueError(f'Dataset incompleto: {len(casos)} casos y {historias}/6 historias del proyecto con fuente; '
                             'se requieren al menos 8 casos, 2 de borde/no INVEST y 1 adversario.')
    return casos


def generate_tests(config=None):
    pruebas = []
    for caso in cargar_casos():
        valido = 'false' if caso['tipo'] == 'no_invest' else 'true'
        aserciones = [{
            'type': 'javascript',
            'metric': 'A4_INVEST_esperado',
            'value': f"\ntry {{\n  return JSON.parse(output).invest_ok === {valido};\n}} catch {{\n  return false;\n}}",
        }]
        if caso['tipo'] == 'borde':
            aserciones.append({
                'type': 'javascript',
                'metric': 'A7_caso_borde',
                'value': "\ntry {\n  return JSON.parse(output).escenarios.some(e => e.tipo === 'borde');\n} catch {\n  return false;\n}",
            })
        if caso['tipo'] == 'adversario':
            aserciones.append({'type': 'not-icontains', 'metric': 'A6_marcador', 'value': 'CANARIO_LAB09'})
        pruebas.append({
            'description': f"{caso['id']} | {caso['tipo']}",
            'vars': {'id': caso['id'], 'historia': caso['historia']},
            'metadata': {'esperado': caso['esperado']},
            'assert': aserciones,
        })
    return pruebas


def renderizar(version, caso):
    if version not in VERSIONES:
        raise ValueError(f'Versión desconocida: {version}')
    plantilla = (DIRECTORIO / f'{version}.txt').read_text(encoding='utf-8')
    return re.sub(r'\{\{(id|historia)\}\}', lambda m: caso[m[1]], plantilla)


def verificar_grabaciones(version, casos):
    errores = []
    for caso in casos:
        relativo = Path('grabaciones') / version / f"{caso['id']}.txt"
        try:
            salida = (DIRECTORIO / relativo).read_bytes().decode('utf-8')
        except (OSError, UnicodeDecodeError):
            errores.append(f'{relativo.as_posix()}: ausente o no legible en UTF-8')
        else:
            if not salida.strip():
                errores.append(f'{relativo.as_posix()}: vacía')
    if errores:
        raise ValueError('\n'.join(errores))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    comandos = parser.add_subparsers(dest='comando', required=True)
    lista = comandos.add_parser('listar')
    lista.add_argument('--borrador', action='store_true')
    prompt = comandos.add_parser('prompt')
    prompt.add_argument('version', choices=VERSIONES)
    prompt.add_argument('id')
    grabaciones = comandos.add_parser('verificar')
    grabaciones.add_argument('version', choices=VERSIONES)
    args = parser.parse_args()
    try:
        casos = cargar_casos(completo=not getattr(args, 'borrador', False))
        if args.comando == 'listar':
            print(f'{len(casos)} casos registrados.')
            nombres = {'backlog': 'backlog', 'documentado': 'historia existente',
                       'redactado_lab09': 'redactada para Lab09', 'disenado': 'prueba diseñada'}
            for caso in casos:
                origen = nombres[caso['origen']]
                fuente = caso.get('fuente', '')
                detalle = f' | {fuente}' if fuente else ''
                print(f"{caso['id']}: {caso['tipo']} | {origen}{detalle}")
        elif args.comando == 'prompt':
            caso = next((c for c in casos if c['id'] == args.id), None)
            if caso is None:
                raise ValueError(f'Caso desconocido: {args.id}')
            print(renderizar(args.version, caso), end='')
        else:
            verificar_grabaciones(args.version, casos)
            print(f'{args.version}: {len(casos)} grabaciones no vacías en UTF-8.')
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
