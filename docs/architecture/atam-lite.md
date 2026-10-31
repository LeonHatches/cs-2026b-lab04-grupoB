# E3 — ATAM-lite de BiblioUNSA

## Alcance
Análisis interno de la iteración 1 de ADD y los escenarios del árbol de utilidad.
La evaluación cruzada oficial requiere el repositorio asignado por el docente.

## Evidencia revisada
- docs/architecture/utilidad/escenarios.md
- docs/architecture/add/iteracion-1.md
- fitness/disponibilidad.py

## Hallazgos internos

| Tipo | Hallazgo | Evidencia o acción |
|---|---|---|
| Sensibilidad | QA-04 depende de la capacidad de reproceso de pendientes | Con 5 pendientes/min se recuperan 20 en 4 min; con 3 pendientes/min se requieren 7 min |
| Trade-off | La cola conserva solicitudes, pero difiere su validación | Simulación: pérdidas de 20 a 0; la solicitud pendiente no equivale a reserva confirmada |
| Riesgo R1 | Una caída de la base de datos podría impedir almacenar solicitudes | Probabilidad estimada 2/5; impacto 5/5; requiere prueba real de persistencia |
| Riesgo R2 | Reintentos sin idempotencia podrían producir operaciones duplicadas | Probabilidad estimada 3/5; impacto 4/5; se requieren claves idempotentes y pruebas |
| No riesgo condicionado | Mantener el monolito modular no impide modelar el reproceso | La simulación cumple QA-03 y QA-04 bajo sus supuestos, pero no demuestra capacidad productiva |

Las probabilidades e impactos son estimaciones iniciales del equipo y deben revisarse.

## Evaluación cruzada recibida

Pendiente: registrar URL del issue recibido, hallazgos y respuestas con evidencia.

## Evaluación de otro grupo

Pendiente: registrar el repositorio asignado por el docente y el issue publicado.
