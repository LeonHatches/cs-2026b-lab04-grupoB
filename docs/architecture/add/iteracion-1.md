# E2 - Iteración 1 ADD: disponibilidad de la integración académica

## 1. Contexto y restricciones

Se revisaron [drivers.md](../drivers.md), [ADR-001](../adr/001-estilo-arquitectonico.md),
[ADR-003](../adr/003-integracion-academica.md), la secuencia de reserva del Lab05
y el [árbol de utilidad del Lab08](../utilidad/escenarios.md). Continúan vigentes:
MVP de un mes, tres desarrolladores, presupuesto bajo, monolito modular y acceso
al sistema académico solo por API. Se incorpora el contexto de todas las
facultades y biblioteca virtual con una caída durante matrícula.

## 2. Objetivo de la iteración

QA-03 del Lab08, **(H,H)**: cero solicitudes recibidas perdidas durante una caída
académica de veinte minutos, sin confirmar reservas sin matrícula validada.
Se relaciona con RF-02, RF-05 y la restricción R-04. Como criterio complementario,
QA-04 fija recuperar veinte solicitudes en no más de cinco minutos tras el retorno
de la API. Los IDs son locales del Lab08, distintos de los QA del Lab04.

## 3. Elemento refinado

La recepción de solicitudes en Reservas, el puerto de matrícula y su integración
académica. El catálogo y la confirmación atómica siguen protegiendo la unicidad
del ejemplar. Se conserva el despliegue del monolito modular del ADR-001.

## 4. Alternativas de diseño

| Concepto / táctica | Qué mejora | Trade-off y riesgo | Presupuesto / complejidad | Decisión |
|---|---|---|---|---|
| Reintentos acotados ante `TimeoutError` | Tolera fallas breves sin cambiar infraestructura | Una caída de 20 min supera los intentos; más llamadas pueden agravar la saturación | Bajo costo y complejidad; reutiliza el manejo del Lab07 | Complemento para fallos transitorios; no conserva por sí solo las solicitudes |
| Cola durable en PostgreSQL y procesamiento diferido | Conserva el trámite hasta poder validar matrícula | Más escrituras, trabajador, idempotencia y confirmación eventual; depende del almacenamiento | Complejidad media; usa la BD prevista sin añadir un servicio de pago | Seleccionada para contrastar conservación y recuperación |
| Circuit breaker | Reduce llamadas repetidas a una API caída | No guarda solicitudes por sí solo; umbrales erróneos retrasan la recuperación | Costo de infraestructura bajo; añade estados, umbrales y pruebas | Complemento a evaluar con datos de fallos; no se simula ni se atribuyen resultados aquí |
| Microservicios y broker externo | Aísla despliegues y permite consumidores independientes | Mayor operación, monitoreo y fallos distribuidos; no resuelve una caída del proveedor por sí solo | Costo y complejidad altos para tres personas y un mes | Rechazada para esta iteración: no hay evidencia que justifique cambiar ADR-001 |

No se asignan precios monetarios sin cotización. Reutilizar PostgreSQL evita
presuponer la contratación de otro servicio, pero consume capacidad y trabajo
del equipo; tampoco equivale a costo operativo cero.

## 5. Diseño y responsabilidades

El diseño registra duraderamente la solicitud con identificador único
y estado `PENDIENTE_VALIDACION`, y responde que se recibió el trámite. Un
trabajador consultará la matrícula por API cuando el proveedor se recupere.
`PENDIENTE_VALIDACION` significa **recibida, todavía no confirmada**; no equivale
a `RESERVADA`, no crea un préstamo ni garantiza disponibilidad del ejemplar.
Es un estado del trámite de integración de esta iteración, separado de los
estados de Reserva y Prestamo definidos en el Lab05.

Si la matrícula resulta vigente, se comprueba la disponibilidad actual y se
confirma mediante operación atómica; si no es vigente o ya no hay ejemplar,
se rechaza. Los reintentos deben ser idempotentes. Una outbox solo se justifica
si también hay que publicar eventos de forma transaccional; no se implementa
un broker ni una outbox de producción en esta simulación.

