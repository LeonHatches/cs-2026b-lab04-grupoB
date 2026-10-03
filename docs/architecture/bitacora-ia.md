# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 30/09/2026 | ChatGPT | Analizar los casos de la guía y recomendar uno adecuado | Propuso BiblioUNSA por ser manejable para E1–E8 | Se revisó que el caso aparezca en la guía y que incluya seguridad e interoperabilidad | Aceptada |
| 2 | 30/09/2026 | ChatGPT | Desarrollar drivers, alternativas y matriz para BiblioUNSA | Propuso monolito en capas, monolito modular y microservicios | Se comparó con plazo de 1 mes, equipo de 3 y presupuesto bajo | Corregida |
| 3 | 30/09/2026 | ChatGPT | Generar arquitectura Mermaid de BiblioUNSA | Incluyó actores, módulos, BD y servicios externos | Se corrigió para mantener la integración académica solo mediante API | Corregida |
| 4 | 30/09/2026 | ChatGPT | Proponer ADR y división del trabajo | Propuso ADR de estilo, BD e integración | Se verificó que cada ADR tenga contexto, alternativas, decisión y consecuencias | Aceptada |
| 5 | 02/10/2026 | ChatGPT | Revisar ADR-003 de integración académica | Propuso consumir la API académica mediante módulo de integración | Se verificó que R-04 prohíbe acceso directo a la BD académica | Aceptada |
| 6 | 02/10/2026 | ChatGPT | Crear vista de despliegue con Python Diagrams | Propuso usuarios, Nginx, aplicación, PostgreSQL, API académica, correo y monitoreo | Se corrigió el entorno instalando Diagrams y Graphviz y se verificó el PNG final | Corregida |
| 7 | 03/10/2026 | ChatGPT | Comparar PostgreSQL y una base documental | Propuso PostgreSQL para reservas, préstamos y multas | Se verificó la coherencia con RF-02, RF-03, RF-04 y QA-02 | Aceptada |
| 8 | 03/10/2026 | ChatGPT | Revisar alternativa de monolito en capas en PlantUML | Propuso ajustar el diagrama del informe a la guía | Se reemplazó WhatsApp por identidad institucional y se mantuvo la API académica | Corregida |

## Anexo: prompts completos

### Interacción 1
Analiza los casos disponibles de la guía del Laboratorio 04 y recomiéndame uno que permita cumplir E1–E8 sin agregar demasiada complejidad.

### Interacción 2
Usando BiblioUNSA como caso, desarrolla la propuesta necesaria para el laboratorio: drivers, atributos de calidad, restricciones, alternativas arquitectónicas y matriz de decisión, respetando un MVP de un mes, equipo de tres y presupuesto bajo.

### Interacción 3
Genera una arquitectura para BiblioUNSA en Mermaid usando la alternativa seleccionada. Debe incluir actores, módulos, almacenamiento y servicios externos.

### Interacción 4
Propón tres ADR para BiblioUNSA y una división del trabajo entre tres integrantes para poder desarrollar las tareas en paralelo.

### Interacción 5
Revisa el ADR-003 de BiblioUNSA. El sistema debe validar la matrícula vigente de los estudiantes mediante una API del sistema académico y no puede acceder directamente a su base de datos. Verifica si la decisión es coherente con seguridad, interoperabilidad y bajo acoplamiento.

### Interacción 6
Revisa una vista de despliegue para BiblioUNSA. Debe incluir estudiantes y bibliotecarios, navegador o celular, servidor en la nube, proxy HTTPS, aplicación como monolito modular, PostgreSQL, API del sistema académico, correo institucional y monitoreo. Identifica posibles errores o inconsistencias.

### Interacción 7
Compara PostgreSQL y una base documental para BiblioUNSA. Considera reservas concurrentes, préstamos, multas, integridad de datos, costo operativo y equipo pequeño. Recomienda una opción y enumera riesgos.

### Interacción 8
Genera o revisa un diagrama PlantUML de la alternativa monolito en capas para BiblioUNSA. Debe incluir Estudiante, Bibliotecario, Presentación, Lógica de negocio, Acceso a datos, PostgreSQL, identidad institucional y API del sistema académico. No permitas acceso directo a la BD académica.
