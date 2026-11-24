"""Contratos del servidor con el SDK oficial MCP 2."""
import asyncio

import pytest
from mcp import Client
from mcp.shared.exceptions import MCPError
from servidor_mcp import bibliounsa_mcp as srv

def run(f):
    async def _go():
        async with Client(srv.mcp) as c:return await f(c)
    return asyncio.run(_go())

def test_catalogo_estable():
    tools=run(lambda c:c.list_tools()).tools
    assert [x.name for x in tools]==['buscar_libro','prestamos_vencidos','crear_reserva']

def test_unica_escritura():
    ts=run(lambda c:c.list_tools()).tools
    assert [t.name for t in ts if not(t.annotations and t.annotations.read_only_hint)]==['crear_reserva']

def test_descripciones_claras():
    ts=run(lambda c:c.list_tools()).tools
    assert all(t.description and len(t.description)>30 for t in ts)

def test_salida_estructurada():
    r=run(lambda c:c.call_tool('prestamos_vencidos',{'hoy':'2026-11-23'}))
    assert not r.is_error
    assert r.structured_content == {
        'fecha': '2026-11-23',
        'cantidad': 1,
        'prestamos': [{'id': 'P-001', 'libro': 'LIB-001', 'vencimiento': '2026-11-10'}],
    }

def test_error_fecha():
    r=run(lambda c:c.call_tool('prestamos_vencidos',{'hoy':'ayer'}))
    assert r.is_error
    assert any('AAAA-MM-DD' in b.text for b in r.content if b.type == 'text')

def test_error_matricula():
    r=run(lambda c:c.call_tool('crear_reserva',{'usuario':'EST-001','libro_id':'LIB-001','matricula_vigente':False}))
    assert r.is_error

def test_recurso_reglamento():
    r=run(lambda c:c.read_resource('bibliounsa://reglamento'))
    assert 'matrícula' in r.contents[0].text

def test_recurso_adr_seguro():
    async def comprobar(cliente):
        templates = (await cliente.list_resource_templates()).resource_templates
        assert [t.uri_template for t in templates] == ['bibliounsa://adr/{numero}']
        recurso = await cliente.read_resource('bibliounsa://adr/001')
        assert 'monolito' in recurso.contents[0].text.lower()
        with pytest.raises(MCPError, match='tres dígitos'):
            await cliente.read_resource('bibliounsa://adr/abc')

    run(comprobar)

def test_prompt_aviso():
    r=run(lambda c:c.get_prompt('aviso_vencimiento',{'prestamo_id':'P-001'}))
    assert 'P-001' in r.messages[0].content.text
