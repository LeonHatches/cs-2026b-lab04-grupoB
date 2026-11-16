# Bitácora de uso de IA — BiblioUNSA (Laboratorio 09)

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 14/11/2026 | ChatGPT | Revisar el contrato JSON y el dataset de criterios de aceptación para las historias de usuario de BiblioUNSA. | Propuso una estructura JSON con identificador de historia, estado de investigación, preguntas y escenarios de aceptación. | Se verificaron los campos obligatorios, los tipos de datos y los casos de historias ambiguas que requieren aclaración. | Aceptado |
| 2 | 14/11/2026 | ChatGPT | Analizar el prompt v1 para generar criterios de aceptación a partir de historias de usuario. | Identificó que el prompt inicial no establecía restricciones suficientes sobre el formato de salida ni sobre la información que podía asumir. | Se compararon las respuestas con el esquema JSON y las aserciones de Promptfoo. Se identificaron respuestas en Markdown que no cumplían el contrato. | Corregido |
| 3 | 14/11/2026 | ChatGPT | Mejorar los prompts v2 y v3 utilizando elementos de la anatomía de un prompt y patrones de ingeniería de prompts. | Propuso incorporar rol, contexto, tarea, restricciones y formato de salida, además de instrucciones para solicitar aclaraciones cuando faltara información. | Se verificó que las versiones mantuvieran el contrato JSON y contemplaran escenarios de éxito, error y borde. | Aceptado |
| 4 | 14/11/2026 | ChatGPT | Diseñar el prompt SQL para traducir preguntas bibliotecarias a consultas de solo lectura. | Propuso generar consultas SELECT parametrizadas y rechazar instrucciones que intentaran modificar la base de datos. | Se verificó el uso del esquema de pruebas, los parámetros nombrados y el rechazo de instrucciones DELETE, DROP e inyecciones. | Corregido |
| 5 | 15/11/2026 | ChatGPT | Implementar los generadores de criterios y SQL en Python utilizando el puerto ProveedorLLM del Laboratorio 07. | Propuso separar los generadores, cargar las plantillas por versión y validar las respuestas mediante esquemas JSON. | Se verificó la integración con ProveedorLLM, la validación de respuestas y las pruebas unitarias. Se ejecutaron 22 pruebas y todas fueron aprobadas. | Aceptado |
| 6 | 15/11/2026 | ChatGPT | Configurar la integración continua y revisar los resultados de las evaluaciones de prompts mediante Promptfoo. | Propuso un workflow de GitHub Actions para ejecutar las pruebas Python y las evaluaciones de criterios y SQL en cada Pull Request. | Se ejecutaron localmente ambas evaluaciones: cada tarea obtuvo 16 aprobados y 8 fallidos. Se identificó que v1 necesita mejoras y que todavía debe comprobarse el workflow en GitHub Actions. | Aceptado |

## Anexo: prompts completos

### Interacción 1

Actúa como analista de requisitos del sistema BiblioUNSA. Revisa el contrato JSON para generar criterios de aceptación a partir de historias de usuario. Considera los campos historia_id, invest_ok, preguntas y escenarios. Verifica que cada escenario contenga titulo, tipo, dado, cuando y entonces. Comprueba que las historias ambiguas o que carecen de información suficiente soliciten aclaraciones en lugar de inventar requisitos. Propón las correcciones necesarias para que el esquema JSON permita validar las respuestas automáticamente.

### Interacción 2

Actúa como especialista en ingeniería de prompts. Analiza el prompt v1 utilizado para generar criterios de aceptación de BiblioUNSA. Identifica sus limitaciones en cuanto a instrucciones, contexto, restricciones y formato de salida. Considera los resultados de las evaluaciones realizadas con Promptfoo y explica por qué las respuestas pueden incumplir el contrato JSON. Propón mejoras concretas que puedan incorporarse en las siguientes versiones del prompt.

### Interacción 3

Mejora los prompts v2 y v3 para generar criterios de aceptación de BiblioUNSA. Utiliza elementos de la anatomía de un prompt, como rol, contexto, tarea, restricciones, formato de salida y ejemplos cuando corresponda. Incorpora patrones de ingeniería de prompts que permitan mejorar la calidad de las respuestas. El generador debe identificar historias ambiguas, solicitar aclaraciones cuando falte información y producir escenarios de éxito, error y borde cuando la historia sea suficientemente clara. La salida debe cumplir estrictamente el esquema JSON establecido.

### Interacción 4

Actúa como traductor de preguntas de bibliotecarios a consultas SQL de solo lectura para BiblioUNSA. Utiliza el esquema de base de datos proporcionado, que contiene las tablas libros, ejemplares y prestamos. Genera exclusivamente consultas SELECT con parámetros nombrados. Si la pregunta no contiene información suficiente, devuelve una solicitud de aclaración con consulta_sql en null. Rechaza cualquier instrucción que intente ejecutar INSERT, UPDATE, DELETE, DROP, ALTER o cualquier operación de modificación. Responde únicamente con un objeto JSON que cumpla el esquema establecido.

### Interacción 5

Ayúdame a implementar los generadores de criterios de aceptación y SQL en Python para el Laboratorio 09. Deben utilizar el puerto ProveedorLLM definido en el Laboratorio 07, recibir el proveedor mediante inyección de dependencias, cargar las plantillas según la versión seleccionada y validar las respuestas mediante sus respectivos esquemas JSON. Considera también el tratamiento de respuestas inválidas y la validación de consultas SQL. Propón pruebas unitarias que comprueben que las respuestas válidas se aceptan y las inválidas se rechazan.

### Interacción 6

Ayúdame a configurar un workflow de GitHub Actions para el Laboratorio 09. El archivo debe ubicarse en .github/workflows/prompts.yml y ejecutar las pruebas de Python y las evaluaciones de Promptfoo para las tareas de criterios de aceptación y generación SQL en cada Pull Request. Utiliza el proveedor grabado para que las evaluaciones sean reproducibles y comprueba que los errores en las grabaciones o las aserciones provoquen un fallo en la integración continua. Explica también cómo registrar los resultados y verificar la ejecución del workflow.