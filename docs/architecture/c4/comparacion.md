# E6 — Comparación Structurizr DSL vs C4-PlantUML manual

**E6 pendiente de completar después de exportar.** Registrar la comparación con C4-PlantUML manual a partir de las exportaciones y resultados reales.

| Criterio | Exportado de `workspace.dsl` | `contexto-manual.puml` | Conclusión comprobada |
|---|---|---|---|
| Fuente de verdad | Pendiente | Archivo independiente | Pendiente |
| Personas y externos | Pendiente | Pendiente | Pendiente |
| Relaciones y protocolos | Pendiente | Pendiente | Pendiente |
| Estilos y leyenda | Pendiente | Pendiente | Pendiente |
| Propagación de cambios | Pendiente | Pendiente | Pendiente |

Adjuntar evidencia de comandos validate/export y capturas de las cinco vistas.

## E4 — Secuencia UML y vista dinámica C4

La secuencia del Lab 05 detalla objetos y métodos, retornos, alternativas de error, reintento transaccional y notificación opcional.
La vista dinámica C4 resume en siete pasos el flujo exitoso entre estudiante, Web, componentes del backend, API académica y PostgreSQL.
Los controladores y repositorios del UML quedan abstraídos por Reservas, Catálogo y sus relaciones con la base de datos; se conserva la validación previa a la reserva atómica.
La secuencia sirve al desarrollador para implementar y probar cada caso; la dinámica sirve al equipo técnico para explicar la colaboración arquitectónica.
