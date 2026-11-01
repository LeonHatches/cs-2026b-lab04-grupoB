# ADR-007: Optimización del catálogo

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo BiblioUNSA (3 developers)

## Contexto

Con el crecimiento de BiblioUNSA, las consultas al catálogo pueden tardar más en responder. El escenario QA-01 establece un p95 máximo de 500 ms, con una carga objetivo de 12 solicitudes por segundo.

## Alternativas consideradas

1. **Sin optimización:** Mantiene las consultas actuales, pero con mayor latencia.
2. **Índices en PostgreSQL:** Mejoran las búsquedas sin cambiar la arquitectura.
3. **Índices y caché:** Reducen las consultas repetidas, pero pueden mostrar datos desactualizados.
4. **Microservicios:** Permiten separar componentes, pero aumentan el costo y la complejidad.

## Decisión

Se adopta el uso de índices en PostgreSQL para mejorar las consultas del catálogo. También se considera una caché con TTL como complemento.

Se descartan los microservicios porque no son necesarios para el alcance actual del proyecto.

## Evidencia

Se simularon 1200 consultas para comparar las alternativas.

- Sin optimización: p95 de 830.61 ms.
- Con índices: p95 de 340.79 ms.
- Con índices y caché: p95 de 155.42 ms.

Ambas alternativas optimizadas cumplen QA-01 en la simulación, aunque falta comprobar su rendimiento con carga real.

## Consecuencias

- **Positivas:** consultas más rápidas y mejor aprovechamiento de PostgreSQL.
- **Negativas/riesgos:** los índices requieren mantenimiento y la caché puede mostrar información desactualizada.
- **Trade-off:** se acepta mayor mantenimiento para reducir los tiempos de respuesta.
