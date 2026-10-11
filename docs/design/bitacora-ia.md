# Bitácora de uso de IA — BiblioUNSA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
| --- | --- | --- | --- | --- | --- | --- |
| x | 10/10/2026 | ChatGPT | Generar el esqueleto en Python del diagrama de clases realizado anteriormente, implementando una lógica mínima. | Propuso un esqueleto en Python basado en el diagrama de clases proporcionado. | Se corrigieron las relaciones entre las clases dentro del código generado. | Corregido |
| x | 10/10/2026 | ChatGPT | Revisar la consistencia entre los diagramas de PlantUML y Mermaid según ciertas reglas. | Propuso una tabla en la que se identifican las reglas incumplidas y las posibles correcciones. | Se corrigió un error en el análisis de una de las reglas establecidas. | Corregido |

## Anexo: prompts completos

### Interacción x

Genera el esqueleto en Python 3.14 del siguiente diagrama de clases de BiblioUNSA, utilizando dataclasses y type hints. Respeta los nombres de las clases y enumeraciones. Convierte los nombres de atributos, parámetros y operaciones a snake_case. Representa las interfaces como clases abstractas mediante ABC y @abstractmethod, respetando las multiplicidades. Implementa únicamente la lógica mínima. [Diagrama de clases].

### Interacción x

Actúa como revisor de diseño. Te paso 6 diagramas UML en PlantUML/Mermaid.
Verifica estas reglas y responde en una tabla (regla, elemento, problema, corrección sugerida): C1: cada mensaje de secuencia corresponde a una operación de la clase receptora; C2: cada transición de estados corresponde a una operación de la clase; C3: multiplicidades coherentes con los criterios de aceptación; C4: paquetes sin ciclos; C5: nombres consistentes. No reescribas los diagramas; solo reporta los hallazgos y cita las líneas correspondientes.
