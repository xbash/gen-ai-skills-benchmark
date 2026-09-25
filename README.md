# gen-ai-skills benchmark harness

Automatización reproducible de los experimentos `v0.1` a `v0.5` de `gen-ai-skills-v0.2`.

## Continuación personal (2026-09-07)

El cierre práctico ahora incluye un piloto de recuperación de contexto al retomar proyectos. Consulta [docs/PROTOCOLO_REANUDACION.md](docs/PROTOCOLO_REANUDACION.md) para el diseño, la rúbrica, las limitaciones y la regla de decisión. El candidato de instrucciones está en [fixtures/AGENTS.resume.md](fixtures/AGENTS.resume.md).

`python scripts/runner.py run resume-pilot` ejecuta cuatro corridas locales en orden ABBA. No usa la rúbrica de investigación de `judge.py`. `run all` también incluye este piloto. Los identificadores de resultados se reutilizan: archiva los resultados antes de repetir un experimento.

Las preparaciones `--dry-run` se guardan separadamente en `output/dry-run/`, con copias en `.workspaces/dry-run/`. Una corrida real con `meta.json` existente se rechaza para preservar sus resultados. El lanzador PowerShell propaga el código de salida de Python.

Para continuar sin repetir corridas exitosas: `python scripts/runner.py run v0.4 --resume` (también para v0.5). `--limit 1` limita a una corrida nueva por experimento. `--resume` omite corridas exitosas y mueve intentos fallidos a `results/_attempts/` antes de repetir el mismo ID. v0.4 y v0.5 se detienen ante el primer fallo.

En este entorno Windows se verificó que la sesión ChatGPT era visible fuera del sandbox del proceso controlador, pero no dentro. Si tu terminal muestra `Logged in using ChatGPT` y el controlador muestra `Not logged in`, verificar el mismo comando con permisos de usuario antes de repetir el login. El agente ejecutado conserva `--sandbox read-only`.

## Qué automatiza
- v0.1: reconocimiento de `AGENTS.md`, routing, control negativo y activación explícita de `deep-research`.
- v0.2: overhead A/B/C (vacío / solo AGENTS / framework completo).
- v0.3: estabilidad del routing R1/R2/R3.
- v0.3.1: cinco repeticiones adicionales de R3.
- v0.4: valor de la skill `deep-research` (baseline vs skill explícita).
- v0.5: efecto causal de `AGENTS.md` (mismo framework sin/con AGENTS).

## Requisitos
- Windows 10/11.
- Python 3.10+.
- Codex CLI instalado y autenticado.
- Repositorio `gen-ai-skills-v0.2` disponible localmente.
- PowerShell 5.1+ o 7.

No requiere paquetes Python externos.

El runner busca `codex` primero en `PATH`. Si no está allí, en Windows busca automáticamente el ejecutable incluido en las extensiones `openai.chatgpt-*` de VS Code o VS Code Insiders. Esto permite ejecutar `doctor` desde PowerShell o Anaconda Prompt aunque el perfil de PowerShell no agregue Codex al `PATH`.

## Preparación
1. Descomprime el ZIP.
2. Edita `benchmark.config.json` y confirma `source_repo`.
3. Verifica el identificador de modelo real de tu Codex CLI. El valor inicial es `gpt-5.4-mini`, porque fue el modelo usado manualmente; si tu CLI usa otro ID, cámbialo.
4. Ejecuta:

```powershell
.\run.ps1 doctor
.\run.ps1 list
.\run.ps1 run v0.5 -DryRun
```

## Ejecutar
```powershell
.\run.ps1 run v0.1
.\run.ps1 run v0.2
.\run.ps1 run v0.3
.\run.ps1 run v0.3.1
.\run.ps1 run v0.4
.\run.ps1 run v0.5
```

Todo el set:
```powershell
.\run.ps1 run all
```

Analizar:
```powershell
.\run.ps1 analyze
```

Juez opcional para calidad (recomendado en v0.4/v0.5):
```powershell
.\run.ps1 judge v0.4
.\run.ps1 judge v0.5
.\run.ps1 analyze
```

## Métricas
El runner usa `codex exec --json` y conserva el JSONL crudo. Intenta extraer `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, tiempo de pared, exit code, thread id, respuesta final y `TRACE_JSON` autodeclarado por el agente.

Indicadores:
- `total_reported_tokens = input_tokens + output_tokens`
- `uncached_input_tokens = input_tokens - cached_input_tokens`
- rúbrica `Q` de 0 a 12
- `E_Q = Q / (total_reported_tokens/1000)` como indicador interno, no universal.

## Reproducibilidad
El harness usa snapshots fijos de `AGENTS.md` (`fixtures/AGENTS.baseline.md` y `fixtures/AGENTS.routed.md`) para que el repositorio fuente pueda evolucionar sin contaminar las comparaciones.

Cada corrida se ejecuta sobre una copia temporal del repositorio y con sandbox `read-only`; el repositorio fuente no se modifica.

## Limitaciones importantes
- El JSONL de Codex CLI puede cambiar entre versiones. Se guarda siempre el stream crudo para reanalizarlo.
- La v0.1 automatizada reproduce los objetivos de las pruebas manuales, pero P1/P2 no son una réplica byte-a-byte de la conversación original: se ejecutan como corridas independientes para aumentar reproducibilidad.
- `TRACE_JSON` no debe tratarse como log exhaustivo de todo lo leído. El hallazgo manual de v0.3.1 mostró que un recurso puede haber sido leído aunque no aparezca en la trazabilidad final.
