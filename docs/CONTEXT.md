# Contexto de continuidad

Actualizado: 2026-09-26.

## Estado actual

- Harness: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark`.
- Repositorio evaluado: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills`.
- Configuración vigente: cohorte `gpt56`; productor y juez `gpt-5.6-terra`,
  esfuerzo `medium`, sandbox `read-only`.
- Antes de una corrida real, ejecutar `doctor` en el mismo contexto de usuario.
  La última comprobación registrada en ese contexto confirmó Codex CLI y sesión
  autenticada; volver a verificar antes de consumir créditos.

## Evidencia vigente

- `v0.9-agents-effect-controlled`: cinco repeticiones por condición, diez
  productores y diez jueces con `exit_code=0`. Las trazas cumplieron
  `deep_research_used=false`, `external_sources_count=0` y
  `primary_sources_count=0`.
- En v0.9, sin AGENTS (A): 205616 tokens promedio, 51.5 s, Q=10.20; con AGENTS
  (B): 329825 tokens, 69.8 s, Q=9.80. Medianas: A 174279 tokens, 42.0 s, Q=10;
  B 305312 tokens, 71.1 s, Q=10.
- Conclusión acotada: para esta tarea, repositorio, Terra/medium y sandbox
  read-only, AGENTS no mejoró calidad y aumentó tokens y tiempo. No generalizar.
- v0.5 sigue siendo exploratoria: A05 es atípica y B02 activó deep research.
  No usarla para afirmar ahorro causal de AGENTS.
- v0.8 comparó esfuerzos Terra de modo descriptivo; medium fue la referencia
  operativa configurada, no una superioridad universal.

## Cambios persistentes de la sesión

- `scripts/runner.py` envía prompts con `encoding='utf-8'`; la corrección
  pasó compilación estática y las corridas posteriores registradas.
- `README.md` quedó orientado a uso básico, resultados vigentes y documentación
  histórica bajo `docs/archivados/`.
- `AGENTS.md` separa documentación vigente e histórica, protege cohortes y
  resultados derivados, y define los roles Ejecutor/Luna, Analista/Tierra y
  Arquitecto/Sol.
- Los documentos históricos canónicos están en `docs/archivados/` y no deben
  usarse para decisiones operativas.

## Artefactos clave

- Definiciones: `experiments/v0.8-terra-low.json`,
  `experiments/v0.8-terra-high.json`,
  `experiments/v0.9-agents-effect-controlled.json`.
- Prompt controlado: `prompts/agents_effect_controlled.txt`.
- Evidencia agregada: `results/summary.md` y `results/summary.csv`.
- Resultados v0.9: `results/gpt56/gpt-5.6-terra/medium/v0.9-agents-effect-controlled/`.

## Límites

No ejecutar nuevas corridas, `doctor`, dry-runs ni `analyze` sin autorización
explícita: los comandos pueden consultar estado externo o escribir artefactos.
No editar manualmente resultados, resúmenes ni definiciones de cohortes ya
ejecutadas.
