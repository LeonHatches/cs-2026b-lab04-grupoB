import pathlib,pytest
from bibliounsa.servicios import buscar_libro,prestamos_vencidos,crear_reserva,ErrorDominio

def test_buscar_libro_existente():assert buscar_libro('algoritmos')[0]['id']=='LIB-001'
def test_buscar_libro_invalido():
    with pytest.raises(ErrorDominio):buscar_libro(' ')
def test_buscar_libro_sin_resultados():assert buscar_libro('texto_inexistente')==[]
def test_vencido_excluye_devuelto():
    x=prestamos_vencidos('2026-11-23');assert x['cantidad']==1 and x['prestamos'][0]['id']=='P-001'
@pytest.mark.parametrize("fecha", ["23/11/2026", "20261123", "2026-02-30"])
def test_fecha_invalida(fecha):
    with pytest.raises(ErrorDominio, match="AAAA-MM-DD"):
        prestamos_vencidos(fecha)
def test_reserva_crea_sin_sobrescribir(tmp_path):
    x=crear_reserva('EST-001','LIB-001',True,tmp_path); y=crear_reserva('EST-001','LIB-001',True,tmp_path)
    assert x['id']!=y['id'] and len(list(tmp_path.glob('*.json')))==2
@pytest.mark.parametrize('args',[('EST-001','LIB-001',False),('A','LIB-001',True),('EST-001','LIB-003',True),('EST-001','LIB-999',True)])
def test_reserva_bloquea_entradas(args,tmp_path):
    with pytest.raises(ErrorDominio):crear_reserva(*args,tmp_path)
