from datetime import date
from bibliounsa_lab10.dominio import dias_multa

def test_issue01_no_multa_domingo():
    # Viernes 13 -> lunes 16: sábado y lunes, no domingo.
    assert dias_multa(date(2026, 11, 13), date(2026, 11, 16)) == 2

def test_issue01_sin_retraso():
    assert dias_multa(date(2026, 11, 16), date(2026, 11, 16)) == 0
