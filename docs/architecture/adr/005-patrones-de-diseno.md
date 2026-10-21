# ADR-005: Patrones adoptados y rechazados para BiblioUNSA

- **Estado:** Aceptado
- **Fecha:** 2026-10-20
- **Decisores:** Equipo BiblioUNSA (3 developers)

## Contexto

El sistema BiblioUNSA requiere mejorar la mantenibilidad, extensibilidad y separación de responsabilidades de sus componentes, evitando concentrar demasiada lógica en `ServicioBiblioteca`. Se necesita seleccionar patrones de diseño que permitan gestionar las reglas de multas, la integración con el sistema académico, los estados de préstamos y las notificaciones, sin aumentar innecesariamente la complejidad del MVP.

## Alternativas consideradas

1. **Strategy:** Permite implementar diferentes políticas de multas según el tipo de usuario.
2. **Adapter:** Permite integrar proveedores académicos con interfaces diferentes.
3. **Factory:** Centraliza la creación de adaptadores académicos y políticas de multas.
4. **State:** Organiza los estados y transiciones válidas de los préstamos.
5. **Observer:** Desacopla las notificaciones y auditorías del proceso de reserva.
6. **Decorator:** Incorpora reintentos ante fallos temporales y almacenamiento en caché sin modificar los componentes originales.
7. **Chain of Responsibility:** Permite aplicar validaciones sucesivas a las respuestas del recomendador de libros.
7. **Singleton:** Propone mantener una única instancia global de determinados servicios.

## Decisión

Se adoptarán los patrones **Strategy, Adapter, Factory, State, Observer, Decorator y Chain of Responsibility**, debido a que resuelven necesidades identificadas en el sistema y favorecen la separación de responsabilidades.

Se rechaza Singleton, debido a que introducir una instancia global podría generar acoplamiento, dificultar las pruebas unitarias y limitar la sustitución de dependencias.

## Consecuencias

- **Positivas:** mayor mantenibilidad, facilidad para incorporar nuevas políticas y proveedores, reutilización de componentes, mejor separación de responsabilidades y mayor facilidad para realizar pruebas unitarias.
- **Negativas/riesgos:** incremento en el número de clases e interfaces, mayor complejidad inicial y necesidad de mantener correctamente las relaciones entre patrones.