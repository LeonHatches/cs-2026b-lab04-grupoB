# Lienzo de diseño · Sistema agéntico BiblioUNSA · Grupo B

| Decisión | Elección | Justificación |
|---|---|---|
| Agente o flujo | Agente acotado en exploración; flujo fijo en confirmación de reservas | Diagnosticar cambios requiere búsqueda; confirmar reservas necesita validaciones deterministas |
| Arquetipo | ReAct para ISSUE-01 | La lectura del issue y el resultado de pytest orientan la edición y la regresión |
| Herramientas | leer, listar, buscar, ejecutar pruebas, editar, diff y mapa_repo | Menor superficie de acción y contexto verificable |
| Memoria | Historial corto + notas.md | Registra hipótesis dentro de una ejecución sin almacenar datos personales |
| Coordinación | Un agente para issue 1 y 3; gestor/actor-crítico para issue 2 | Compara sencillez frente a separación de ejecución y revisión |
| Papel humano | Aprobador de edición; responsable final del PR | El agente no puede fusionar cambios ni usar credenciales |
| Control | Contrato JSON, sandbox, pruebas protegidas y máximo 12 pasos. Hasta dos rondas para la variante coordinada | Limita el alcance de las acciones y corta la ejecución cuando agota el presupuesto |

Los tres issues son fallos **sembrados exclusivamente en una copia** inspirada en los módulos de reservas, préstamos y multas de los Labs 05–07. No se afirma que estos fallos existan en la rama principal.

- ISSUE-01 se vincula a la [estrategia de multas](../../docs/design/patrones/strategy.puml) del Lab 07. Excluir domingos es una regla del ejercicio.
- ISSUE-02 se vincula a [HU-05](../../docs/design/historia.md) del Lab 05, que exige matrícula vigente para reservar.
- ISSUE-03 se vincula al [diagrama de estados del préstamo](../../docs/design/estados-prestamo.mmd) del Lab 05, donde `DEVUELTO` es un estado terminal.
