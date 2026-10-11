# E7 — Bitácora de apoyo de IA, 07/10/2026
Las siguientes son **interacciones de diseño propuestas/documentadas en esta preparación**, no una transcripción de conversaciones verificadas en servicios externos. El equipo debe revisar y validar antes de entregar.
| # | Herramienta | Instrucción/consulta | Propuesta | Verificación y decisión |
|---|---|---|---|---|
| 1 | ChatGPT | Modelar HU de reserva según ADR-001 a 003 | `Estudiante`, `Ejemplar`, `Reserva`, puertos | Aceptar clases del dominio; separar interfaz académica |
| 2 | ChatGPT | Generar secuencia con casos de error | Validación + transacción + notificación | Aceptar `alt`, `loop`, `opt`; exigir retorno |
| 3 | ChatGPT | Modelar estados de préstamo | Estados de guía y transiciones | Separar `Prestamo` de `Reserva` y revisar C2 |
| 4 | ChatGPT | Describir actividad de devolución | Tres carriles y cálculo de multa | Aceptar; ajustar rama sin préstamo |
| 5 | ChatGPT | Revisar dependencias de paquetes del ADR | Módulos sin ciclos | Rechazar acceso directo a BD académica |
| 6 | ChatGPT | Contrastar UML con Python | ABC, colecciones, diferencias de nombres | Documentar limitaciones de inferencia |
