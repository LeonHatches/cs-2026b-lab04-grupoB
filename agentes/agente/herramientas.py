"""Herramientas mínimas, con sandbox y ejecución de pruebas sin shell arbitrario."""
import ast
import difflib
import os
from pathlib import Path
import re
import subprocess
import sys

class Herramientas:
    def __init__(self, raiz, original=None):
        self.raiz = Path(raiz).resolve()
        self.original = Path(original).resolve() if original else None

    def _ruta(self, ruta):
        if not isinstance(ruta, str):
            raise TypeError("Ruta no textual")
        p = (self.raiz / ruta).resolve()
        if p != self.raiz and self.raiz not in p.parents:
            raise PermissionError("Ruta fuera del sandbox")
        return p

    def catalogo(self):
        return {
            "listar_archivos": "listar_archivos(carpeta='.'): archivos de la copia",
            "leer_archivo": "leer_archivo(ruta): texto con números de línea",
            "buscar": "buscar(patron): texto coincidente en archivos Python",
            "ejecutar_pruebas": "ejecutar_pruebas(objetivo='tests'): pytest sin shell; solo tests/",
            "editar_archivo": "editar_archivo(ruta, antes, despues): reemplazo exacto (una aparición)",
            "ver_cambios": "ver_cambios(): diff respecto de la copia original",
            "mapa_repo": "mapa_repo(): módulos, clases y firmas Python (AST)",
            "anotar": "anotar(texto): añade una nota breve a notas.md en sandbox",
            "leer_notas": "leer_notas(): lee notas.md en sandbox",
        }

    def listar_archivos(self, carpeta='.'):
        base=self._ruta(carpeta)
        return '\n'.join(sorted(str(p.relative_to(self.raiz)) for p in base.rglob('*')
                    if p.is_file() and p.suffix in ('.py','.md') and '__pycache__' not in p.parts)[:120])

    def leer_archivo(self, ruta):
        p=self._ruta(ruta)
        if p.suffix not in ('.py','.md'): raise PermissionError("Tipo no permitido")
        return '\n'.join(f'{i:3d}| {x}' for i,x in enumerate(p.read_text(encoding='utf-8').splitlines(),1))[:16000]

    def buscar(self, patron):
        if len(patron)>100: raise ValueError("Patrón excesivo")
        rx=re.compile(patron)
        found=[]
        for p in sorted(self.raiz.rglob('*.py')):
            if '__pycache__' in p.parts:continue
            for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
                if rx.search(line): found.append(f'{p.relative_to(self.raiz)}:{i}: {line.strip()}')
        return '\n'.join(found[:40]) or '(sin resultados)'

    def ejecutar_pruebas(self, objetivo='tests'):
        if objetivo not in ('tests','tests/test_issue_01.py','tests/test_issue_02.py','tests/test_issue_03.py'):
            raise PermissionError("Objetivo de pytest no autorizado")
        proc=subprocess.run([sys.executable,'-m','pytest','-q',objetivo,'-p','no:cacheprovider'], cwd=self.raiz,
                capture_output=True,text=True,timeout=45,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        lines=(proc.stdout+'\n'+proc.stderr).strip().splitlines()
        failures=[line for line in lines if line.startswith(('FAILED','E   '))][:5]
        return f'returncode={proc.returncode}\n'+'\n'.join(failures+lines[-2:])

    def editar_archivo(self,ruta,antes,despues):
        p=self._ruta(ruta)
        if not ruta.startswith('src/') or p.suffix!='.py': raise PermissionError("Solo se edita src/*.py")
        if not isinstance(antes,str) or not antes or not isinstance(despues,str): raise ValueError("Fragmento inválido")
        src=p.read_text(encoding='utf-8')
        if src.count(antes)!=1: return f'ERROR: fragmento encontrado {src.count(antes)} veces; se exige 1'
        p.write_text(src.replace(antes,despues),encoding='utf-8')
        return f'OK: {ruta} modificado'

    def ver_cambios(self):
        if self.original is None:return '(original no definido)'
        diff=[]
        for p in sorted(self.raiz.rglob('*.py')):
            if '__pycache__' in p.parts:continue
            rel=p.relative_to(self.raiz);q=self.original/rel
            orig=q.read_text(encoding='utf-8').splitlines() if q.exists() else []
            ruta = rel.as_posix()
            diff.extend(difflib.unified_diff(
                orig, p.read_text(encoding='utf-8').splitlines(),
                fromfile=f'a/{ruta}', tofile=f'b/{ruta}', lineterm='',
            ))
        return '\n'.join(diff)[:16000] or '(sin cambios)'

    def mapa_repo(self):
        out=[]
        for p in sorted(self.raiz.rglob('*.py')):
            if '__pycache__' in p.parts:continue
            tree=ast.parse(p.read_text(encoding='utf-8'))
            signatures=[]
            for node in tree.body:
                if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef)):
                    signatures.append(f'{node.name}({", ".join(a.arg for a in node.args.args)})')
                elif isinstance(node,ast.ClassDef):signatures.append('class '+node.name)
            out.append(f'{p.relative_to(self.raiz)}: {", ".join(signatures) or "(sin funciones)"}')
        return '\n'.join(out[:60])[:10000]

    def anotar(self,texto):
        if not isinstance(texto,str) or not 1<=len(texto.strip())<=300: raise ValueError("Nota entre 1 y 300 caracteres")
        p=self._ruta('notas.md')
        with p.open('a',encoding='utf-8') as f:f.write('- '+texto.replace('\n',' ').strip()+'\n')
        return 'OK: nota registrada'

    def leer_notas(self):
        p=self._ruta('notas.md')
        return p.read_text(encoding='utf-8')[:4000] if p.exists() else '(sin notas)'
