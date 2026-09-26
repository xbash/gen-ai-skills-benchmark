# Decisiones vigentes

Actualizado: 2026-09-26.

1. La configuración operativa actual usa `gpt-5.6-terra` con esfuerzo
   `medium` para productor y juez. Es una configuración de referencia local,
   no una afirmación universal de superioridad.
2. La conclusión vigente sobre AGENTS proviene de
   `v0.9-agents-effect-controlled`: bajo tarea, repositorio, prompt,
   Terra/medium y sandbox read-only controlados, AGENTS aumentó tokens y tiempo
   sin mejorar Q. No generalizar a otras tareas, modelos o entornos.
3. `v0.5` Terra se conserva como evidencia exploratoria, no causal, por el
   valor atípico A05 y deep research en B02. v0.8 compara esfuerzos solo de
   modo descriptivo.
4. Mantener separadas cohortes, condiciones, modelos, esfuerzos, intentos
   fallidos y archivos históricos. No sobrescribir `meta.json`, ni alterar
   retrospectivamente prompts, fixtures, experimentos o configuración de una
   cohorte con resultados.
5. Los resúmenes se regeneran mediante `scripts/analyze.py`; no se editan
   manualmente resultados ni artefactos derivados para cambiar una conclusión.
6. Mantener `encoding='utf-8'` al enviar prompts desde `scripts/runner.py`.
   El intento fallido previo se conserva en `results/_attempts/v0.5/`.
7. `docs/archivados/` es el repositorio canónico de documentación histórica;
   no participa en decisiones operativas.
8. No ejecutar corridas que consuman créditos, dry-runs o análisis que escriba
   artefactos sin autorización explícita. `git clean`, staging, commit, push,
   publicación y borrados también requieren autorización explícita.
