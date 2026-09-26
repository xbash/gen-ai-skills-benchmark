# gen-ai-skills benchmark harness

Harness para ejecutar, conservar y analizar experimentos reproducibles sobre carga de contexto e instrucciones para agentes. Las definiciones de experimentos están en `experiments/`; los prompts y variantes controladas, en `prompts/` y `fixtures/`.

## Qué hace

- Ejecuta corridas declarativas sobre una copia temporal del repositorio fuente.
- Conserva JSONL crudo, metadatos, respuesta final y `TRACE_JSON` declarado por el agente.
- Evalúa calidad con `Q` mediante `scripts/judge.py`.
- Genera resúmenes CSV y Markdown con `scripts/analyze.py`.
- Mantiene separados resultados activos, intentos fallidos y preparaciones dry-run.

## Requisitos y configuración

- Windows 10/11.
- Python 3.10 o posterior.
- Codex CLI instalado y autenticado.
- PowerShell 5.1 o posterior.
- Repositorio fuente disponible localmente.

Revisa `benchmark.config.json` antes de ejecutar. Allí se definen `source_repo`, modelo, esfuerzo, sandbox, tiempos de espera y configuración del juez. Ejecuta `doctor` en el mismo contexto de usuario que usarás para la corrida.

## Uso básico

Desde la raíz del proyecto:

```powershell
.\run.ps1 doctor
.\run.ps1 list
.\run.ps1 run <experimento> -DryRun
```

Reemplaza `<experimento>` por un nombre mostrado por `list`. El dry-run prepara artefactos sin ejecutar una corrida productora.

Para una corrida real, juzgar y analizar:

```powershell
.\run.ps1 run <experimento>
.\run.ps1 judge <experimento>
.\run.ps1 analyze
```

Las corridas reales crean evidencia y pueden consumir recursos. Usa `-Resume` solo para continuar un experimento preservando resultados exitosos; los intentos fallidos se archivan en `results/_attempts/`. `-Limit` restringe la cantidad de corridas nuevas. No uses `run all` como flujo normal: ejecuta únicamente el experimento autorizado.

En Windows también puedes invocar `run.cmd`, que delega en `run.ps1`.

## Experimentos y resultados

Cada archivo JSON de `experiments/` declara condiciones, repeticiones, workspace, variante de instrucciones y prompt. Consulta esa carpeta y `run.ps1 list` para el catálogo vigente; el README no duplica la descripción histórica de cada cohorte.

Los resultados agregados se regeneran en:

- `results/summary.md`
- `results/summary.csv`

Los artefactos individuales están bajo `results/`. No edites manualmente resultados crudos ni reutilices un `meta.json` existente.

## Métricas y límites

El análisis conserva, cuando Codex los informa:

- `input_tokens`, `cached_input_tokens`, `output_tokens` y `reasoning_output_tokens`;
- tiempo de pared y `exit_code`;
- `total_reported_tokens = input_tokens + output_tokens`;
- `uncached_input_tokens = input_tokens - cached_input_tokens`;
- `Q`, de 0 a 12, y `E_Q`, indicador interno de eficiencia de calidad.

Las medias de cohortes pequeñas son descriptivas y no prueban causalidad ni ahorro generalizable. `TRACE_JSON` es autodeclarado y no constituye un registro exhaustivo de todos los archivos leídos o acciones realizadas.

## Documentación

- [Rúbrica de calidad](docs/RUBRIC.md)
- [Contexto de continuidad](docs/CONTEXT.md)
- [Decisiones vigentes](docs/DECISIONS.md)
- [Handoff de reanudación](docs/HANDOFF.md)
- [Protocolo de reanudación](docs/PROTOCOLO_REANUDACION.md)
- [Resultados agregados](results/summary.md)
- [Instrucciones para agentes](AGENTS.md)

## Reproducibilidad y seguridad operativa

El runner trabaja sobre copias temporales y usa el sandbox configurado en `benchmark.config.json`; el repositorio fuente no debe modificarse durante una corrida. Antes de ejecutar, valida el repositorio, archivos requeridos, modelo y autenticación con `doctor`. Conserva las condiciones comparables: tarea, prompt, modelo, esfuerzo, sandbox y procedimiento.

Consulta [LICENSE](LICENSE) para los términos de uso.
