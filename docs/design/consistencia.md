# Consistencia — BiblioUNSA

## Revisión de consistencia con IA

| Regla | Problema identificado | Corrección sugerida |
|---|---|---|
| C1 | Sin incumplimiento. Las llamadas de la secuencia corresponden a operaciones declaradas en las clases o interfaces receptoras. | Sin correción |
| C2 | Sin incumplimiento. Todas las transiciones del préstamo tienen su operación correspondiente en `Prestamo`. | Sin correción |
| C3 | La multiplicidad `0..1` permite préstamos sin reserva, aunque el diagrama de paquetes indica que Préstamos consume reservas confirmadas. | Verificar el criterio de aceptación. Si todo préstamo requiere reserva, establecer multiplicidad `1` en el extremo `Reserva` |
| C3 | Falso positivo. La multiplicidad `0..*` entre `Ejemplar` y `Reserva` podría interpretarse como múltiples reservas activas simultáneas. Sin embargo, representa el historial de reservas. | Mantener la multiplicidad. Garantizar la unicidad de reservas activas mediante Gestor de Base de Datos |
| C4 | Sin incumplimiento. No se identifican dependencias cíclicas entre los paquetes. | Sin correción |
| C5 | Los estados utilizan nombres diferentes: `RESERVADO` frente a `Reservado`, `CON_MULTA` frente a `ConMulta`, etc. | Unificar los identificadores de estados en ambos diagramas, si representan directamente los valores. |
| C5 | Los métodos utilizan `camelCase` en el diseño y `snake_case` en Python. | Falso positivo: es una adaptación válida a las convenciones de Python |
| C5 | El título menciona «Reservar un libro» y la operación utiliza `ejemplarId`. | Falso positivo: el título es general y la operación identifica el ejemplar concreto.  |

