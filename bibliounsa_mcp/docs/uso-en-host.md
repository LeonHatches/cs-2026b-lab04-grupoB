# E5 — Conexión con un host MCP real

## Hosts utilizados

Se configuró el servidor MCP BiblioUNSA mediante transporte `stdio`.

En VS Code se verificó el estado `Running` del servidor y el descubrimiento de tres herramientas.

También se utilizó Antigravity CLI 1.5.16 para realizar consultas reales mediante herramientas MCP. Para comprobar el prompt del servidor se utilizó MCP Inspector CLI.

## Cinco consultas desde Antigravity CLI

| N.º | Consulta en lenguaje natural | Herramienta | Resultado |
|---|---|---|---|
| 1 | Buscar el libro "Algoritmos". | `buscar_libro` | Se encontró `LIB-001`, "Algoritmos y estructuras de datos", con 3 ejemplares. |
| 2 | Consultar préstamos vencidos al 23/11/2026. | `prestamos_vencidos` | Se obtuvo 1 préstamo vencido: `P-001`. |
| 3 | Consultar préstamos vencidos usando la fecha "ayer". | `prestamos_vencidos` | El servidor rechazó la entrada: `Fecha inválida: use AAAA-MM-DD`. |
| 4 | Crear una reserva ficticia solicitando autorización previa. | `crear_reserva` | Tras la autorización expresa del usuario, el host informó la creación de `RES-0003`, con estado `BORRADOR`. |
| 5 | Buscar el libro "Bases de datos". | `buscar_libro` | Se encontró `LIB-003`, con 0 ejemplares disponibles. |

## Permisos y autorización

Las consultas de lectura se realizaron sin solicitar autorización adicional.

Antes de ejecutar `crear_reserva`, el agente mostró los parámetros propuestos: `usuario=EST-001`, `libro_id=LIB-001` y `matricula_vigente=true`.

La operación se ejecutó después de que el usuario respondiera afirmativamente. Este consentimiento fue solicitado mediante la conversación; no constituye por sí mismo una verificación de permisos obligatorios implementados por el host.

## Verificación del prompt MCP

Se comprobó `aviso_vencimiento` mediante MCP Inspector CLI utilizando `prompts/list` y `prompts/get`, con el argumento `prestamo_id=P-001`.

El servidor devolvió correctamente la plantilla para redactar un aviso de préstamo vencido, con indicaciones para consultar los préstamos antes de afirmar un atraso y no inventar información personal, fechas ni montos.

Antigravity no permitió invocar directamente el prompt mediante las capacidades disponibles en esa sesión. Por tanto, esta prueba se documenta como realizada desde MCP Inspector, no desde Antigravity.

## Observaciones

La consulta del recurso `bibliounsa://reglamento` mostró contenido en Antigravity, pero no se conservó una evidencia visible de la operación MCP de lectura del recurso. Por ello, no se considera una llamada verificada dentro de las cinco consultas.

Los registros utilizados son ficticios y corresponden al entorno académico del laboratorio.

## Resultado

Se realizaron cinco consultas mediante herramientas MCP desde Antigravity CLI, incluyendo búsquedas, consulta de préstamos, validación de errores y una operación de escritura autorizada.

Se verificó adicionalmente el prompt MCP mediante Inspector CLI. Las evidencias visuales se incorporaron al informe grupal.