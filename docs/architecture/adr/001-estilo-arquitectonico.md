# ADR-001: Adoptar un monolito modular para BiblioUNSA

- Estado: Aceptado
- Fecha: 2026-01-10
- Decisores: Equipo BiblioUNSA (3 developers)

## Contexto

R-01 exige un MVP en 1 mes, R-02 limita el equipo a 3 developers y R-03 establece un presupuesto bajo. QA-01 exige seguridad e interoperabilidad con el sistema académico mediante API. Se necesita elegir una arquitectura entre las alternativas de monolito en capas, monolito modular y microservicios.

## Alternativas consideradas

1. Monolito en capas - 4,05.
2. Monolito modular - 4,55.
3. Microservicios - 2,75.

## Decisión

Se adoptará un monolito modular, al obtener el mayor puntaje en la matriz de decisión. El sistema se dividirá en los módulos de Catálogo, Reservas, Préstamos, Multas y Autenticación/Integración, manteniendo interfaces internas claras entre ellos.

## Consecuencias

- Positivas: un solo despliegue, bajo costo, entrega rápida y límites de dominio claros.
- Negativas/riesgos: una falla grave puede afectar el despliegue completo y el equipo debe respetar los límites entre módulos.