"""BiblioUNSA Lab 10: laboratorio controlado de fallos sembrados.
No es el código desplegado de BiblioUNSA. No maneja datos personales.
"""
from datetime import date, timedelta


def dias_multa(vencimiento: date, devolucion: date) -> int:
    """Días sujetos a multa: excluye domingos; extremos (vencimiento, devolución]."""
    if devolucion <= vencimiento:
        return 0
    return (devolucion - vencimiento).days


def reservar_ejemplar(matricula_vigente: bool, disponible: bool) -> str:
    """Decisión simulada para una reserva; ninguna API real es invocada."""
    if not disponible:
        return "NO_DISPONIBLE"
    return "RESERVADA"


def prestamo_vencido(estado: str, vencimiento: date, hoy: date) -> bool:
    """Estado vencido con prioridad de la devolución sobre la fecha límite."""
    return vencimiento < hoy
