# E7 — Auditoría razonada C1–C5
| Regla | Hallazgo | Verificación / corrección |
|---|---|---|
| C1 | `validarVigente()`, `buscar()`, `verificarDisponible()`, `reservarAtomicamente()`, `enviarConfirmacion()` aparecen en secuencia | Existen en `clases.puml`. Los mensajes de UI representan interacción y el controlador expone `crearReserva()` |
| C2 | El diseño incluye estados de préstamo, mientras E1 se concentra en Reserva | Se incorpora `src/reservas/prestamo.py`; antes de entregar integrar la enumeración `EstadoPrestamo` y operaciones de `Prestamo` en el diagrama final ampliado o aclarar que son agregados distintos |
| C3 | Ejemplar tiene historial de muchas reservas, pero solo una activa | La multiplicidad histórica `0..*` es válida; unicidad activa requiere restricción transaccional |
| C4 | `reservas → integracion_academica` no debe implicar acceso directo a base externa | Respeta ADR-003 mediante `ServicioMatricula`; dependencias dibujadas acíclicas |
| C5 | `camelCase` versus `snake_case` | Correspondencias documentadas en `round-trip.md` |

## Ejemplo de falso positivo a verificar
**Propuesta atribuible a una posible revisión automática (no resultado real de una ejecución):** «`Ejemplar 1 -- 0..* Reserva` permite reservar simultáneamente el mismo ejemplar».
**Verificación:** falso positivo si se interpreta la multiplicidad como reservas activas: expresa historial de reservas, no concurrencia. La restricción única de reserva activa se aplica en repositorio y PostgreSQL. **Decisión:** mantener multiplicidad y documentar restricción.

## Cambio pendiente
Para C2 completo, agregar las operaciones del préstamo al diseño de clases, y para E6 generar el diagrama inverso real.
