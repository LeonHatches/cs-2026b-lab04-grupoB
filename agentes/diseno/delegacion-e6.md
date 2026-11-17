# E6 — Delegación progresiva y control humano
## BiblioUNSA — Laboratorio 10

### 1. Humano ejecutor
La persona realiza las operaciones directamente. El agente propone acciones y ofrece información, pero no modifica archivos por sí mismo.

### 2. Humano revisor
El agente inspecciona código y ejecuta pruebas. Antes de editar, solicita autorización explícita. Este es el nivel utilizado en la ejecución interactiva de E6.

### 3. Humano colaborador
El agente podría ejecutar tareas acotadas de bajo riesgo, con supervisión periódica. Este nivel no fue habilitado en la práctica.

### 4. Humano gobernador
La persona define políticas, permisos, límites y métricas de supervisión. Una mayor autonomía requeriría evaluaciones adicionales. Este nivel tampoco fue habilitado.

## Evidencia experimental
- Aprobación con "s": edición autorizada y dos pruebas aprobadas.
- Rechazo con "n": acción bloqueada y código intacto.
- Pruebas automatizadas del framework: 17 aprobadas.
- Las ejecuciones utilizaron copias temporales aisladas.

## Controles
Se restringieron las ediciones a src/*.py, se protegieron las pruebas y se aplicaron permisos por rol, sandbox y límites de pasos. No se concedieron permisos para fusionar PR ni acceder a credenciales reales.

## Conclusión
El nivel de humano revisor permitió controlar las modificaciones y verificar que el agente respetara las decisiones de autorización y rechazo.
