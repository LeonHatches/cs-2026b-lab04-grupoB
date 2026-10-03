# Drivers arquitectónicos — BiblioUNSA

## 1. Requisitos funcionales clave

| ID | Requisito | Actor | Prioridad |
|-------|----------------------------------------|-----------|-----------|
| RF-01 | Buscar libros por título, autor, categoría y disponibilidad | Estudiante | Alta |
| RF-02 | Reservar y cancelar un ejemplar disponible | Estudiante | Alta |
| RF-03 | Registrar préstamo mediante carné QR | Bibliotecario | Alta |
| RF-04 | Consultar y gestionar multas del estudiante | Estudiante / Bibliotecario | Media |
| RF-05 | Validar matrícula vigente mediante API del sistema académico | Sistema | Alta |
| RF-06 | Autenticar al usuario con cuenta institucional | Estudiante / Bibliotecario | Alta |

## 2. Atributos de calidad (ordenados por prioridad)

1. Seguridad e interoperabilidad — atributo crítico: identidad institucional e integración académica solo mediante API.
2. Fiabilidad - evitar dobles reservas y conservar la consistencia de préstamos y multas.
3. Rendimiento - catálogo y reservas deben responder de forma aceptable con usuarios concurrentes.
4. Mantenibilidad - las reglas de préstamos, multas e integraciones deben poder cambiar sin afectar todo el sistema.

## 3. Restricciones

| ID | Tipo | Restricción |
|------|--------------|-------------------------------------------------|
| R-01 | Plazo | MVP en producción en 1 mes. |
| R-02 | Equipo | 3 desarrolladores. Tecnologías conocidas: Python, JavaScript, Angular, Django, PostgreSQL y Git. |
| R-03 | Presupuesto | Bajo; justificar cualquier servicio de pago. |
| R-04 | Interoperabilidad | El sistema académico se consulta mediante API; sin acceso a su BD. |

## 4. Escenarios de atributos de calidad

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|-------|--------------|--------|----------|---------|-----------|-----------|------------|
| QA-01 | Seguridad / interoperabilidad | Estudiante | Inicia sesión y solicita reserva | Operación normal | Autenticación e integración | Valida cuenta y matrícula por API | 100% vía API; 0 accesos directos a la BD académica |
| QA-02 | Fiabilidad | 2 estudiantes | Reservan el mismo ejemplar casi simultáneamente | Alta demanda | Reservas | Confirma una sola reserva | 0 dobles reservas en 1000 intentos concurrentes |
| QA-03 | Rendimiento | 200 estudiantes | Consultan catálogo y disponibilidad | Carga concurrente | Catálogo | Devuelve resultados actualizados | p95 <= 2 s |