# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|-------|-------------|------------------|-------------------|------------------------------|----------|
| 1 | 01 / 10 | ChatGPT | Analizar los requisitos y restricciones del proyecto y proponer 3 estilos arquitectónicos, comparando fortalezas y riesgos | Arquitectura de monolito en capas, monolito modular y microservicios | Verificamos R-01 (plazo) y R-03 (presupuesto) | Aceptada |
| 2 | 01 / 10 | ChatGPT | Actuar como abogado del diablo e identificar 5 riesgos de la arquitecutra propuesta anteriormente | Riesgos de sobrearquitectura, acoplamiento entre módulos, fallos o lentitud de APIs, dobles reservas y punto único de fallo | Se corrigió para alinearlo con los escenarios de calidad: seguridad, consistencia y rendimiento | Corregida |
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