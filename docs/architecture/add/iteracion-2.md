# E4 — Iteración 2 de ADD: rendimiento del catálogo (QA-01)

## 1. Revisar las entradas
Se mantiene el caso BiblioUNSA de los laboratorios 04–07, con un monolito modular, tres desarrolladores, presupuesto limitado y un mes para adaptar el sistema.
El escenario de crecimiento incorpora todas las facultades y la biblioteca virtual.
Se selecciona QA-01 del árbol de utilidad del Lab 08, con prioridad (H,M).

## 2. Establecer el objetivo

QA-01: responder consultas al catálogo con latencia p95 menor o igual a 500 ms, considerando una carga objetivo de 12 solicitudes por segundo.
El propósito de esta iteración es evaluar tácticas que permitan reducir la latencia de las consultas sin cambiar el estilo arquitectónico del ADR-001.

## 3. Elegir el elemento a refinar

Se refina el módulo de catálogo y su acceso a datos, específicamente las consultas de disponibilidad y búsqueda de ejemplares.

## 4. Elegir conceptos de diseño candidatos
| Alternativa | Ventaja | Trade-off | Decisión |
|---|---|---|---|
| Consulta sin optimización | Implementación sencilla | Mayor latencia | Rechazada como diseño final |
| Índices en PostgreSQL | Reduce el costo de búsqueda | Mayor costo de escritura y almacenamiento | Aceptada |
| Índice y caché con TTL | Disminuye consultas repetidas | Riesgo de datos desactualizados | Aceptada como opción complementaria |
| Migración a microservicios | Despliegue independiente | Mayor complejidad y costo operativo | Rechazada por las restricciones del proyecto |

La propuesta conserva el monolito modular del ADR-001.

## 5. Instanciar elementos y asignar responsabilidades
- Catálogo: recibe las consultas de búsqueda y disponibilidad.
- PostgreSQL: almacena ejemplares y utiliza índices para optimizar lecturas.
- Caché: conserva temporalmente resultados de consulta.
- Reservas: verifica la disponibilidad actual antes de confirmar una reserva.

La caché nunca debe utilizarse como única garantía de disponibilidad de un ejemplar.

## 6. Bosquejar vistas y registrar decisiones

Se conserva la estructura del monolito modular y se propone incorporar índices y una caché de lectura del catálogo.

La decisión debe registrarse en ADR-007 y reflejarse en el modelo C4 si se incorpora una tecnología o componente nuevo.

La política propuesta requiere invalidación o expiración de caché y confirmación atómica de la reserva.

## 7. Analizar el diseño y verificar el objetivo

Se ejecutó una simulación sintética reproducible con semilla 42 y 1200 muestras de latencia por alternativa mediante `fitness/rendimiento.py`.
| Alternativa | p95 simulado | Comparación con 500 ms |
|---|---:|---|
| Sin optimizar | 830.61 ms | No cumple |
| Índice | 340.79 ms | Cumple en el modelo |
| Índice y caché | 155.42 ms | Cumple en el modelo |

Se ejecutaron cuatro pruebas específicas de rendimiento y todas aprobaron.

**Limitación:** el simulador genera latencias aleatorias dentro de rangos predefinidos. No modela la concurrencia, la cola de solicitudes ni la carga efectiva de 12 solicitudes por segundo. Por tanto, los resultados solo respaldan una comparación ilustrativa; todavía no demuestran el cumplimiento real de QA-01.

**Trade-off principal:** una caché reduce latencia de lectura, pero puede presentar disponibilidad desactualizada.

**Riesgos:** invalidación incorrecta de caché, consultas con índices inadecuados y cambios en la distribución real de la carga.

**Conclusión:** se propone adoptar índices como primera táctica y evaluar caché con TTL como complemento. El cumplimiento definitivo de QA-01 requiere pruebas de carga sobre un prototipo o implementación real.