La simulación `fitness/disponibilidad.py` evalúa recepción y validación de
matrícula. Una respuesta `VALIDADA` solo expresa elegibilidad académica;
la disponibilidad del ejemplar y la confirmación atómica pertenecen al flujo
de reserva del Lab05. La persistencia en PostgreSQL es parte del diseño;
el experimento utiliza una cola en memoria.

## 6. Experimento y resultados

Condiciones de la simulación antes y después:

- Llegan 100 solicitudes: una al inicio de cada minuto, de 0 a 99.
- El proveedor falla en el intervalo `[30, 50)`: 20 minutos y 20 solicitudes afectadas.
- Fuera de la caída el proveedor responde y todas las matrículas simuladas son
  vigentes; no se modela latencia de red ni competencia por un mismo ejemplar.
- La variante con cola supone almacenamiento durable y disponible; el programa
  usa memoria, por lo que no demuestra supervivencia a reinicios ni fallas de BD.
- Un trabajador dispone de capacidad adicional para 5 pendientes/min; las nuevas
  solicitudes se atienden aparte. No hay fallas del trabajador ni del proveedor
  durante la recuperación. Al retornar la API en el minuto 50 se inicia el
  primer lote, que termina en el minuto 51; el último termina en el minuto 54.
- La simulación avanza en minutos discretos. La tasa de una solicitud/minuto
  es una carga sintética para aislar la conservación y recuperación del trámite;
  no estima la demanda de todas las facultades ni demuestra capacidad de producción.

Resultados de la simulación:

| Medida | Antes: sin cola | Después: cola modelada |
|---|---:|---:|
| Solicitudes totales | 100 | 100 |
| Duración de caída, minutos | 20 | 20 |
| Solicitudes afectadas | 20 | 20 |
| Matrículas validadas al final del experimento | 80 | 100 |
| Matrículas rechazadas en el caso base | 0 | 0 |
| Pendientes al restaurar la API | 0 | 20 |
| Pendientes recuperadas | 0 | 20 |
| Pendientes al final | 0 | 0 |
| Solicitudes perdidas | 20 | 0 |
| Tiempo de vaciado de cola | No aplica: se perdieron | 4 min |

Sin cola, las veinte solicitudes afectadas no se conservan para recuperación.
Las cien solicitudes del experimento no representan reservas confirmadas.

## 7. Cumplimiento y riesgos

En el modelo se cumple QA-03: se pasa de veinte pérdidas a cero. También se
cumple el criterio de recuperación de QA-04: 20 / 5 = 4 minutos, dentro de los
cinco minutos propuestos. Es evidencia sintética condicionada a los supuestos,
no una medición del sistema desplegado.

Las pruebas incluyen un control sin reproceso: conserva veinte pendientes y
solo ochenta solicitudes validadas. La recepción en cola no cuenta como éxito
final. Un segundo control responde con matrícula no vigente para dos de las
solicitudes en cola: se validan 98 matrículas y se rechazan dos, sin pérdidas.
La traza de respuestas comprueba que no se valida durante la caída y que
el reproceso comienza al volver la API, antes del fin de las llegadas.
Con capacidad de tres pendientes/min la recuperación tarda siete minutos
y **no cumple QA-04**, aunque no pierde solicitudes: la capacidad es un punto
de sensibilidad que puede invalidar el objetivo temporal.

Riesgos: caída de almacenamiento, saturación de la cola, duplicación de intentos,
API que no vuelve y ejemplares ocupados al validar. El diseño propone
persistencia transaccional, claves idempotentes, límites/alertas y nueva validación
atómica; estas defensas requieren pruebas de integración para demostrar
durabilidad, elegibilidad y unicidad reales. El trade-off de la decisión
es conservar solicitudes a cambio de demorar la confirmación.
