from bibliounsa_lab10.dominio import reservar_ejemplar

def test_issue02_matricula_vencida_rechazada():
    assert reservar_ejemplar(matricula_vigente=False, disponible=True) == "MATRICULA_NO_VIGENTE"

def test_issue02_matricula_vigente_puede_reservar():
    assert reservar_ejemplar(matricula_vigente=True, disponible=True) == "RESERVADA"
