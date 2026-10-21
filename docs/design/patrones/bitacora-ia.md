# Bitácora de uso de IA — BiblioUNSA

## Bitácora de interacciones con IA

| # | Fecha | Herramienta | Prompt (resumen) | Qué propuso la IA | Qué verificamos o corregimos | Decisión |
|---|---|---|---|---|---|---|
| 1 | 19/10/2026 | ChatGPT | Identificar olores de código en `antes/servicio.py` y proponer patrones GoF para solucionarlos. | Identificó 5 olores de código y propuso patrones de diseño relacionados con los principios SOLID. | Se evaluó la utilidad de los patrones, su complejidad y su relación con los olores detectados. | Corregido |
| 2 | 19/10/2026 | ChatGPT | Refactorizar el código aplicando Strategy, Adapter y Factory sin modificar su comportamiento. | Propuso separar las políticas de multa, adaptar los proveedores académicos y utilizar fábricas para crear objetos. | Se revisó que los patrones mantuvieran el comportamiento original y no introdujeran dependencias innecesarias. | Corregido |
| 3 | 19/10/2026 | ChatGPT | Comparar los métodos de `Prestamo` con el diagrama de estados e identificar transiciones inválidas. | Identificó las transiciones permitidas y las operaciones correspondientes a cada estado del préstamo. | Se contrastaron las transiciones con `estados-prestamo.mmd`, evitando agregar estados u operaciones no contempladas. | Corregido |
| 4 | 20/10/2026 | ChatGPT | Generar diagramas de clases PlantUML para los patrones implementados en el código Python. | Propuso diagramas individuales con clases, relaciones y estereotipos correspondientes a cada patrón. | Se revisaron los nombres de las clases, las relaciones y la correspondencia de los diagramas con el código implementado. | Corregido |
| 5 | 20/10/2026 | ChatGPT | Generar el diagrama de clases completo del sistema BiblioUNSA a partir de sus archivos Python. | Propuso un diagrama general integrando las clases, herencias, asociaciones y dependencias de los distintos módulos. | Se contrastó la estructura propuesta con las clases reales del sistema para evitar relaciones o componentes inexistentes. | Corregido |

## Anexo: prompts completos

### Interacción 1

Actúa como revisor de código experto en refactorización (Fowler) y patrones GoF. Contexto: [pegar antes/servicio.py y la salida de radon]. Tarea: identifica los olores de código. Para cada uno indica: líneas, olor, el patrón GoF que lo resolvería (o "ninguno" si no se justifica), el principio SOLID que mejora y el costo de aplicarlo. Restricciones: no escribas código todavía; no propongas patrones sin un olor concreto; no uses Singleton. Formato: tabla Markdown.

### Interacción 2

Aplica únicamente los patrones Strategy, Adapter y Factory al siguiente código: [pegar archivos Python]. Reglas: (1) no cambies el comportamiento observable; las pruebas de `test_comportamiento.py` deben seguir pasando; (2) no introduzcas Singleton ni estado global; (3) no agregues patrones adicionales; (4) muestra los archivos completos y explica brevemente qué olor de código elimina cada patrón.

### Interacción 3

Analiza la implementación de la clase `Prestamo` y compárala con el diagrama `estados-prestamo.mmd`. Identifica las transiciones válidas e inválidas, verificando que los métodos correspondan con los estados definidos. Propón las correcciones necesarias sin agregar estados ni transiciones que no estén contemplados en el diseño original.

### Interacción 4

Genera un diagrama de clases en PlantUML para cada patrón de diseño implementado en los siguientes archivos: [archivos Python con patrones]. Representa las clases involucradas, sus relaciones de herencia, asociación y dependencia. Utiliza estereotipos UML para identificar los roles de cada patrón, como `<<Strategy>>`, `<<Adapter>>` o `<<Factory>>`. Realiza un diagrama independiente por patrón y respeta la estructura del código existente.

### Interacción 5

Genera un diagrama de clases completo en PlantUML del sistema BiblioUNSA utilizando todos los archivos Python proporcionados: [archivos Python del sistema]. Incluye las clases, atributos, métodos principales y relaciones de herencia, asociación, composición y dependencia que correspondan. Organiza las clases por módulos para facilitar su comprensión. No inventes clases ni relaciones que no estén sustentadas por el código.
