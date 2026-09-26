# Auditoría de limpieza del proyecto

Fecha de auditoría: 2026-09-25  
Proyecto: `C:\rutinas-local\gen-ai-skills-root\gen-ai-skills-benchmark`  
Alcance: inventario estático, referencias textuales, configuración, scripts, documentación y estado Git local. No se ejecutaron benchmarks ni se modificaron, movieron o eliminaron artefactos del proyecto.

## Criterio de clasificación

- `MANTENER`: tiene uso actual comprobable o valor técnico/operacional/histórico claro.
- `REVISAR`: no es necesario para la ejecución principal, pero conserva valor posible o existe una decisión de retención documentada.
- `ELIMINAR`: residuo temporal sin uso ni valor justificable, sujeto a confirmación antes de cualquier acción.

La matriz agrupa árboles homogéneos de resultados cuando existen cientos de archivos generados con la misma función. La clasificación se aplica al conjunto indicado; no implica que todos sus archivos internos tengan contenido idéntico.

## Estado observado

- `git ls-files` contiene únicamente `LICENSE`; el resto del harness aparece como no versionado. Los resultados están además cubiertos por `.gitignore`, por lo que Git no es una fuente suficiente para decidir su conservación.
- Existen `results/` con experimentos, intentos, archivo histórico y resúmenes, y `output/dry-run/` con preparaciones reproducibles. El árbol de resultados observado ocupa aproximadamente 6,7 MB y el de dry-run aproximadamente 40 KB.
- No existen actualmente `.workspaces/`, `scripts/__pycache__/`, `output/playwright/`, `VALIDATION.txt` ni `fixtures/routing-snippet.md`. Se consideran residuos ya ausentes, no candidatos accionables de esta auditoría.
- `runner.py` produce y consume rutas de resultados; `analyze.py` y `judge.py` excluyen explícitamente `_archive` y `_attempts`. Esto distingue uso de ejecución normal de valor histórico/diagnóstico.
- La búsqueda de referencias fue estática. Una ausencia de referencia textual no demuestra que un archivo no tenga valor para una persona ni que un flujo externo no lo utilice.

## Matriz de auditoría

