# Observación de trazas · BiblioUNSA Lab 10

## Métricas por issue

| Issue / configuración | Pasos | Rondas | Herramientas usadas | Decisiones rechazadas por contrato | Acciones bloqueadas | Contexto final (caracteres) |
|---|---:|---:|---|---:|---:|---:|
| ISSUE-01 | 6 | 6 | `leer_archivo`, `ejecutar_pruebas`, `editar_archivo` | 0 | 0 | 2906 |
| ISSUE-02 · Agente único | 4 | 4 | `ejecutar_pruebas`, `editar_archivo` | 0 | 0 | 1310 |
| ISSUE-02 · Multiagente | 8 | 8 | `ejecutar_pruebas`, `editar_archivo`, `ver_cambios` | 0 | 0 | 2512 |
| ISSUE-03 | 10 | 10 | `leer_archivo`, `ejecutar_pruebas`, `editar_archivo`, `ver_cambios` | 0 | 0 | 4405 |

## Diagrama de trayectoria: ISSUE-01

```mermaid
flowchart TD
    inicio["ISSUE-01"]
    inicio --> e6["Paso 1 · OBSERVANDO · leer_archivo"]
    e6 --> e11["Paso 2 · OBSERVANDO · ejecutar_pruebas"]
    e11 --> e16["Paso 3 · OBSERVANDO · leer_archivo"]
    e16 --> e21["Paso 4 · OBSERVANDO · editar_archivo"]
    e21 --> e26["Paso 5 · OBSERVANDO · ejecutar_pruebas"]
    e26 --> e29["Paso 6 · FINALIZADO"]
```