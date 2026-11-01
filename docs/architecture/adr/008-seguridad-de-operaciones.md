# ADR-008: Autorización en el backend

- **Estado:** Aceptado
- **Fecha:** 2026-10-31
- **Decisores:** Equipo BiblioUNSA (3 developers)

## Contexto

BiblioUNSA debe impedir que usuarios sin permisos realicen operaciones sobre préstamos y multas. El escenario QA-05 establece como objetivo cero accesos indebidos en 100 intentos.

## Alternativas consideradas

1. **Control en frontend:** Es sencillo, pero el usuario puede manipular los roles enviados.
2. **Autorización en backend:** Comprueba los permisos antes de ejecutar una operación.
3. **Servicio externo de políticas:** Ofrece más opciones de control, pero aumenta la complejidad.

## Decisión

Se adopta la autorización en el backend, utilizando el rol autenticado del usuario para comprobar sus permisos.

Se descarta depender únicamente del frontend y utilizar un servicio externo de políticas por la complejidad adicional.

## Evidencia

Se simularon 100 intentos de acceso no autorizado.

- Antes: 100 accesos indebidos.
- Después: 0 accesos indebidos.

La simulación cumple QA-05, aunque todavía se necesitan pruebas con la autenticación real del sistema.

## Consecuencias

- **Positivas:** evita confiar en roles enviados por el cliente y mejora el control de acceso.
- **Negativas/riesgos:** requiere verificar permisos en cada operación protegida.
- **Trade-off:** se acepta una validación adicional para evitar accesos no autorizados.
