# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 08/10/2026 | ChatGPT | Modelar la historia de usuario de reserva según ADR-001, ADR-002 y ADR-003. | Propuso las clases como Estudiante, Ejemplar y Reserva, además de interfaces para la integración. | Se verifico y corrigio clases faltantes para completar lógica | Corregido |
| 2 | 08/10/2026 | ChatGPT | Generar un diagrama de secuencia que contemple los casos de error durante una reserva. | Propuso un flujo de validación, transacción y notificación utilizando fragmentos. | Se verificó la utilización de los fragmentos UML y la presencia de mensajes de retorno. | Corregido |
| 3 | 08/10/2026 | ChatGPT | Modelar los estados y transiciones del proceso de préstamo. | Propuso una máquina de estados basada en las transiciones del préstamo. | Se separaron las responsabilidades de Prestamo y Reserva, revisando la correspondencia entre transiciones y operaciones según C2. | Corregido |
| 4 | 09/10/2026 | ChatGPT | Describir el diagrama de actividades del proceso de devolución de libros. | Propuso tres carriles de actividades e incorporó el cálculo de multas por retraso. | Se ajustó la rama correspondiente al caso en que no se encuentra un préstamo activo. | Corregido |
| 5 | 09/10/2026 | ChatGPT | Revisar las dependencias entre los paquetes de acuerdo con las decisiones arquitectónicas del ADR. | Propuso una organización modular sin dependencias cíclicas. | Se rechazó cualquier dependencia que permitiera acceder directamente a la base de datos del sistema académico. | Corregido |
| 6 | 10/10/2026 | ChatGPT | Generar el esqueleto en Python del diagrama de clases realizado anteriormente, implementando una lógica mínima. | Propuso un esqueleto en Python basado en el diagrama de clases proporcionado. | Se corrigieron las relaciones entre las clases dentro del código generado. | Corregido |
| 7 | 10/10/2026 | ChatGPT | Revisar la consistencia entre los diagramas de PlantUML y Mermaid según ciertas reglas. | Propuso una tabla en la que se identifican las reglas incumplidas y las posibles correcciones. | Se corrigió un error en el análisis de una de las reglas establecidas. | Corregido |

## Anexo: prompts completos

### Interacción 1

Modela la historia de usuario de reserva de libros para el sistema BiblioUNSA, tomando como referencia las decisiones arquitectónicas ADR-001, ADR-002 y ADR-003. Identifica las clases principales del dominio, como Estudiante, Ejemplar y Reserva, y las interfaces necesarias para comunicarse con el sistema académico. Mantén separadas las responsabilidades del dominio y de la integración externa.

### Interacción 2

Genera un diagrama de secuencia UML para el proceso de reserva de libros en BiblioUNSA. Considera la validación de matrícula, la comprobación de disponibilidad, el registro de la reserva y la notificación al estudiante. Incluye escenarios de error y utiliza los fragmentos UML alt, loop y opt cuando corresponda.

### Interacción 3

Modela un diagrama de estados UML para representar el ciclo de vida de un préstamo en BiblioUNSA. Identifica los estados, eventos y transiciones permitidas. Mantén diferenciados los procesos de reserva y préstamo, y verifica que las transiciones tengan operaciones correspondientes en las clases del dominio.

### Interacción 4

Genera un diagrama de actividades UML para el proceso de devolución de libros en BiblioUNSA. Utiliza tres carriles: Estudiante, Bibliotecario y Sistema BiblioUNSA. Incluye la identificación del préstamo, el cálculo de retrasos, la generación de multas cuando corresponda, la actualización del estado del ejemplar y el tratamiento de errores cuando no se encuentra un préstamo activo.

### Interacción 5

Revisa las dependencias entre los paquetes y módulos de BiblioUNSA según las decisiones arquitectónicas definidas en los ADR. Verifica que no existan dependencias cíclicas, que los módulos mantengan sus responsabilidades y que la comunicación con el sistema académico se realice exclusivamente mediante su API, sin acceso directo a su base de datos.

### Interacción 6

Genera el esqueleto en Python 3.14 del siguiente diagrama de clases de BiblioUNSA, utilizando dataclasses y type hints. Respeta los nombres de las clases y enumeraciones. Convierte los nombres de atributos, parámetros y operaciones a snake_case. Representa las interfaces como clases abstractas mediante ABC y @abstractmethod, respetando las multiplicidades. Implementa únicamente la lógica mínima. [Diagrama de clases].

### Interacción 7

Actúa como revisor de diseño. Te paso 6 diagramas UML en PlantUML/Mermaid. [Código de Diagramas]
Verifica estas reglas y responde en una tabla (regla, elemento, problema, corrección sugerida). C1: cada mensaje de secuencia corresponde a una operación de la clase receptora. C2: cada transición de estados corresponde a una operación de la clase. C3: multiplicidades coherentes con los criterios de aceptación. C4: paquetes sin ciclos. C5: nombres consistentes. No reescribas los diagramas; solo reporta los hallazgos y cita las líneas correspondientes.