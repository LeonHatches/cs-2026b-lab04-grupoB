
# E7 — Auditoría de las cinco vistas C4 de BiblioUNSA

## Objetivo
Verificar la coherencia del modelo C4 con los Laboratorios 04 y 05, aplicando la lista de revisión sobre elementos, relaciones, títulos, tecnologías y alcance.

## Revisión del modelo

| Vista | Comprobación | Resultado | Evidencia |
|---|---|---|---|
| Contexto | Dos personas, sistema principal, dos sistemas externos y relaciones etiquetadas | Sí | workspace.dsl, vista Contexto y contexto.png |
| Contenedores | Tres contenedores con descripción y tecnología: Angular, Django y PostgreSQL | Sí | workspace.dsl y contenedores.png |
| Componentes | Seis módulos del backend, con responsabilidades y dependencias identificadas | Sí | workspace.dsl y componentes.png |
| Dinámica | Siete pasos numerados para la reserva de un ejemplar, incluyendo matrícula y disponibilidad | Sí | workspace.dsl y dinamica-exportada.png |
| Despliegue | Entorno Producción, nodos anidados e instancias de Web, API y base de datos | Sí | workspace.dsl y despliegue-exportado.png |

Los resultados anteriores se verificaron contra el modelo fuente.
Queda pendiente la revisión visual final de todas las imágenes
para confirmar legibilidad, leyendas y ausencia de etiquetas cortadas.

## Observaciones de la revisión con IA

### Hallazgo 1: protocolos internos

Propuesta de ChatGPT: exigir HTTPS en todas las relaciones entre componentes internos.

Verificación: Reservas, Catálogo, Préstamos, Multas, Usuarios e Integración académica son componentes del mismo backend Django. No se ha definido una comunicación de red entre cada par de módulos.

Decisión: rechazada como falso positivo. No corresponde inventar protocolos de red para llamadas internas de un monolito modular.

### Hallazgo 2: autenticación institucional

En el contexto exportado se indica HTTPS; en la relación de un componente con el sistema externo aparece "HTTPS (por verificar)".

Decisión: mantener como observación pendiente de confirmación con los ADR y la documentación institucional. No afirmar que el protocolo se verificó si no existe evidencia.

### Hallazgo 3: tecnologías del despliegue

El despliegue incluye navegador, Angular, Nginx, Django y PostgreSQL. Proveedor, sistema operativo, CPU, RAM y costo del servidor no están confirmados.

Decisión: conservar esos aspectos como decisiones pendientes y no representar el despliegue como infraestructura ya contratada.

## Conclusión

La revisión del código del modelo confirma las cinco vistas C4 y las relaciones principales de BiblioUNSA. Se identificó y refutó un falso positivo relativo a los protocolos de comunicación interna. Se mantiene pendiente la confirmación del protocolo institucional y la comprobación visual final de las imágenes.
