# ADR-006: Disponibilidad de la integración académica

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo BiblioUNSA (3 developers)

## Contexto

BiblioUNSA necesita validar la matrícula de los estudiantes mediante una API académica. Si este servicio deja de funcionar, las solicitudes pueden perderse. Se busca conservarlas durante una caída de 20 minutos y procesarlas cuando el servicio se recupere, según QA-03 y QA-04.

## Alternativas consideradas

1. **Reintentos:** Permiten manejar fallos breves, pero no caídas prolongadas.
2. **Cola en PostgreSQL:** Guarda las solicitudes pendientes hasta que puedan procesarse.
3. **Circuit Breaker:** Evita llamadas repetidas a un servicio caído, pero no conserva solicitudes.
4. **Microservicios con broker:** Separan el procesamiento, pero aumentan la complejidad.

## Decisión

Se adopta una cola persistente en PostgreSQL para conservar las solicitudes pendientes y procesarlas cuando vuelva la API académica. Se descartan los microservicios por su complejidad y el alcance del proyecto.

Las solicitudes pendientes no se consideran reservas confirmadas hasta validar la matrícula y la disponibilidad del ejemplar.

## Evidencia

Se simularon 100 solicitudes y una caída de 20 minutos.

- Sin cola: 20 solicitudes perdidas.
- Con cola: 0 solicitudes perdidas.
- Recuperación: 20 solicitudes en 4 minutos.

La simulación cumple QA-03 y QA-04, aunque todavía no demuestra la persistencia real en PostgreSQL.

## Consecuencias

- **Positivas:** evita perder solicitudes y permite recuperarlas después de una caída.
- **Negativas/riesgos:** requiere controlar los reintentos, posibles duplicados y el almacenamiento.
- **Trade-off:** se acepta una confirmación más lenta a cambio de conservar las solicitudes.
