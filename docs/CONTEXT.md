# Contexto de continuidad

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
