# E1 - Árbol de utilidad de BiblioUNSA

## Contexto y trazabilidad

Escenario de crecimiento: **«Todas las facultades y la biblioteca virtual; el
sistema académico no responde durante la matrícula».**

Base arquitectónica: [drivers del Lab04](../drivers.md), [ADR-001](../adr/001-estilo-arquitectonico.md)
y [ADR-003](../adr/003-integracion-academica.md). Se mantiene el monolito modular,
el MVP de un mes, tres desarrolladores, presupuesto bajo y acceso académico
exclusivamente mediante API.

Los códigos QA-01 a QA-07 identifican los escenarios del Lab08. Los escenarios
históricos del Lab04 mantienen su significado: QA-01 de seguridad e
interoperabilidad, QA-02 de unicidad de reserva y QA-03 de rendimiento con
200 usuarios y p95 <= 2 s. Los objetivos de esta iteración se evalúan por separado.

## Escenarios de seis partes y prioridades

H = alta, M = media, L = baja. La pareja es (importancia para el negocio,
dificultad técnica). Las cifras son objetivos de calidad. QA-03 y el tiempo de
recuperación de QA-04 se contrastan con la simulación de disponibilidad;
los objetivos de rendimiento, seguridad y modificabilidad se mantienen como
escenarios de diseño, sin atribuirles resultados de ese experimento.

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida objetivo | Prioridad y justificación |
|---|---|---|---|---|---|---|---|---|
| QA-01 | Rendimiento | Estudiantes de todas las facultades | Consultan catálogo y disponibilidad | Carga sintética de 12 solicitudes/s | Catálogo | Responder consultas | p95 <= 500 ms | (H,M): uso principal RF-01; requiere optimizar y medir |
| QA-02 | Rendimiento | Estudiantes | Solicitan reserva | Carga sintética de 6 solicitudes/s con API disponible | Reservas | Validar y responder sin duplicar reserva | p95 <= 1000 ms | (M,M): objetivo adicional; conserva la unicidad exigida por QA-02 del Lab04 |
| QA-03 | Disponibilidad | Sistema académico | Deja de responder | Matrícula, caída de 20 min; 1 solicitud/min | Integración académica y recepción de solicitudes | Conservar las solicitudes recibidas sin asumir matrícula vigente | 0 solicitudes perdidas de las 20 afectadas | (H,H): protege el trámite durante la falla central del caso; exige almacenamiento y reproceso |
| QA-04 | Disponibilidad | Sistema académico | Vuelve a responder | Retorno después de la caída de QA-03 | Trabajador de solicitudes conservadas | Revalidar matrícula y resolver la cola | Resolver 20 pendientes en <= 5 min | (H,M): sin recuperación el trámite queda detenido; depende de capacidad y del proveedor |
| QA-05 | Seguridad | Cliente sin rol autorizado | Intenta modificar multas o préstamos | Sesión institucional, cliente alterado | Autorización del backend | Rechazar operaciones no autorizadas | 0 accesos indebidos en 100 intentos | (H,M): protege operaciones de bibliotecario; control en servidor y pruebas negativas |
| QA-06 | Modificabilidad | Equipo de desarrollo | Incorpora una facultad | Evolución del MVP y biblioteca virtual | Configuración e integración institucional | Incorporar la facultad y ejecutar regresión | <= 1 jornada de 8 h, sin fallos en la suite | (M,M): reglas, permisos y regresión atraviesan varios módulos |
| QA-07 | Seguridad / interoperabilidad | Módulo de integración | Consulta matrícula de una facultad | Operación normal y recuperación tras caída | Puerto académico | Usar el contrato institucional de API | 100% consultas por API; 0 accesos a BD académica | (H,M): hace explícitos RF-05, R-04 y ADR-003; crítico en el nuevo alcance |

El árbol cubre rendimiento, disponibilidad, seguridad y modificabilidad. Disponibilidad, seguridad e
interoperabilidad tienen escenarios (H,H) o (H,M). La fiabilidad de la reserva
del Lab04 continúa como invariante: ninguna solicitud en espera equivale a una
reserva confirmada ni bloquea por sí sola un ejemplar.

## Justificación de prioridades

QA-03 tiene prioridad (H,H) porque la interrupción académica afecta directamente
la recepción y validación de solicitudes durante matrícula. QA-04 atiende la
recuperación del trámite, mientras QA-05 y QA-07 protegen la autorización y el
contrato de integración institucional.

QA-06 tiene prioridad (M,M): incorporar una facultad implica revisar contratos,
permisos y regresión en varios módulos con un equipo de tres personas. El
objetivo de ocho horas incluye esas actividades.

## Modelo y evidencia

- [Fuente Graphviz](arbol.dot) y [árbol renderizado](arbol.png).
- [Primera iteración ADD](../add/iteracion-1.md): prioriza QA-03 (H,H).
- Los 500 ms y 12 solicitudes/s de QA-01 no sustituyen los 2 s con 200 usuarios
  del Lab04: son cargas y objetivos diferentes, que requieren validación propia.
