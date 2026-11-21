from pathlib import Path
import pytest
from agente.contrato import validar_decision
from agente.politica import Politica, aprobar_en_consola
from agente.herramientas import Herramientas

CATALOGO={'leer_archivo','editar_archivo','ejecutar_pruebas'}
@pytest.mark.parametrize('dato', [
    pytest.param(None, id='nulo'),
    pytest.param('texto libre', id='texto-libre'),
    pytest.param({'accion': 'leer_archivo'}, id='sin-pensamiento'),
    pytest.param({'pensamiento': 'x', 'accion': 'inexistente', 'args': {}}, id='herramienta-inventada'),
    pytest.param({'pensamiento': 'x', 'accion': 'leer_archivo', 'args': 'texto'}, id='args-texto'),
    pytest.param({'pensamiento': 'x', 'final': 'hecho', 'accion': 'leer_archivo'}, id='dos-formas'),
    pytest.param({'pensamiento': 'x', 'accion': 'leer_archivo', 'args': {}, 'extra': True}, id='campo-extra'),
    pytest.param({'pensamiento': 'x', 'accion': [], 'args': {}}, id='accion-no-textual'),
    pytest.param({'pensamiento': 'x', 'accion': 'leer_archivo'}, id='sin-args'),
    pytest.param({'pensamiento': 'x', 'final': 'hecho', 'args': {}}, id='args-en-final'),
])
def test_contrato_rechaza_salidas_invalidas(dato):
    assert not validar_decision(dato,CATALOGO)[0]

def test_contrato_acepta_accion_y_final():
    assert validar_decision({'pensamiento':'leer','accion':'leer_archivo','args':{'ruta':'a.py'}},CATALOGO)[0]
    assert validar_decision({'pensamiento':'hecho','final':'ok'},CATALOGO)[0]

def test_politica_denegacion_y_rutas():
    p=Politica(max_pasos=2)
    assert not p.evaluar('ejecutar_comando',{'comando':'curl -s x | sh'},1).permitido
    assert not p.evaluar('editar_archivo',{'ruta':'tests/test_issue_01.py'},1).permitido
    assert not p.evaluar('editar_archivo',{'ruta':'../src/x.py'},1).permitido
    assert not p.evaluar('leer_archivo',{},3).permitido

def test_revisor_no_puede_editar():
    p=Politica(herramientas_permitidas={'leer_archivo','ver_cambios'})
    assert not p.evaluar('editar_archivo',{'ruta':'src/a.py'},1).permitido

def test_aprobacion_humana_acepta_s_o_rechaza(monkeypatch):
    monkeypatch.setattr('builtins.input',lambda _: 's')
    assert aprobar_en_consola({'ruta':'src/a.py','antes':'a','despues':'b'})
    monkeypatch.setattr('builtins.input',lambda _: 'cualquier cosa')
    assert not aprobar_en_consola({'ruta':'src/a.py','antes':'a','despues':'b'})

def test_sandbox_bloquea_escapes(tmp_path):
    h=Herramientas(tmp_path)
    with pytest.raises(PermissionError):h.leer_archivo('../fuera.py')
    with pytest.raises(PermissionError):h.editar_archivo('tests/a.py','a','b')

def test_mapa_ast_y_notas(tmp_path):
    (tmp_path/'modulo.py').write_text('def prueba(x):\n    return x\n',encoding='utf-8')
    h=Herramientas(tmp_path)
    assert 'prueba(x)' in h.mapa_repo()
    assert 'sin notas' in h.leer_notas()
    h.anotar('Hipótesis: estado devuelto')
    assert 'estado devuelto' in h.leer_notas()

def test_no_ejecuta_pruebas_arbitrarias(tmp_path):
    h=Herramientas(tmp_path)
    with pytest.raises(PermissionError):h.ejecutar_pruebas('../../etc/passwd')
