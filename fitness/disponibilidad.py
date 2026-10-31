"""E2: simulación por minutos de la indisponibilidad académica.

Cada solicitud llega en un minuto distinto. La cola se representa en memoria;
su durabilidad es un supuesto de arquitectura, no una propiedad comprobada aquí.
"""
from collections import deque


def simular(cola_persistente=True, cantidad=100, falla_desde=30, falla_hasta=50,
            *, capacidad_recuperacion=5, recuperar=True,
            matriculas_no_vigentes=()):
    """Pérdidas, validaciones y rechazos ante una caída de intervalo semiabierto.

El proveedor simulado responde fuera de la caída. El trabajador consume lotes
de pendientes por minuto, con capacidad adicional a la del tráfico nuevo.
Los identificadores de solicitud son los minutos de llegada: 0 a cantidad - 1.
Una validación de matrícula no equivale a una reserva confirmada.
"""
    valores = (cantidad, falla_desde, falla_hasta, capacidad_recuperacion)
    if any(type(valor) is not int for valor in valores):
        raise ValueError("Los parámetros de cantidad, tiempo y capacidad deben ser enteros")
    if cantidad < 0 or falla_desde < 0 or falla_hasta < falla_desde:
        raise ValueError("Cantidad e intervalo de caída inválidos")
    if capacidad_recuperacion <= 0:
        raise ValueError("La capacidad de recuperación debe ser positiva")
    no_vigentes = frozenset(matriculas_no_vigentes)
    if any(type(i) is not int or not 0 <= i < cantidad for i in no_vigentes):
        raise ValueError("Las matrículas no vigentes deben identificar solicitudes existentes")

    estados = {}
    validaciones = []
    pendientes = deque()
    afectadas = acumuladas = recuperadas = 0
    ultima_recuperacion = None

    def validar(solicitud, minuto_respuesta):
        validaciones.append((solicitud, minuto_respuesta))
        estados[solicitud] = 'RECHAZADA' if solicitud in no_vigentes else 'VALIDADA'

    minuto = 0
    while minuto < cantidad or (recuperar and pendientes):
        api_disponible = not falla_desde <= minuto < falla_hasta
        if minuto < cantidad:
            if api_disponible:
                validar(minuto, minuto)
            else:
                afectadas += 1
                if cola_persistente:
                    pendientes.append(minuto)
                    estados[minuto] = 'PENDIENTE_VALIDACION'
                    acumuladas += 1
                else:
                    estados[minuto] = 'NO_CONSERVADA'

        if api_disponible and recuperar and pendientes:
            # Cada lote termina al final del minuto, nunca durante la caída.
            for _ in range(min(capacidad_recuperacion, len(pendientes))):
                validar(pendientes.popleft(), minuto + 1)
                recuperadas += 1
            ultima_recuperacion = minuto + 1
        minuto += 1

    return {
        'solicitudes_total': cantidad,
        'duracion_caida_min': falla_hasta - falla_desde,
        'solicitudes_afectadas': afectadas,
        'exitos_finales': sum(estado == 'VALIDADA' for estado in estados.values()),
        'rechazadas': sum(estado == 'RECHAZADA' for estado in estados.values()),
        'pendientes_al_restaurar': acumuladas,
        'pendientes_recuperadas': recuperadas,
        'pendientes_finales': len(pendientes),
        'perdidas': sum(estado == 'NO_CONSERVADA' for estado in estados.values()),
        'recuperacion_min': (
            ultima_recuperacion - falla_hasta if ultima_recuperacion is not None else 0
        ),
        'minuto_ultima_recuperacion': ultima_recuperacion,
        'estados': estados,
        'validaciones': validaciones,
    }


def main():
    print('BiblioUNSA - E2: simulación de disponibilidad (no producción)')
    print('Carga: 100 solicitudes, una por minuto; caída: [30, 50) = 20 minutos.')
    print('Caso base: matrículas vigentes y almacenamiento siempre disponible.')
    print('Trabajador de pendientes: 5 solicitudes/min, además del tráfico nuevo.')
    antes = simular(cola_persistente=False)
    despues = simular(cola_persistente=True)
    print(f'\n{"Medida":30} | {"Sin cola":>8} | {"Con cola":>8}')
    print('-' * 56)
    for etiqueta, campo in [
        ('Solicitudes totales', 'solicitudes_total'),
        ('Caída académica (min)', 'duracion_caida_min'),
        ('Solicitudes afectadas', 'solicitudes_afectadas'),
        ('Matrículas validadas', 'exitos_finales'),
        ('Matrículas rechazadas', 'rechazadas'),
        ('Pendientes al restaurar API', 'pendientes_al_restaurar'),
        ('Pendientes resueltas', 'pendientes_recuperadas'),
        ('Pendientes al final', 'pendientes_finales'),
        ('Solicitudes no conservadas', 'perdidas'),
    ]:
        print(f'{etiqueta:30} | {antes[campo]:8} | {despues[campo]:8}')
    print(f'{"Vaciado de cola (min)":30} | {"N/A":>8} | {despues["recuperacion_min"]:8}')
    print(f'Reproceso: minutos {50} a {despues["minuto_ultima_recuperacion"]}.')
    control = simular(recuperar=False)
    print(f"Sin reprocesar: {control['pendientes_finales']} pendientes y "
          f"{control['exitos_finales']} matrículas validadas.")
    rechazos = simular(matriculas_no_vigentes=(30, 49))
    print(f"Con 2 matrículas no vigentes durante la caída: "
          f"{rechazos['exitos_finales']} validadas, {rechazos['rechazadas']} rechazadas.")
    print('Validar matrícula no confirma la reserva: falta comprobar el ejemplar y reservar atómicamente.')
    print('La simulación usa memoria; no demuestra persistencia en PostgreSQL.')


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    main()
