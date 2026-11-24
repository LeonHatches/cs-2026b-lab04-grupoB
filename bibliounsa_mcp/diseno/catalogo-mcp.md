# Catálogo MCP del caso BiblioUNSA — E1

| Primitiva | Nombre | Entrada | Salida | Seguridad |
|---|---|---|---|---|
| Tool R | buscar_libro | texto: 2–80 caracteres | Lista JSON limitada a 20 | Solo lectura |
| Tool R | prestamos_vencidos | hoy: AAAA-MM-DD | ReporteVencidos estructurado | Solo lectura, sin identificador personal |
| Tool W | crear_reserva | usuario EST-001, libro_id LIB-001, matricula_vigente bool | Reserva nueva BORRADOR | Única escritura; creación exclusiva; permiso humano |
| Resource | bibliounsa://reglamento | — | Reglas de prueba | Solo consulta |
| Resource template | bibliounsa://adr/{numero} | 3 dígitos | ADR disponible | Rechazo de rutas arbitrarias |
| Prompt | aviso_vencimiento | prestamo_id | Plantilla de comunicación | No inventa datos |

El servidor es un adaptador de los servicios de BiblioUNSA. El dominio valida la matrícula
ficticia y la disponibilidad. La herramienta de escritura usa apertura exclusiva `x` para
crear cada borrador en `reservas_demo/` y conservar los registros existentes.
El host debe solicitar autorización humana antes de invocar la herramienta. Las
anotaciones del catálogo describen estas operaciones y orientan al host.
