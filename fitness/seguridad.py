"""Simulación de autorización para BiblioUNSA (QA-05)."""

ROLES_PERMITIDOS = {"BIBLIOTECARIO", "ADMINISTRADOR"}


def autorizacion_insegura(rol_cliente):
    """Modelo inicial: confía en el rol declarado por el cliente."""
    return rol_cliente in ROLES_PERMITIDOS


def autorizacion_segura(rol_autenticado):
    """Modelo mejorado: consulta el rol verificado por el servidor."""
    return rol_autenticado in ROLES_PERMITIDOS


def simular_intentos(total=100):
    indebidos_antes = 0
    indebidos_despues = 0

    for _ in range(total):
        rol_real = "ESTUDIANTE"
        rol_enviado = "ADMINISTRADOR"

        if autorizacion_insegura(rol_enviado):
            indebidos_antes += 1

        if autorizacion_segura(rol_real):
            indebidos_despues += 1

    return {
        "intentos": total,
        "accesos_indebidos_antes": indebidos_antes,
        "accesos_indebidos_despues": indebidos_despues,
    }


if __name__ == "__main__":
    resultado = simular_intentos()
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
