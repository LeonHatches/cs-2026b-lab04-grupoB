# ADR-010: Sistema agéntico acotado para BiblioUNSA

- **Estado:** Aceptado
- **Fecha:** 2026-11-16
- **Decisores:** León Hatches, Romina Camargo y Joaquín Quispe

## Contexto
Los Labs 04–09 documentaron arquitectura modular, diagramas UML/C4, patrones, tácticas de calidad y prompts con validación. El Lab 10 añade un agente de código seguro capaz de observar pruebas y proponer cambios a fallos sembrados sin modificar los artefactos previos.

## Alternativas
1. Flujo fijo sin LLM: simple y verificable, adecuado para validación de matrícula y reglas de negocio; menos flexible para localizar la causa de un fallo.
2. Agente único ReAct: menor coordinación y costo, útil para reparaciones acotadas.
3. Gestor con actor-crítico: separa ejecución y revisión, mejora vigilancia de seguridad, cuesta más pasos y contexto.

## Decisión
Adoptar ReAct con contrato estructurado y herramientas de mínimo privilegio en sandbox. El prototipo compara agente único con planificador, ejecutor y revisor (lector). Registro JSONL, diff, notas.md, AST y máximo 12 pasos por agente; un máximo de dos rondas de revisión. El humano controla la aprobación de ediciones y la fusión del PR.

## Consecuencias
- A favor: trazabilidad, pruebas objetivas, guardrails y reutilización de prácticas de Lab 07–09.
- Costos: más contexto en multiagente, mayor complejidad y revisión manual obligatoria.
- Riesgos: las decisiones grabadas de demostración no equivalen a una evaluación real del comportamiento de un LLM. La integración con un asistente y la revisión efectiva deben documentarse por separado.
