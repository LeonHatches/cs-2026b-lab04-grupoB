# E4 - Iteración 3 de ADD: seguridad (QA-05)

## 1. Revisar las entradas
Se revisan los drivers del Lab04, ADR-001, ADR-005 y el árbol de utilidad del Lab08.
Se conserva el monolito modular y el plazo de un mes.

## 2. Establecer el objetivo
QA-05 (H,M): impedir operaciones no autorizadas sobre multas y préstamos.
Medida: cero accesos indebidos en cien intentos.

## 3. Elegir el elemento a refinar
Se refina la autorización de operaciones administrativas en el backend.

## 4. Elegir conceptos de diseño
| Alternativa | Ventaja | Trade-off | Decisión |
|---|---|---|---|
| Control solo en frontend | Sencillo | El cliente puede falsificar roles | Rechazada |
| Autorización en backend | Control centralizado | Validación por operación | Seleccionada |
| Servicio externo de políticas | Gestión avanzada | Mayor complejidad | Rechazada para el MVP |

## 5. Instanciar elementos y responsabilidades
- Cliente web: solicita operaciones sin decidir permisos.
- Backend: obtiene el rol autenticado desde una fuente confiable.
- Autorizador: verifica permisos antes de modificar préstamos o multas.
- Dominio: ejecuta únicamente operaciones autorizadas.

## 6. Bosquejar vistas y registrar decisiones
Se mantiene el monolito modular. La decisión propuesta se documentará en ADR-008.
No se requieren nuevos contenedores para verificar permisos en el backend.

## 7. Analizar y verificar el objetivo
Se ejecutó fitness/seguridad.py como simulación didáctica.

| Indicador | Antes | Después |
|---|---:|---:|
| Intentos no autorizados | 100 | 100 |
| Accesos indebidos | 100 | 0 |

Se aprobaron cuatro pruebas de seguridad y 85 pruebas de la suite general.

**Trade-off:** la validación agrega procesamiento, pero evita confiar en roles declarados por el cliente.

**Limitación:** se simulan roles fijos; no se demuestra autenticación real ni seguridad del sistema desplegado.

**Conclusión:** se selecciona la autorización en backend. Se requieren pruebas de integración para validar su aplicación real.
