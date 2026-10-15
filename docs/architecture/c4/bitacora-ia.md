# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 15/10/2026 | ChatGPT | Analizar inventario, ADR-001 y depliegue para estructrar un modelo C4 base como borrador | Borrador de modelo C4 completo con vistas y relaciones de todos los diagramas del modelo | Se verifico que todos los sistemas externos y personas sean representados de forma correcta, se corrigio la inclusión de un sistema externo extra | Corregida |

## Anexo: prompts completos

### Interacción 1
Actúa como arquitecto de software experto en el modelo C4 y en Structurizr DSL. Contexto: [Inventario.md - ADR-001 - Despligeue.py] Tarea: escribe un workspace de Structurizr DSL con personas, el sistema, sus contenedores (con tecnología), los componentes del contenedor API, los sistemas externos (con la etiqueta "Externo") y relaciones con descripción y protocolo. Incluye las vistas systemContext, container, component, dynamic (confirmar y pagar) y deployment (entorno "Producción"). Restricciones: usa SOLO las tecnologías del ADR-001; no confundas contenedor C4 con contenedor Docker; usa !identifiers hierarchical. Formato: solo el código DSL.