# Bitácora de IA — Hatches — Lab 05

Fecha de la revisión: 10/10/2026 (America/Lima).
Responsable: Hatches Curo, José León Enrique. Alcance: E1 y E5.
Herramienta: Codex (asistente de OpenAI).

Este archivo documenta la revisión realizada en esta conversación. Se mantiene como aporte individual para que el responsable de E7 pueda enlazarlo o integrarlo en la bitácora general, que tiene cambios en la rama de Joaquín.

## Solicitud del integrante (resumen)

Revisar la guía y el repositorio, corregir aspectos de la parte estructural que no alteren los contratos usados por otros integrantes, crear una rama y commits locales con prefijo lab05, sin hacer push. El integrante generará después las imágenes y continuará con el PR.

| Elemento | Hallazgo o propuesta de IA | Verificación realizada | Decisión y cambio |
|---|---|---|---|
| E1: historia, criterio 3 | El criterio permitía confirmar una reserva de un ejemplar ya reservado o prestado. | Se contrastó con el criterio 1 y la regla de una sola reserva activa: la carrera entre solicitudes debe partir de un ejemplar disponible. | Corregir la precondición del criterio 3 y agregar el criterio 5 para rechazar solicitudes de ejemplares ocupados. Se conserva la numeración de los criterios anteriores. |
| E1: clases | Las tres enumeraciones estaban escritas en una sola línea con valores separados por punto y coma. | Se compararon nombres, orden y valores antes y después del ajuste. | Escribir cada valor en su propia línea; conservar clases, métodos, relaciones y valores. La validación visual en PlantUML queda pendiente. |
| E5: paquetes | ADR-001 agrupa Autenticación/Integración, pero el diagrama muestra dos paquetes separados y uno compartido. | Se leyó ADR-001 y se comprobaron las dependencias del diagrama mediante un recorrido del grafo; no se encontraron ciclos. | Agregar una nota que explique el detalle del módulo y la función de compartido, conservando todas las dependencias. |

## Evidencias pendientes del integrante

- Renderizar clases.puml y paquetes.puml, comprobar legibilidad y guardar las imágenes en docs/design/img/.
- Capturar esta revisión para la evidencia de IA del informe y compartir este registro con el responsable de E7.
- Agregar las imágenes en un commit posterior, publicar la rama cuando se decida y abrir el PR.
- Obtener revisión de otro integrante y revisar un PR ajeno.

No se declara validación visual, aprobación de compañeros, push ni PR realizados en esta revisión.
