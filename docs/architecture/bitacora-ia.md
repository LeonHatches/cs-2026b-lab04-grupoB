# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 30/09/2026 | ChatGPT | Analizar los casos de la guía y recomendar uno adecuado | Propuso BiblioUNSA por ser manejable para E1–E8 | Se revisó que el caso aparezca en la guía y que incluya seguridad e interoperabilidad | Aceptada |
| 2 | 30/09/2026 | ChatGPT | Desarrollar drivers, alternativas y matriz para BiblioUNSA | Propuso monolito en capas, monolito modular y microservicios | Se comparó con plazo de 1 mes, equipo de 3 y presupuesto bajo | Corregida |
| 3 | 30/09/2026 | ChatGPT | Generar arquitectura Mermaid de BiblioUNSA | Incluyó actores, módulos, BD y servicios externos | Se corrigió para mantener la integración académica solo mediante API | Corregida |
| 4 | 30/09/2026 | ChatGPT | Proponer ADR y división del trabajo | Propuso ADR de estilo, BD e integración | Se verificó que cada ADR tenga contexto, alternativas, decisión y consecuencias | Aceptada |
| 5 | 02/10/2026 | ChatGPT | Revisar ADR-003 de integración académica | Propuso consumir la API académica mediante módulo de integración | Se verificó que R-04 prohíbe acceso directo a la BD académica | Aceptada |
| 6 | 02/10/2026 | ChatGPT | Crear vista de despliegue con Python Diagrams | Propuso usuarios, Nginx, aplicación, PostgreSQL, API académica, correo y monitoreo | Se corrigió el entorno instalando Diagrams y Graphviz y se verificó el PNG final | Corregida |
| 7 (I2-1, León Hatches) | 03/10/2026 | Codex | Comparar PostgreSQL y una base documental para reservas, préstamos y multas | Recomendó PostgreSQL por las relaciones entre entidades y las operaciones transaccionales; señaló migraciones y control de concurrencia como riesgos | Se contrastó con RF-02/RF-03/RF-04, QA-02 y R-03, y con la documentación oficial de PostgreSQL y MongoDB. MongoDB también admite transacciones; elegir PostgreSQL no demuestra por sí solo los 1000 intentos de QA-02 | Aceptada con verificación |
| 8 (I2-2, León Hatches) | 03/10/2026 | Codex | Revisar PlantUML de monolito en capas con identidad institucional y API académica | Identificó que el borrador del informe (pp. 12-13) incluye WhatsApp y omite identidad institucional; propuso usar el código de la guía del Integrante 2 | Se corrigió la variante del borrador al crear alternativa.puml: se omitió WhatsApp y se incluyó Identidad institucional, respetando literalmente la guía. Se conservaron la API académica, las tres capas y la nota 4,05 frente a 4,55. El PDF original no se modificó | Corregida respecto del borrador del informe |

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

### Interacción 7 / I2-1 - Integrante 2 (León Hatches)

Fecha de la revisión: 03/10/2026. Herramienta: Codex.

Consigna de la guía del Integrante 2, atendida dentro de la solicitud de seguirla en esta sesión:

> Compara PostgreSQL y una base documental para BiblioUNSA. Considera reservas concurrentes, prestamos, multas, integridad de datos, costo operativo y equipo pequeno. Recomienda una opcion y enumera riesgos.

Respuesta y verificación:

- PostgreSQL permite modelar las relaciones entre Libro, Ejemplar, Reserva, Prestamo, Multa y Usuario y agrupar operaciones críticas en transacciones. Coincide con el ADR-002 y con las tecnologías conocidas por el equipo en R-02.
- Una base documental puede ser útil para estructuras variables, pero el caso exige coordinar entidades relacionadas. MongoDB también soporta transacciones: no se descartó atribuyéndole una ausencia de esa capacidad.
- Riesgos: migraciones del esquema, operación y respaldo de la base de datos, y diseño correcto del control de concurrencia. Las transacciones y restricciones deben implementarse y probarse; no se ejecutaron pruebas de 1000 reservas porque este repositorio contiene documentación arquitectónica.
- Verificación documental realizada en esta sesión: RF-02, RF-03, RF-04, QA-02 y R-03 de drivers.md coinciden con la guía. El ADR conserva el contenido y la fecha de decisión indicados por la guía (2026-09-30); esta revisión ocurrió el 03/10/2026.
- Decisión del registro: Aceptada con verificación. La aprobación humana del PR queda pendiente.

Fuentes consultadas:

- [PostgreSQL: transacciones](https://www.postgresql.org/docs/current/tutorial-transactions.html).
- [MongoDB: transacciones](https://www.mongodb.com/docs/manual/core/transactions/).

### Interacción 8 / I2-2 - Integrante 2 (León Hatches)

Fecha de la revisión: 03/10/2026. Herramienta: Codex.

Consigna de la guía del Integrante 2, atendida dentro de la misma sesión:

> Genera o revisa un diagrama PlantUML de la alternativa monolito en capas para BiblioUNSA. Debe incluir Estudiante, Bibliotecario, Presentacion, Logica de negocio, Acceso a datos, PostgreSQL, identidad institucional y API del sistema academico. No permitas acceso directo a la BD academica.

Respuesta y evidencia de corrección:

- Antes: el borrador PlantUML del informe, páginas 12-13, contiene `cloud "WhatsApp" as WA` y `BL --> WA`, y no incluye identidad institucional.
- Después: [alternativa.puml](diagramas/alternativa.puml) reproduce el código de la guía, páginas 3-4, con `cloud "Identidad institucional" as SSO` y `NEG --> SSO`; no contiene WhatsApp.
- La integración académica se conserva como `NEG --> ACAD`, siendo ACAD la API del sistema académico. La única base de datos representada es PostgreSQL de BiblioUNSA.
- Se verificaron Estudiante, Bibliotecario, Presentacion, Logica de negocio y Acceso a datos. La nota tiene cuatro líneas y mantiene los puntajes 4,05 y 4,55 de la matriz acordada.
- Validación realizada: PlantUML 1.2026.8 ejecutado localmente, comprobación de sintaxis y exportación a [PNG](diagramas/img/alternativa.png) y [SVG](diagramas/img/alternativa.svg). Se revisó visualmente el PNG y se verificaron los textos del SVG. La validación en plantuml.com/plantuml indicada en la guía queda pendiente: el entorno bloqueó el envío del código a ese servidor externo.
- La corrección se refiere a la variante del borrador suministrado, no a un error inventado en una respuesta nueva ni a una modificación del PDF. Se aplicó al archivo del repositorio siguiendo la guía individual.
- Decisión del registro: Corregida respecto del borrador del informe. La revisión humana del PR queda pendiente.

Estas dos entradas documentan dos consignas resueltas en una misma sesión; no representan dos conversaciones independientes ni una aprobación del revisor.
