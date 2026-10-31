"""Dos fitness functions estructurales ligeras para el paquete Lab 08.
Estas pruebas comprueban la estructura del paquete de simulación; el equipo
además debe aplicar los contratos import-linter al código integrado de BiblioUNSA.
"""
from pathlib import Path
import ast
ROOT = Path(__file__).resolve().parents[1] / 'fitness'

def imports_de(archivo):
    arbol = ast.parse((ROOT / archivo).read_text())
    modulos = []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Import):
            modulos.extend(alias.name for alias in nodo.names)
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            modulos.append(nodo.module)
    return modulos

def test_ff01_fitness_no_depende_de_interfaz_web():
    for archivo in ['rendimiento.py', 'disponibilidad.py', 'seguridad.py']:
        assert not any(x.startswith(('django', 'flask', 'fastapi')) for x in imports_de(archivo))

def test_ff02_simulaciones_no_importan_adaptadores_institucionales():
    for archivo in ['rendimiento.py', 'disponibilidad.py', 'seguridad.py']:
        assert not any('adaptador' in x.lower() for x in imports_de(archivo))