| Ruta | Tipo | Uso actual | Evidencia | Propósito original | Clasificación | Riesgo | Acción propuesta |
|---|---|---|---|---|---|---|---|
| `.gitignore` | Configuración | Activo | Excluye `results/*`, `.workspaces/` y cachés; conserva `results/.gitkeep` | Evitar publicar salidas y temporales | MANTENER | Resultados no visibles en `git status`; riesgo de perder control de qué se conserva | Mantener; revisar posteriormente si los resultados seleccionados deben versionarse o documentarse fuera de Git |
| `README.md` | Documentación operativa | Activo | Describe comandos, experimentos, dry-run, reanudación y limitaciones | Explicar uso y reproducibilidad del harness | MANTENER | Puede quedar desfasado si cambian cohortes o rutas | Mantener y actualizar solo cuando cambie el flujo verificado |
| `benchmark.config.json` | Configuración | Activo | `runner.py` lo carga como `CFG`; define repositorio fuente, modelo, esfuerzo y sandbox | Centralizar parámetros del benchmark | MANTENER | Ejecutar con modelo o repositorio equivocado si se altera sin registro | Mantener; validar cambios antes de nuevas corridas |
| `run.ps1`, `run.cmd` | Lanzadores | Activo | `run.ps1` despacha `doctor`, `list`, `run`, `analyze` y `judge`; `run.cmd` lo envuelve | Interfaz operativa Windows | MANTENER | Cambiar el lanzador puede romper ejecuciones reproducibles | Mantener |
| `scripts/` | Código | Activo | `runner.py`, `analyze.py` y `judge.py` referencian configuración, experimentos, prompts, fixtures y resultados | Ejecutar, juzgar y resumir experimentos | MANTENER | Eliminación rompe el flujo principal | Mantener; no mezclar código con salidas generadas |
| `experiments/` | Configuración de experimentos | Activo | `runner.py` carga `experiments/<nombre>.json`; incluye v0.1–v0.7 y `resume-pilot` | Declarar condiciones, repeticiones y prompts | MANTENER | Borrar una versión impide reproducir o interpretar sus resultados | Mantener; marcar explícitamente experimentos cerrados si se desea archivarlos |
| `prompts/` | Entradas de experimentos | Activo | Los JSON de `experiments/` nombran los prompts; `runner.py` los lee | Definir tareas comparables | MANTENER | Cambiar prompts invalida comparaciones con resultados existentes | Mantener congelados para cohortes ya ejecutadas |
| `fixtures/AGENTS.baseline.md`, `fixtures/AGENTS.routed.md`, `fixtures/AGENTS.resume.md` | Fixtures de prueba | Activo | `runner.py` copia las variantes a los workspaces; README y protocolo las documentan | Controlar las condiciones de presencia/ausencia de `AGENTS.md` | MANTENER | Eliminar una variante impide repetir condiciones | Mantener |
| `fixtures/legacy/deep-research/SKILL.md` | Fixture histórica | No consumido por el runner actual | No hay referencias desde scripts ni configuraciones; `docs/CONTEXT.md` y `HANDOFF.md` lo identifican como referencia histórica | Preservar la versión de una skill usada en una iteración anterior | REVISAR | Confunde si se interpreta como skill activa; ocupa poco espacio | Confirmar si se necesita trazabilidad histórica; si no, eliminar solo tras conservar una referencia suficiente en la documentación |
| `output/dry-run/` | Salidas generadas de preparación | No consumido por el flujo de ejecución normal | README y `CIERRE_PERSONAL.md` lo describen como evidencia de preparación; contiene `command.json`, `meta.json` y `prompt.txt` | Verificar previamente las corridas sin invocar el modelo | REVISAR | Puede confundirse con resultados reales; es regenerable | Mantener mientras se use como evidencia de preparación; después, archivar o eliminar el árbol completo con decisión documentada |
| `results/v0.1/` a `results/v0.5/` | Resultados de benchmark | Activo como evidencia y entrada de análisis | `analyze.py` recorre `results`; `judge.py` lee corridas; README y documentos de cierre los citan | Conservar JSONL, metadatos, respuestas y métricas de corridas | MANTENER | Pérdida de evidencia y ruptura de trazabilidad; resultados están ignorados por Git | Mantener fuera de Git y respaldar según la política del proyecto |
| `results/gpt56/`, `results/gpt56-terra/` | Resultados de cohortes recientes | Activo para la decisión pendiente de modelo | `HANDOFF.md` cita v0.6, smoke limpio y pilotos v0.7; los experimentos correspondientes existen | Comparar operacionalmente cohortes y decidir próximos pasos | MANTENER | Interpretar cohortes pequeñas como evidencia causal o generalizable | Mantener; no mezclar v0.6 y v0.7 ni borrar antes de completar la decisión documentada |
| `results/resume-pilot/` | Resultado de piloto de reanudación | Parcial; el protocolo lo usa y registra un intento observado | README, `PROTOCOLO_REANUDACION.md` y `CIERRE_PERSONAL.md` lo referencian; el árbol observado contiene la corrida inicial | Evaluar recuperación de contexto con orden ABBA | MANTENER | Confundir fallo de autenticación con desempeño del fixture | Mantener hasta cerrar o declarar abandonado el piloto; separar fallos de resultados comparables |
| `results/_archive/` | Archivo de resultados | No usado por el análisis normal | `runner.py`, `analyze.py` y `judge.py` lo excluyen; `DECISIONS.md` ordena conservarlo | Separar una cohorte histórica antes de repetir o cambiar configuración | MANTENER | Duplicación y posible confusión con resultados activos | Mantener separado; identificar claramente cohorte, fecha y motivo de archivo |
| `results/_attempts/` | Intentos fallidos/reintentos | No usado por el análisis normal | `runner.py` mueve allí intentos al reanudar; scripts lo excluyen; documentos lo conservan | Diagnosticar fallos y evitar sobrescritura de IDs | REVISAR | Puede retener errores o datos sensibles de sesiones; puede crecer sin límite | Definir retención; conservar solo intentos necesarios para diagnóstico y luego eliminar por lote documentado |
| `results/summary.csv`, `results/summary.md` | Resúmenes generados | Activo como salida de análisis y lectura humana | `analyze.py` los escribe; `docs/CONTEXT.md` los cita como artefactos clave | Facilitar comparación agregada sin abrir cada corrida | MANTENER | Pueden quedar obsoletos respecto de las corridas si no se regeneran | Mantener; regenerar después de cada análisis autorizado y registrar fecha de corte |
| `docs/CONTEXT.md` | Continuidad | Activo | Contiene estado de corte, artefactos, límites y limpieza realizada | Recuperar contexto verificable entre sesiones | MANTENER | Declaraciones históricas pueden quedar obsoletas | Mantener; actualizar solo con evidencia nueva |
| `docs/DECISIONS.md` | Decisiones operativas | Activo | Define separación de resultados, exclusiones y prohibición de `git clean` | Registrar decisiones de preservación e interpretación | MANTENER | Contradicciones con una futura limpieza pueden inducir pérdida de evidencia | Mantener y actualizar si cambia una decisión humana |
| `docs/HANDOFF.md` | Handoff | Activo | Señala la decisión pendiente sobre v0.7 y rutas exactas | Permitir reanudar el trabajo sin repetir corridas | MANTENER | Queda obsoleto cuando se tome la decisión pendiente | Mantener hasta cerrar la decisión; luego convertirlo en historial o reemplazarlo por un handoff nuevo |
| `docs/PROTOCOLO_REANUDACION.md` | Protocolo/rúbrica del piloto | Activo | README lo enlaza; `resume-pilot.json` y `fixtures/AGENTS.resume.md` implementan el flujo | Definir pregunta, condiciones, límites y regla de decisión | MANTENER | Piloto antiguo puede confundirse con el benchmark principal | Mantener; etiquetarlo como piloto complementario y no usar `judge.py` para él |
| `docs/otros/RUBRIC.md` | Rúbrica histórica | No leído por los scripts actuales | `judge.py` contiene su propia rúbrica; la versión archivada conserva un criterio específico de v0.5 | Preservar la interpretación histórica de esa cohorte | MANTENER | Confundir su criterio específico con la evaluación vigente | Mantener como historial; no usarla como referencia operativa |
| `docs/CIERRE_PERSONAL.md` | Cierre histórico/continuidad antigua | Referenciado por `PROTOCOLO_REANUDACION.md`, pero parcialmente superseded por `CONTEXT.md` y `HANDOFF.md` | Contiene estados de 2026-09-07 y antecedentes, incluyendo una ruta `output/playwright/` que ya no existe | Preservar decisiones y bloqueos de iteraciones anteriores | REVISAR | Presenta estados antiguos y rutas ausentes; puede inducir a repetir pasos ya resueltos | Comparar con `CONTEXT.md`; conservar como historial con etiqueta explícita o consolidar y retirar tras decisión humana |
| `docs/AUDITORIA_LIMPIEZA_PROYECTO.md` | Informe de auditoría | Activo desde esta auditoría | Es el entregable solicitado; no es entrada del runner | Dejar trazabilidad de candidatos, evidencia y plan | MANTENER | Puede quedar obsoleto después de aplicar decisiones | Mantener como registro fechado; generar una nueva auditoría si cambia sustancialmente el árbol |

