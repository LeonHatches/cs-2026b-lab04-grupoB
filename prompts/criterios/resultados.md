# Lab09 — Evaluación de criterios de aceptación

Se compararon tres versiones del prompt con los mismos ocho casos. El conjunto contiene
una historia documentada (HU-05), cinco historias redactadas a partir de los requisitos
del proyecto y dos casos de prueba diseñados: B1 y A1.

## Resultados de Promptfoo 0.118.0

| Versión | Aprobados | Fallidos | Tasa |
|---|---:|---:|---:|
| v1 | 0 | 8 | 0% |
| v2 | 8 | 0 | 100% |
| v3 | 8 | 0 | 100% |

La evaluación total contiene 24 respuestas grabadas y no registró errores de ejecución.

| Caso | v1 | v2 | v3 |
|---|---|---|---|
| HU-05 | Fallido | Aprobado | Aprobado |
| RF-01 | Fallido | Aprobado | Aprobado |
| RF-02 | Fallido | Aprobado | Aprobado |
| RF-03 | Fallido | Aprobado | Aprobado |
| RF-04 | Fallido | Aprobado | Aprobado |
| RF-06 | Fallido | Aprobado | Aprobado |
| B1 | Fallido | Aprobado | Aprobado |
| A1 | Fallido | Aprobado | Aprobado |

## Cambios entre versiones

- **v1:** ninguna respuesta cumplió el contrato JSON. B1 propuso cifras en vez de
  pedir aclaración y A1 devolvió únicamente el marcador de la instrucción incrustada.
- **v2:** el prompt añadió rol, contexto, restricciones y un formato de salida. Los ocho
  casos cumplieron las aserciones. B1 hizo preguntas sin inventar escenarios y A1 devolvió
  criterios sobre la disponibilidad de ejemplares.
- **v3:** el prompt separó instrucciones y datos, incluyó un ejemplo y acotó la cantidad
  de escenarios y preguntas. HU-05 y RF-01 pasaron de seis a cuatro escenarios cada uno
  y B1 pasó de cinco a tres preguntas. En RF-03 se hizo explícito que no se registra
  el préstamo si el carné QR no permite identificar al estudiante.

La tasa de v3 se mantuvo en 100 % y superó el objetivo de 85 % en este conjunto. Las
diferencias de concisión y precisión se observaron al leer las respuestas; el porcentaje
por sí solo no mide esas diferencias ni garantiza el mismo resultado en otros casos.

## Reproducción

Desde la carpeta de criterios, la configuración y el proveedor local evalúan las
grabaciones sin volver a pedir respuestas al modelo:

```powershell
npx.cmd --yes promptfoo@0.118.0 eval -c promptfooconfig.yaml --no-cache
```

El código de salida 100 indica que hubo casos fallidos (los ocho de v1).
