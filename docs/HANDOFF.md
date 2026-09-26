# Handoff

Actualizado: 2026-09-26.

## Estado de cierre

El objetivo experimental vigente quedó resuelto para el alcance controlado de
v0.9: en esta tarea, `AGENTS.md` no mantuvo el equilibrio costo/rendimiento.
La evidencia no permite generalizar ese resultado fuera de Terra/medium,
sandbox read-only, el repositorio evaluado y el prompt controlado.

No hay una corrida pendiente obligatoria. No iniciar nuevas ejecuciones sin una
pregunta experimental nueva y autorización explícita.

## Configuración y evidencia

- Configuración actual: cohorte `gpt56`; productor y juez
  `gpt-5.6-terra`, esfuerzo `medium`, sandbox `read-only`.
- Experimento principal: `experiments/v0.9-agents-effect-controlled.json`.
- Prompt: `prompts/agents_effect_controlled.txt`.
- Resultados: `results/gpt56/gpt-5.6-terra/medium/v0.9-agents-effect-controlled/`.
- Resúmenes: `results/summary.md` y `results/summary.csv`.
- Intentos fallidos e históricos: `results/_attempts/` y
  `results/_archive/`; conservar separados.

## Cambios recientes

- `scripts/runner.py` usa UTF-8 para la entrada de prompts.
- `README.md` fue reducido a orientación de uso, resultados y enlaces.
- `AGENTS.md` contiene reglas permanentes para cohortes, resultados,
  seguridad de trazas y selección por roles.
- `docs/archivados/` concentra el material histórico y no guía decisiones.

## Próxima intervención

1. Revisar `git status --short` antes de modificar; el árbol contiene cambios
   deliberados sin commit.
2. Para cambios en scripts, ejecutar compilación estática; para cambios en
   definiciones, verificar referencias. Ejecutar dry-run solo con autorización.
3. Para una nueva cohorte, crear un nuevo identificador, prompt y definición;
   no modificar artefactos que ya tengan resultados.
4. Si se autoriza una corrida real, ejecutar primero
   `powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 doctor`
   en el mismo contexto de usuario y confirmar configuración, fuente y
   autenticación.
5. Regenerar resúmenes con `analyze` solo cuando esté autorizado; informar
   siempre condición, n, `exit_code`, métricas y limitaciones.

## Límites

`TRACE_JSON` es autodeclarado y no prueba exhaustividad. No editar resultados
crudos, resúmenes, prompts o configuraciones retrospectivamente para ajustar una
conclusión. No usar `git clean`, staging, commit, push, publicación ni borrados
sin autorización explícita.
