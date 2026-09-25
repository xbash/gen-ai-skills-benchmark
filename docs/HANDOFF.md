# Handoff

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
