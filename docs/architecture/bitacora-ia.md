# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 01 / 10 | ChatGPT | Analizar los requisitos y restricciones del proyecto y proponer 3 estilos arquitectónicos, comparando fortalezas y riesgos | Arquitectura de monolito en capas, monolito modular y microservicios | Verificamos R-01 (plazo) y R-03 (presupuesto) | Aceptada |
| 2 | 01 / 10 | ChatGPT | Actuar como abogado del diablo e identificar 5 riesgos de la arquitecutra propuesta anteriormente | Riesgos de sobrearquitectura, acoplamiento entre módulos, fallos o lentitud de APIs, dobles reservas y punto único de fallo | Se corrigió para alinearlo con los escenarios de calidad: seguridad, consistencia y rendimiento | Corregida |
| 3 | 01 / 10 | ChatGPT | Analizar matriz de decisión y arquitectura seleccionada para devolver el código Mermaid para generar el diagrama | Una código Mermaid con dos actores y dos subgraphs para dividir en FrontEnd y Backend, respetando módulos | Se corrige la visibilidad de algunas tecnologías no específicadas en el prompt inicialmente | Corregida |
| 3 | ... | ... | ... | ... | ... | Aceptada / Corregida / Rechazada |

---

# Anexo: Prompts

## Prompt 1

Actúa como arquitecto de software senior con experiencia en sistemas universitarios.
Contexto: plataforma "BiblioUNSA" para la gestión de biblioteca universitaria. Los estudiantes pueden buscar libros por título, autor, categoría y disponibilidad; reservar y cancelar ejemplares; los bibliotecarios registran préstamos mediante carné QR; además, el sistema gestiona multas, autenticación institucional y validación de matrícula mediante la API del sistema académico. Se esperan aproximadamente 200 usuarios concurrentes consultando catálogo y disponibilidad.
Restricciones: 3 developers con experiencia en Python, JavaScript, Angular, Django, PostgreSQL y Git; presupuesto bajo; MVP en producción en 1 mes; el sistema académico solo puede consultarse mediante API, sin acceso directo a su base de datos.
Atributos prioritarios: seguridad e interoperabilidad, fiabilidad para evitar dobles reservas, rendimiento con p95 <= 2 s bajo carga concurrente y mantenibilidad.
Tarea: propón 3 alternativas de estilo arquitectónico. Para cada una indica fortalezas, debilidades, riesgos y qué atributos de calidad favorece o penaliza.
Formato: tabla comparativa en Markdown y, al final, tu recomendación justificada.
No inventes APIs ni capacidades de servicios; si no estás seguro, indícalo.

## Prompt 2

Ahora actúa como "abogado del diablo". Critica la arquitectura recomendada para BiblioUNSA: ¿qué podría fallar considerando el MVP en 1 mes, 3 developers, bajo presupuesto y dependencia de APIs institucionales? Enumera los 5 riesgos más graves y, para cada uno, indica el driver afectado y una táctica de mitigación.

## Prompt 3
Actúa como arquitecto de software senior. Contexto: estamos desarrollando BiblioUNSA, un sistema de biblioteca universitaria. Según nuestra matriz de decisión, la arquitectura seleccionada es un monolito modular. El sistema tendrá un frontend en Angular, un backend en Django y una base de datos PostgreSQL. Dentro del backend deben distinguirse los módulos de Catálogo, Reservas, Préstamos, Multas, Usuarios y Autenticación, e Integración Académica. Además, el sistema debe comunicarse con un servicio de autenticación institucional y con la API del sistema académico para validar la matrícula. Restricciones: equipo de 3 developers, presupuesto bajo, MVP en 1 mes y sin acceso directo a la base de datos del sistema académico. No inventes APIs, protocolos, servicios ni tecnologías adicionales que no hayan sido especificadas. Tarea: genera el código Mermaid de un diagrama de arquitectura que represente claramente el monolito modular, sus módulos internos, el frontend, la base de datos, los actores Estudiante y Bibliotecario y los servicios externos. Usa un flowchart LR, agrupa los módulos del backend con subgraph y devuelve el código Mermaid.