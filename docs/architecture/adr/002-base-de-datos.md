# ADR-002: Usar PostgreSQL como base de datos principal

- Estado: Aceptado
- Fecha: 2026-09-30
- Decisores: equipo BiblioUNSA

## Contexto

RF-02, RF-03 y RF-04 requieren manejar reservas, prestamos y multas con consistencia. QA-02 exige evitar dobles reservas. R-03 limita el presupuesto, por lo que se busca una solucion madura y operable por un equipo pequeno.

## Alternativas consideradas

1. PostgreSQL relacional.
2. Base documental (por ejemplo MongoDB).

## Decision

Usaremos PostgreSQL como base de datos principal. Las entidades Libro, Ejemplar, Reserva, Prestamo, Multa y Usuario se modelaran de forma relacional y las operaciones criticas se protegeran con transacciones y restricciones de integridad.

## Consecuencias

- Positivas: transacciones ACID, restricciones de integridad, consultas relacionales y buen soporte para evitar reservas inconsistentes.
- Negativas/riesgos: cambios de esquema requieren migraciones y un modelo muy variable puede necesitar mas trabajo que en una BD documental.
