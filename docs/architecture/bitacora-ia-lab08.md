# Bitácora de uso de IA - Lab 08

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 30/09/2026 | ChatGPT | Analizar los casos de la guía y recomendar uno adecuado | Propuso BiblioUNSA por ser manejable para el laboratorio | Se verificó que el caso estuviera en la guía y cumpliera los requisitos | Aceptada |
| 2 | 30/09/2026 | ChatGPT | Desarrollar drivers y alternativas arquitectónicas | Propuso monolito en capas, monolito modular y microservicios | Se compararon las alternativas considerando un mes, tres desarrolladores y presupuesto bajo | Corregida |
| 3 | 30/09/2026 | ChatGPT | Generar arquitectura de BiblioUNSA en Mermaid | Propuso actores, módulos, base de datos y servicios externos | Se corrigió la integración para utilizar exclusivamente la API académica | Corregida |
| 4 | 02/10/2026 | ChatGPT | Revisar ADR-003 de integración académica | Propuso consumir la API académica mediante un módulo de integración | Se verificó que R-04 prohíbe acceder directamente a la base de datos académica | Aceptada |
| 5 | 03/10/2026 | ChatGPT | Comparar PostgreSQL con una base documental | Recomendó PostgreSQL para gestionar reservas, préstamos y multas | Se comprobó su coherencia con los requisitos de integridad y concurrencia | Aceptada |
| 6 | Por registrar | ChatGPT | Evaluar la arquitectura mediante ATAM-lite | Pendiente de registrar la respuesta real | Verificar los hallazgos con ADR-006 a ADR-008, el modelo C4 y las simulaciones. Si existe un falso positivo, registrar aquí la afirmación y la evidencia que la refuta | Pendiente |

## Anexo: prompts completos

### Interacción 1

Analiza los casos disponibles de la guía del Laboratorio 04 y recomiéndame uno que permita cumplir las actividades sin agregar demasiada complejidad.

### Interacción 2

Usando BiblioUNSA como caso, desarrolla los drivers, atributos de calidad, restricciones, alternativas arquitectónicas y matriz de decisión, respetando un MVP de un mes, un equipo de tres desarrolladores y presupuesto bajo.

### Interacción 3

Genera una arquitectura para BiblioUNSA en Mermaid utilizando la alternativa seleccionada. Incluye actores, módulos, almacenamiento y servicios externos.

### Interacción 4

Revisa el ADR-003 de BiblioUNSA. El sistema debe validar la matrícula vigente mediante una API del sistema académico y no puede acceder directamente a su base de datos. Verifica si la decisión es coherente con seguridad, interoperabilidad y bajo acoplamiento.

### Interacción 5

Compara PostgreSQL y una base documental para BiblioUNSA. Considera reservas concurrentes, préstamos, multas, integridad de datos, costo operativo y equipo pequeño. Recomienda una opción y enumera riesgos.

### Interacción 6

Actúa como evaluador ATAM escéptico. Te paso el árbol de utilidad, los ADR-006 a 008, la vista de contenedores y los resultados de las simulaciones [pegar]. Para cada escenario (H,*) identifica: puntos de sensibilidad, puntos de trade-off, riesgos y no riesgos. Para cada riesgo indica probabilidad e impacto (1 a 5) y una pregunta incómoda que el equipo debería poder responder. No propongas rediseños completos; cita la evidencia que te falta.
