# Decisiones vigentes

> **Actualizacion 2026-09-26.** Estas decisiones reemplazan cualquier estado
> operativo contradictorio que aparezca mas abajo.

12. Usar `gpt-5.6-terra` con `medium` como productor y juez de referencia.
    La eleccion viene de los pilotos v0.7/v0.8 y es exploratoria, no una
    afirmacion universal de superioridad.
13. Tratar la comparacion de esfuerzos Terra como evidencia descriptiva: low
    privilegia tiempo/tokens; medium obtuvo la Q mas alta del piloto; high no
    mejoro la Q observada frente a medium.
14. Conservar `v0.5` Terra como cohorte exploratoria de AGENTS. No afirmar que
    AGENTS ahorra tokens o tiempo: las medias estan afectadas por A05 y B02
    activo investigacion externa/deep research.
15. `v0.9-agents-effect-controlled` completo con cinco repeticiones por
    condicion y controles de fuentes satisfechos. En esta tarea, AGENTS aumento
    tokens y tiempo en medias y medianas; Q promedio fue ligeramente menor y Q
    mediana igual.
16. La respuesta queda acotada a la tarea, repositorio, Terra/medium,
    sandbox read-only y prompt controlado de v0.9. No generalizar a otras
    tareas o modelos. Si se requiere una recomendacion para otro dominio,
    disenar una cohorte especifica.
17. Mantener `encoding='utf-8'` en el productor de `runner.py`; fue necesario
    para que Codex aceptara `research_base.txt` en Windows. El intento fallido
    permanece separado bajo `results/_attempts/`.
18. No ejecutar nuevas corridas que consuman creditos sin una autorizacion
    explicita posterior a este handoff. El dry-run no es evidencia experimental.

## Registro historico previo (no usar para el estado actual)

Fecha de corte: 2026-09-25.

1. Mantener resultados separados por cohorte, modelo, esfuerzo, experimento, condición y repetición. Nunca sobrescribir un `meta.json`.
2. Conservar `v0.6` como cohorte exploratoria; no reinterpretarla como evidencia limpia ni reutilizar sus IDs.
3. Usar `v0.6-clean-smoke` únicamente para validar el entorno reparado.
4. El piloto limpio de selección ya fue completado con `A_NO_AGENTS`, mismo prompt/workspace y `medium`, para Luna y Terra.
5. `high` es un experimento posterior: comparar `medium` contra `high` dentro del modelo elegido.
6. No modificar manualmente caches de plugins de primera parte. Los únicos cambios globales realizados fueron retirar el BOM de dos skills y respaldar/regenerar `models_cache.json`.
7. Mantener PowerShell y el contexto elevado constantes dentro de cada cohorte; el snapshot de shell es una limitación residual.

## Regla de interpretación

Informar `exit_code`, tokens de entrada/cacheados/salida/razonamiento, tiempo,
configuración y Q cuando exista. Una media con `n=1` o `n=2` es descriptiva:
no demuestra causalidad, ahorro generalizable ni superioridad de modelo.

## Limpieza y preservacion

8. No ejecutar `git clean`: el checkout tiene solo `LICENSE` versionado y el
   harness, sus documentos y artefactos aparecen como no versionados.
9. Mantener separados los resultados activos, los intentos fallidos
   (`results/_attempts/`) y la cohorte archivada (`results/_archive/`);
   `judge.py` y `analyze.py` excluyen intencionalmente los dos ultimos.
10. Mantener `output/dry-run/` como evidencia de preparacion documentada.
    Los workspaces y caches generados no deben conservarse cuando
    `keep_workspaces` sea `false`.
11. La limpieza ya aprobada elimino `.workspaces/`, `scripts/__pycache__/`,
    `output/playwright/`, `VALIDATION.txt` y `fixtures/routing-snippet.md`.
    No hay candidatos de eliminacion pendientes tras la revision de esta
    sesion.
