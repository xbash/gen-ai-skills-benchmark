# Decisiones vigentes

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
