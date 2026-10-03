# Matriz de decisión — BiblioUNSA

## Alternativas
- **A. Monolito en capas:** El sistema se organiza en capas separadas, como presentación, lógica de negocio y acceso a datos. Es sencillo de desarrollar y desplegar, aunque puede dificultar la separación de responsabilidades a medida que el sistema crece.
- **B. Monolito modular:** El sistema se divide en módulos funcionales independientes dentro de una sola aplicación y un único despliegue. Cada módulo concentra su propia lógica y responsabilidades, facilitando el mantenimiento y la evolución del sistema.
- **C. Microservicios:** El sistema se divide en servicios independientes que se comunican mediante APIs. Permite mayor independencia entre componentes, pero aumenta la complejidad de desarrollo, despliegue, comunicación y mantenimiento.

## Criterios y pesos

| Criterio | Peso | Justificación (driver relacionado) |
|---|---:|---|
| Tiempo de entrega | 25 % | R-01: MVP en 1 mes. |
| Seguridad e interoperabilidad | 25 % | QA-01 y R-04: atributos críticos del sistema. |
| Costo operativo | 20 % | R-03: presupuesto reducido. |
| Modificabilidad | 15 % | Necesidad de modificar reglas e integraciones sin rehacer el sistema. |
| Simplicidad operativa | 15 % | R-02: equipo de desarrollo pequeño. |

## Matriz (puntaje: 1 = muy malo; 5 = excelente)

| Criterio (peso) | A | B | C |
|---|---:|---:|---:|
| Tiempo de entrega (25 %) | 5 | 4 | 2 |
| Seguridad e interoperabilidad (25 %) | 3 | 5 | 3 |
| Costo operativo (20 %) | 5 | 4 | 3 |
| Modificabilidad (15 %) | 3 | 5 | 5 |
| Simplicidad operativa (15 %) | 4 | 5 | 1 |
| **Total ponderado** | **4,05** | **4,55** | **2,75** |

## Conclusión
Elegimos el **monolito modular** porque combina un único despliegue con límites claros entre los módulos de **Catálogo, Reservas, Préstamos, Multas e Integración Académica**. Además, ofrece un buen equilibrio entre rapidez de desarrollo, seguridad, modificabilidad y simplicidad operativa, siendo coherente con el plazo establecido, el presupuesto reducido y el tamaño pequeño del equipo.