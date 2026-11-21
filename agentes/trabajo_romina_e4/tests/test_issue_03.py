from datetime import date
from bibliounsa_lab10.dominio import prestamo_vencido

def test_issue03_devuelto_no_sigue_vencido():
    assert not prestamo_vencido("DEVUELTO", date(2026, 11, 1), date(2026, 11, 16))

def test_issue03_prestado_efectivamente_vencido():
    assert prestamo_vencido("PRESTADO", date(2026, 11, 1), date(2026, 11, 16))