## Resumen por categoría

Conteo de filas de la matriz, agrupando árboles homogéneos:

| Categoría | Cantidad |
|---|---:|
| MANTENER | 18 |
| REVISAR | 4 |
| ELIMINAR | 0 |
| Total | 22 |

El cero en `ELIMINAR` es deliberado: no se encontró un elemento actualmente presente que carezca simultáneamente de uso, valor histórico/técnico/operacional y una decisión de retención documentada. La auditoría no autoriza por sí misma la eliminación.

## Principales residuos detectados

1. `output/dry-run/` es una salida generada y regenerable. Tiene valor como evidencia de preparación y está documentado, pero no participa en el análisis normal.
2. `results/_attempts/` contiene intentos fallidos o reintentados. Es útil para diagnóstico, pero no entra en `analyze.py` ni `judge.py` y necesita una política de retención.
3. `fixtures/legacy/deep-research/SKILL.md` es una copia histórica no consumida por el runner. Su valor depende de si se requiere reproducir una iteración anterior.
4. `docs/CIERRE_PERSONAL.md` conserva contexto histórico, pero contiene estados antiguos y referencias a `output/playwright/`, que ya no existe.
5. Hay un riesgo transversal de control de cambios: casi todo el harness y sus artefactos no están versionados, y `results/` está ignorado. La ausencia en Git no equivale a obsolescencia ni a respaldo.

## Casos ambiguos que requieren decisión humana

- ¿Debe conservarse `fixtures/legacy/deep-research/SKILL.md` para reproducibilidad histórica o basta la referencia documental?
- ¿Cuál es la retención aceptable para `results/_attempts/` y para los intentos que contienen errores de autenticación, límites o fallos de servicio?
- ¿Se desea conservar `output/dry-run/` como evidencia permanente o solo hasta cerrar la preparación de las cohortes actuales?
- ¿`docs/CIERRE_PERSONAL.md` debe permanecer como bitácora histórica, o consolidarse con `docs/CONTEXT.md` y `docs/HANDOFF.md` para evitar documentación obsoleta?
- ¿Qué política externa de respaldo/versionado debe aplicarse a `results/`, dado que `.gitignore` oculta las salidas y solo `LICENSE` está versionado en el checkout observado?

## Plan de acción propuesto

El plan no se ejecuta con esta auditoría.

1. Decidir primero la retención de los cuatro casos `REVISAR`, sin borrar nada.
2. Si se conserva evidencia, añadir una convención de archivo: fecha, cohorte, motivo, contenido y criterio de restauración.
3. Si se autoriza una limpieza, actuar por lotes completos y explícitos: `output/dry-run/`, `results/_attempts/`, el fixture legacy o el documento histórico que corresponda. No usar `git clean` ni patrones amplios.
4. Antes de cada lote, comprobar referencias, estado Git, tamaño y copia de respaldo; después, verificar que `runner.py`, `analyze.py` y `judge.py` siguen encontrando las rutas activas.
5. Regenerar `results/summary.csv` y `results/summary.md` únicamente si el usuario autoriza una nueva ejecución de análisis; no presentar resúmenes regenerados como resultados nuevos sin identificar la fecha de corte.
6. Actualizar `CONTEXT.md`, `DECISIONS.md` y `HANDOFF.md` solo después de una decisión humana, conservando qué se retiró y por qué.

## Limitaciones

- No se ejecutaron corridas, juez, análisis ni pruebas funcionales; la evaluación de uso actual se basa en inspección estática y referencias.
- No se inspeccionó el contenido completo de cada JSONL de resultados porque la clasificación se realizó por función del árbol y por los consumidores declarados en código.
- La fecha de modificación y el tamaño son evidencia auxiliar, no prueba de obsolescencia.
- La ausencia de historial de versiones útil para el harness impide reconstruir con Git quién creó cada archivo o recuperar con Git un archivo que se elimine.
