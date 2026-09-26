# Handoff

> **Estado vigente al 2026-09-26.** Leer esta seccion antes del contenido
> historico posterior.

## Objetivo resuelto en el alcance v0.9

Para la tarea controlada del harness, `AGENTS.md` no mantuvo el equilibrio:
con Terra/medium y sin fuentes externas aumento el costo y el tiempo, sin
mejorar Q. Esta conclusion es local a v0.9; v0.5 queda como evidencia
exploratoria confun­dida por outliers y deep research.

## Punto exacto de reanudacion

`v0.9-agents-effect-controlled` ya fue ejecutado, juzgado y analizado. Para
revisar la evidencia agregada:

```powershell
$bench = 'C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark'
Set-Location $bench
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 doctor
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 analyze
```

Si una corrida falla, no sobrescribirla: inspeccionar `meta.json`, `stderr.txt`
y `codex.jsonl`; usar `--resume` solo despues de decidir conservarla en
`results/_attempts/` conforme al comportamiento del runner.

## Condiciones y criterios v0.9

- Productor y juez: `gpt-5.6-terra`, esfuerzo `medium`; sandbox `read-only`.
- Cinco repeticiones `A_NO_AGENTS` (`agents=none`) y cinco
  `B_WITH_AGENTS` (`agents=routed`), con el mismo prompt/workspace.
- El prompt exige solo evidencia local y `external_sources_count=0`,
  `primary_sources_count=0`, `deep_research_used=false`.
- Verificacion realizada: diez `meta.json` con `exit_code=0` y diez `trace.json`
  sin deep research ni fuentes externas.
- Reportar por condicion: n, fallidas, tokens de entrada/cacheados/salida,
  tokens totales, tiempo, Q, mediana, dispersion y artefactos atipicos. No
  atribuir causalidad ni generalizar fuera de esta tarea si la variabilidad o
  las trazas rompen comparabilidad.

## Cambios y resguardos vigentes

- `benchmark.config.json` quedo en Terra/medium para productor y juez.
- `scripts/runner.py` fija la codificacion UTF-8 al enviar prompts a Codex.
- `v0.5` Terra esta completo y juzgado; su primer fallo UTF-8 fue archivado.
- `v0.8` Terra low/high y v0.9 son experimentos nuevos; no eliminar ni
  sobrescribir resultados, `results/_attempts/`, `results/_archive/` ni
  `output/dry-run/`.
- No usar `git clean`, staging, commit o push sin autorizacion explicita.

## Registro historico previo (no usar para el estado actual)

Fecha de corte: 2026-09-25.

## Estado al reanudar

- `v0.6` está completo: cuatro productores, juez y análisis.
- El entorno fue reparado y validado por `doctor`, dry-run y smoke real limpio.
- El piloto `v0.7` está completo: dos corridas Luna/medium y dos Terra/medium,
  todas `A_NO_AGENTS` y exitosas.
- La configuración activa fue restaurada a `gpt56`, `gpt-5.6-luna/medium`.
- Ninguna corrida `v0.7` tiene juez o análisis agregado todavía.

## Próxima decisión

Revisar los artefactos `v0.7` y decidir si se necesita una Q comparable:

1. Leer `meta.json`, `stderr.txt`, `final.txt`, `trace.json` y tokens de ambas cohortes.
2. Si se necesita Q, ejecutar el mismo juez para las corridas `v0.7` y comparar descriptivamente.
3. Elegir Luna o Terra antes de iniciar la evaluación causal de `AGENTS.md`.
4. Mantener `high` fuera del alcance hasta formular una pregunta separada sobre esfuerzo.

No mezclar `v0.6` con `v0.7` en una conclusión de modelo. No ejecutar una nueva
cohorte causal ni `high` sin autorización explícita.

## Artefactos de reanudación

- `benchmark.config.json`
- `experiments/v0.7-luna-medium-pilot.json`
- `experiments/v0.7-terra-medium-pilot.json`
- `results/gpt56/gpt-5.6-luna/medium/v0.7-luna-medium-pilot/`
- `results/gpt56-terra/gpt-5.6-terra/medium/v0.7-terra-medium-pilot/`

## Comandos de orientación

```powershell
$bench = 'C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark'
Set-Location $bench
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 doctor
powershell.exe -ExecutionPolicy Bypass -NoProfile -File .\run.ps1 list
```

## Estado de limpieza y control de cambios

La limpieza de residuos fue completada el 2026-09-25. Se eliminaron
`.workspaces/`, `scripts/__pycache__/`, `output/playwright/`,
`VALIDATION.txt` y `fixtures/routing-snippet.md`. No eliminar
`output/dry-run/`, `results/_attempts/`, `results/_archive/`,
`fixtures/legacy/deep-research/SKILL.md` ni `docs/RUBRIC.md` sin una nueva
decision explicita: son evidencia de preparacion, historial o documentacion
legible.

Antes de cualquier cambio adicional, confirmar el estado Git con:

```powershell
$bench = 'C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark'
git -c safe.directory=$bench -C $bench status --short
git -c safe.directory=$bench -C $bench ls-files
```

Solo `LICENSE` estaba versionado en el corte de esta sesion. No usar
`git clean`; los demas archivos del harness aparecen como no versionados.
