# ADR-003: Integrar el sistema académico únicamente mediante API

- Estado: Aceptado
- Fecha: 2026-10-02
- Decisores: Grupo 3

## Contexto

RF-06 indica que BiblioUNSA debe validar que el estudiante tenga matrícula vigente.

R-04 establece que el sistema académico debe consultarse mediante API y no mediante acceso directo a su base de datos.

QA-01 prioriza la seguridad e interoperabilidad del sistema.

## Alternativas consideradas

1. Acceder directamente a la base de datos del sistema académico.
2. Consumir la API del sistema académico mediante un módulo de integración.

## Decisión

BiblioUNSA consumirá la API del sistema académico mediante el módulo de integración.

No se realizará acceso directo a la base de datos académica ni se almacenarán credenciales de conexión a dicha base de datos.

## Consecuencias

### Positivas

- Reduce el acoplamiento con el sistema académico.
- Mejora la seguridad.
- Respeta la restricción de interoperabilidad definida para el caso.
- Permite modificar la implementación interna del sistema académico sin afectar directamente a BiblioUNSA.

### Negativas / riesgos

- La validación depende de la disponibilidad de la API externa.
- Si la API demora o deja de responder, la validación de matrícula puede verse afectada.
- Será necesario implementar manejo de errores, timeouts y reintentos.
