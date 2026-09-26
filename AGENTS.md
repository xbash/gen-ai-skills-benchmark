# Instrucciones para agentes

## Alcance

Este repositorio contiene un harness para ejecutar, conservar y analizar
experimentos reproducibles sobre carga de contexto e instrucciones de agentes.

Estas reglas son estables. Para uso del proyecto, estado de una sesión,
decisiones, resultados o planes vigentes, consulta los documentos específicos
referenciados desde `README.md` y `docs/`; no copies esa información aquí.

## Estructura y carga de contexto

- `experiments/`: definición declarativa de cada experimento.
- `prompts/`: prompts usados por las corridas.
- `fixtures/`: variantes controladas de instrucciones.
- `scripts/`: runner, juez y análisis.
- `results/`: evidencia producida por las corridas.
- `docs/`: continuidad y decisiones vigentes; `docs/archivados/` conserva
  documentación histórica que no participa en decisiones operativas.

Carga solo el contexto necesario para la tarea:

1. Lee `README.md` para orientación y uso.
2. Para modificar o revisar un experimento, carga su archivo en `experiments/`,
   el prompt asociado y el script afectado.
3. Para interpretar resultados, carga únicamente los artefactos y documentos
   relevantes a la cohorte o condición solicitada.
4. Consulta documentos de continuidad solo al retomar estado o decidir trabajo
   posterior; no los trates como reglas permanentes.

No infieras que `TRACE_JSON` representa un registro exhaustivo de archivos
leídos o acciones realizadas.

## Integridad experimental y evidencia

- No inventes métricas, resultados, capacidades, costos, tiempos, fuentes ni
  conclusiones.
- Distingue hechos observados, inferencias, recomendaciones, riesgos,
  limitaciones y pendientes de verificación.
- Conserva condiciones comparables: misma tarea, prompt, configuración,
  modelo, esfuerzo, sandbox y procedimiento, salvo que el experimento evalúe
  explícitamente una de esas variables.
- No presentes muestras pequeñas, resultados exploratorios o una sola cohorte
  como evidencia causal o generalizable.
- Al reportar resultados, identifica al menos condición, repeticiones,
  configuración, `exit_code`, métricas observadas y limitaciones.
- Mantén separados resultados activos, intentos fallidos, archivos históricos
  y preparaciones de prueba. No sobrescribas evidencia existente.
- No modifiques retroactivamente prompts, fixtures, definiciones de experimento
  ni condiciones de una cohorte que ya tenga resultados; crea una nueva
  definición o identificador para una variación comparativa.
- Regenera `results/summary.md` y `results/summary.csv` únicamente mediante
  `scripts/analyze.py`; no edites manualmente resultados crudos ni resúmenes
  derivados.

## Ejecución y validación

- Usa los lanzadores y scripts existentes; no reimplementes su lógica en
  comandos ad hoc si el proyecto ya proporciona una ruta equivalente.
- Antes de una ejecución real, valida configuración, repositorio fuente,
  disponibilidad de Codex y autenticación mediante el procedimiento
  documentado en `README.md`.
- Para cambios en scripts o definiciones de experimentos, realiza validaciones
  proporcionales: revisión estática, prueba acotada y/o preparación en seco
  cuando corresponda. Distingue esas validaciones de una corrida experimental.
- Para cambios en scripts Python, usa como mínimo una compilación estática;
  para cambios en experimentos, prompts o configuración, revisa referencias y
  usa preparación en seco solo cuando esté autorizada. Antes de una corrida
  real, ejecuta `doctor` en el mismo contexto de usuario.
- Una ejecución puede crear resultados, salidas temporales o espacios de
  trabajo; no la ejecutes sin que la tarea la autorice.
- No modifiques manualmente resultados crudos, archivos de configuración o
  artefactos generados para ajustar una conclusión.

## Política de modificaciones y seguridad

- Antes de modificar, identifica los archivos canónicos y revisa el estado Git.
  Preserva cambios ajenos.
- Analiza impacto y dependencias antes de eliminar archivos o directorios,
  cambiar configuraciones relevantes, dependencias, estructuras persistentes o
  realizar refactorizaciones extensas.
- Si existe incertidumbre relevante sobre una operación destructiva o de alto
  impacto, presenta la acción y su alcance antes de ejecutarla.
- No ejecutes `git clean`, staging, commit, push, publicación ni borrados sin
  autorización explícita.
- No expongas ni incorpores secretos, credenciales, tokens o datos sensibles.
- No incluyas secretos ni contenido sensible en prompts, trazas, respuestas
  finales o artefactos de resultados; `TRACE_JSON` debe limitarse a metadatos
  necesarios para la trazabilidad.
- Mantén archivos de texto en UTF-8 sin BOM, con LF, newline final y sin
  espacios finales cuando las convenciones del repositorio lo requieran.

## Selección eficiente de modelos

Esta política es independiente del proveedor. Clasifica el trabajo por rol y
elige siempre el rol menos costoso que pueda completarlo correctamente:

- **Ejecutor**: razonamiento bajo, para tareas mecánicas, deterministas y de
  alta velocidad. Mapeo vigente: Luna.
- **Analista**: razonamiento medio, para análisis acotado y equilibrio entre
  rendimiento y costo. Mapeo vigente: Tierra.
- **Arquitecto**: razonamiento alto, para diseño, decisiones de impacto,
  análisis transversal y revisión sustantiva. Mapeo vigente: Sol.
- No elijas un rol de mayor capacidad solo por el volumen de archivos:
  distingue volumen operativo de complejidad cognitiva.
- Prefiere herramientas deterministas —búsqueda, Git, scripts, validadores,
  linters y pruebas— cuando resuelvan la tarea con menor incertidumbre que el
  razonamiento de un LLM.

## Planificación y ejecución

Para tareas complejas, separa análisis de ejecución:

1. Usa el rol Arquitecto para diagnóstico, diseño y un plan verificable cuando
   la complejidad o el impacto lo justifiquen.
2. Divide el plan en operaciones pequeñas, con alcance y validación definidos.
3. Delega operaciones mecánicas aprobadas al rol Ejecutor.
4. Escala al rol Analista o Arquitecto solo ante decisiones no cubiertas,
   ambigüedad relevante, riesgo alto o impacto arquitectónico.
5. Documenta estado, decisiones y resultados en sus destinos correspondientes,
   no en este archivo.
