# Contexto de continuidad

> **Estado vigente al 2026-09-26.** Esta seccion es canonica para reanudar. El
> contenido posterior describe el corte historico 2026-09-25 y no debe
> prevalecer sobre esta actualizacion.

## Actualizacion 2026-09-26

- Harness: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark`.
  Repositorio evaluado: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills`.
- Configuracion vigente: cohorte `gpt56`, productor y juez `gpt-5.6-terra`,
  esfuerzo `medium`, sandbox `read-only`.
- El comando de prechequeo que paso en el contexto correcto fue
  `powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 doctor`;
  confirmo `codex-cli 0.157.0` y sesion ChatGPT autenticada. El contexto no
  elevado habia reportado `Not logged in`; no mezclar ambos contextos.

### Evidencia nueva

- Seleccion de modelo/esfuerzo: con la misma tarea `A_NO_AGENTS`, Terra/medium
  tuvo `n=2`, Q promedio `12.00`, 191301 tokens y 54.7 s. Luna/medium tuvo
  `n=3`, Q promedio `11.00`, 302742 tokens y 74.5 s. Es evidencia descriptiva.
- Terra por esfuerzo: low (`n=2`, Q `9.50`, 115694 tokens, 32.2 s), medium
  (`n=2`, Q `12.00`, 191301 tokens, 54.7 s) y high (`n=2`, Q `10.00`, 195985
  tokens, 66.5 s). Terra/medium quedo como referencia; no es una conclusion
  generalizable.
- `v0.5` con Terra/medium completo: A sin AGENTS (`n=5`, 451489 tokens, 93.1 s,
  Q `11.20`) y B con AGENTS (`n=5`, 447691 tokens, 77.2 s, Q `11.40`). La
  revision individual muestra que A05 (974130 tokens, 209.9 s) domina la media;
  las medianas fueron A=292903 tokens/63.7 s/Q11 y B=419937 tokens/76.3 s/Q12.
  B02 activo `deep_research_used=true`. Esta cohorte no prueba ahorro causal.
- El primer productor Terra de `v0.5` fallo por entrada no UTF-8; se archivo en
  `results/_attempts/v0.5/`. `scripts/runner.py` ahora usa
  `encoding='utf-8'` en `subprocess.run`; `py_compile`, reanudacion y las diez
  corridas posteriores pasaron con `exit_code=0`.
- `v0.9-agents-effect-controlled` completo: cinco repeticiones por condicion,
  diez productores y diez jueces validos, todos `exit_code=0`. Todas las
  trazas cumplieron `deep_research_used=false`, `external_sources_count=0` y
  `primary_sources_count=0`. A sin AGENTS: 205616 tokens promedio, 51.5 s,
  Q=10.20; B con AGENTS: 329825 tokens, 69.8 s, Q=9.80. Medianas: A
  174279 tokens/42.0 s/Q10; B 305312 tokens/71.1 s/Q10.

### Artefactos de esta sesion

- `benchmark.config.json`, `scripts/runner.py`.
- `experiments/v0.8-terra-low.json`, `experiments/v0.8-terra-high.json`,
  `experiments/v0.9-agents-effect-controlled.json`.
- `prompts/agents_effect_controlled.txt`.
- `results/summary.md`, `results/summary.csv`, `results/gpt56/gpt-5.6-terra/`.

## Registro historico previo (no usar para el estado actual)

Fecha de corte: 2026-09-25.

## Propósito y rutas

- Harness: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark`
- Repositorio evaluado: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills`
- Configuración activa: cohorte `gpt56`, `gpt-5.6-luna`, esfuerzo `medium`, sandbox `read-only`.
- Usar el contexto elevado: `doctor` confirmó autenticación ChatGPT y `codex-cli 0.157.0`.

## Evidencia disponible

### v0.6 (exploratoria; entorno con advertencias)

Productor, juez y análisis completados: dos repeticiones por condición.

| Condición | n | Tokens entrada prom. | Tiempo prom. | Q prom. |
|---|---:|---:|---:|---:|
| `A_NO_AGENTS` | 2 | 350863 | 81.7 s | 11.00 |
| `B_WITH_AGENTS` | 2 | 229223 | 59.3 s | 11.50 |

Todos los productores terminaron con `exit_code=0`, `gpt-5.6-luna/medium`.
Es evidencia descriptiva, no causal ni generalizable: durante esa cohorte hubo
errores de skills globales y avisos de plugins.

### v0.6-clean-smoke (entorno reparado)

`A_NO_AGENTS-01` terminó con `exit_code=0`, `gpt-5.6-luna/medium`.

- 71.23 s; input 288490; cacheado 249856; output 4323; razonamiento 1243.
- No hubo errores de frontmatter, cache de modelos ni hooks.
- Persistieron avisos de íconos de paquetes de primera parte y snapshot de PowerShell.

No usar este smoke para una conclusión de calidad o comparación de modelos:
tiene una sola repetición y una sola condición.

### Piloto de selección de modelo (v0.7)

Se completaron corridas limpias `A_NO_AGENTS` con el mismo prompt/workspace y
esfuerzo `medium`:

| Cohorte | n | Input promedio | Cacheado promedio | Tiempo promedio |
|---|---:|---:|---:|---:|
| `gpt56` Luna | 2* | 291179 | 249344 | 73.59 s |
| `gpt56-terra` Terra | 2 | 187977 | 134016 | 54.65 s |

`*` Luna combina `v0.6-clean-smoke` y `v0.7-luna-medium-pilot`, ambos posteriores
a la reparación. Terra corresponde a `v0.7-terra-medium-pilot`. Ninguna de estas
corridas tiene juez todavía; la comparación es solo operacional y descriptiva.

## Estado del entorno

Se retiró el BOM UTF-8 de las skills globales `revisar-codigo-dev` y
`usar-reglas-dev`; sus copias son `SKILL.md.bak-20260925-031344`.

Se apartó la cache anterior de modelos y Codex la regeneró. El error
`missing field base_instructions` no reapareció.

No editar manualmente `C:\Users\xbash\.codex\plugins\cache`: los avisos de
íconos con `..` pertenecen a paquetes de primera parte. El snapshot de
PowerShell es una limitación residual, no una falla del harness.

## Artefactos clave

- `benchmark.config.json`
- `experiments/v0.6.json`
- `experiments/v0.6-clean-smoke.json`
- `prompts/evaluation_progressive_loading.txt`
- `results/summary.md` y `results/summary.csv`
- `results/gpt56/gpt-5.6-luna/medium/v0.6/`
- `results/gpt56/gpt-5.6-luna/medium/v0.6-clean-smoke/`
- `results/gpt56/gpt-5.6-luna/medium/v0.7-luna-medium-pilot/`
- `results/gpt56-terra/gpt-5.6-terra/medium/v0.7-terra-medium-pilot/`

## Limpieza de artefactos (2026-09-25)

Se eliminaron solo residuos verificados: `.workspaces/` (4.118 archivos,
23.815.688 bytes), `scripts/__pycache__/`, `output/playwright/`,
`VALIDATION.txt` y `fixtures/routing-snippet.md`. Las eliminaciones fueron
permanentes y no tienen recuperacion por Git: solo `LICENSE` esta versionado
en el checkout actual.

Se conservaron `output/dry-run/`, `results/_attempts/` y
`results/_archive/` porque documentan preparaciones, fallos y cohortes
historicas separadas. Tambien se conservaron
`fixtures/legacy/deep-research/SKILL.md` como referencia historica y
`docs/RUBRIC.md` como contrato legible de la Q. Ninguno de esos dos ultimos
archivos es consumido por el runner.
