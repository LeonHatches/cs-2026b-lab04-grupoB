# E1 — Inventario C4 de BiblioUNSA (borrador por verificar)

| Elemento | Tipo C4 | Origen | Validación |
|---|---|---|---|
| Estudiante | Persona | Lab 04, drivers.md | Confirmar |
| Bibliotecario | Persona | Lab 04, drivers.md | Confirmar |
| BiblioUNSA | Software system | Lab 04, arquitectura.mmd | Confirmar |
| Sistema académico UNSA | Sistema externo | ADR-003 | Confirmar |
| Identidad institucional | Sistema externo | Lab 04, arquitectura.mmd | Confirmar |
| Interfaz web | Contenedor | Lab 04, arquitectura.mmd (frontend) | Confirmar tecnología específica |
| Aplicación backend / API | Contenedor | ADR-001, monolito modular | Confirmar tecnología específica |
| PostgreSQL | Contenedor de base de datos | ADR-002 | Confirmar |
| Usuarios y autenticación | Componente de API | Lab 05, paquetes.puml | Confirmar |
| Catálogo | Componente de API | Lab 05, paquetes.puml | Confirmar |
| Reservas | Componente de API | Lab 05, paquetes.puml | Confirmar |
| Préstamos | Componente de API | Lab 05, paquetes.puml | Confirmar |
| Multas | Componente de API | Lab 05, paquetes.puml | Confirmar |
| Integración académica | Componente de API | Lab 05, paquetes.puml | Confirmar |

**Pendientes importantes:** decidir si corresponde modelar un servicio de correo como tercer sistema externo y/o una tarea programada de multas como cuarto contenedor. La guía los menciona como posibilidades, no evidencia de que ya se implementaron.
