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

## Revisión realizada de E1 y E5 — 10/10/2026

Registro de la conversación de Hatches con Codex y de las correcciones locales realizadas. Las seis entradas anteriores conservan su carácter de propuestas pendientes de validación.

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
| --- | --- | --- | --- | --- | --- | --- |
| 7 | 10/10/2026 | Codex | Revisar la parte estructural, hacer correcciones sin alterar los contratos usados por los compañeros y guardarlas en commits locales sin push. | Separar la concurrencia sobre un ejemplar disponible del rechazo de uno ocupado; escribir los valores de las enumeraciones en líneas separadas; aclarar la correspondencia de paquetes con ADR-001. | Se corrigió el criterio 3 y se agregó el criterio 5; se comprobó que las enumeraciones conservaran nombres y valores; se contrastó ADR-001 y se verificó que el grafo de paquetes no tuviera ciclos. La revisión visual de los diagramas queda pendiente. | Corregido en commits locales; pendiente generar las imágenes y obtener revisión del PR. |
