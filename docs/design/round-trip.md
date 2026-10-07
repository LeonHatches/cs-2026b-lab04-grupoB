# E6 — Round-trip y diferencias esperadas / por comprobar
**Origen:** `clases.puml` (diseño) y `src/reservas/dominio.py` (esqueleto en Python). Para obtener evidencia de ingeniería inversa ejecutar los comandos del README; no se afirma que GitHub ya contiene el resultado.

| Diferencia al comparar | Causa | Acción |
|---|---|---|
| Las multiplicidades `1` y `0..*` del UML no se expresan explícitamente en Python | Las anotaciones de tipos no fijan cardinalidades del dominio | Mantener multiplicidades en PlantUML y validar invariantes en repositorios |
| Una agregación `Libro o-- Ejemplar` puede aparecer como atributo `list[Ejemplar]` | Pyreverse infiere relaciones a partir de atributos y no garantiza su semántica | Documentar la limitación y preservar el diagrama de diseño |
| Las interfaces UML pueden representarse como clases abstractas ABC | Python no tiene palabra clave `interface` | Verificar `ABC` y `@abstractmethod`; conservar estereotipo `<<puerto>>` |
| camelCase de UML pasa a snake_case de Python | Convenciones de estilo del lenguaje | Mantener tabla de correspondencias, p. ej. `validarVigente` → `validar_vigente` |
| Las transacciones/índice único de PostgreSQL no son inferibles desde clases | Reglas de concurrencia son infraestructura | Implementar migración y prueba de concurrencia antes de producción |

**Nota:** Son diferencias fundamentadas en cómo se representan estos conceptos; contrastar con la imagen realmente producida por pyreverse y ajustar la tabla si corresponde.
