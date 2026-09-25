# AGENTS.md

## Propósito
Este archivo es el punto de entrada operacional de `gen-ai-skills`. Orienta al agente hacia el contexto mínimo necesario para cada tarea. No cargues automáticamente todas las skills, documentación, ejemplos, templates o checklists.

## Principios operacionales
1. Identifica objetivo y dominio.
2. Carga solo el contexto necesario.
3. Prefiere una skill específica antes que múltiples skills generales.
4. Consulta auxiliares solo cuando aporten valor.
5. No inventes ejecuciones, resultados, métricas, compatibilidades ni evidencia.
6. Distingue hechos, supuestos, inferencias, recomendaciones y datos pendientes cuando sea relevante.
7. Prefiere cambios pequeños, verificables y reversibles.
8. Evita duplicar contexto consolidado.
9. Preserva trazabilidad y reproducibilidad.

## Descubrimiento de contexto
1. Clasifica la solicitud.
2. Identifica el dominio relevante dentro de `skills/`.
3. Selecciona la skill mínima suficiente.
4. Si es simple, lee su `.md`; si es compuesta, comienza por `SKILL.md`.
5. Lee `README.md`, `CHECKLIST.md`, `TEMPLATE.md` o `EXAMPLES.md` solo si son necesarios.

## Eficiencia
Maximiza valor útil por contexto, tiempo y costo; no minimices tokens de forma absoluta.

## Routing recomendado
Cuando una tarea requiera investigación profunda, búsqueda y contraste de fuentes, revisión del estado del arte o verificación sistemática de afirmaciones, utiliza `skills/academia/deep-research/SKILL.md`.
No la cargues para consultas simples, inspección local del repositorio o tareas que no requieran investigación externa.
