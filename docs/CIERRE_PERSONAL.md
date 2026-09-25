# Estado del cierre personal — 2026-09-07

## Estado operativo actualizado
La autenticación ChatGPT se confirmó al verificar fuera del sandbox del proceso controlador. El estado `Not logged in` observado dentro de ese sandbox no describe la sesión de la terminal del usuario. No fue necesario volver a autenticar después de comprobar esa diferencia.

Primera corrida real completada: v0.4/A_BASELINE-01, exit_code=0, 280.232 segundos. Uso reportado: 242160 tokens de entrada, 107008 de entrada cacheada, 15128 de salida y 12404 de razonamiento de salida. El total definido por el benchmark es 257288 (entrada + salida); no sumar nuevamente razonamiento ni caché. Es una observación sin comparación ni Q todavía.

El registro muestra búsquedas en memoria global e intentos fallidos de localizar la skill instalada. El agente declara `deep_research_used=false` en su respuesta final. Intentar cargar una skill no equivale a haberla utilizado. Estos eventos limitan la interpretación a este entorno personal. v0.4 evalúa el efecto de solicitar explícitamente la skill, no garantiza ausencia/presencia de su uso efectivo.

Las secciones siguientes conservan el historial del bloqueo anterior. El bloqueo de autenticación está resuelto para ejecuciones con permisos de usuario; v0.4 está en curso mediante `--resume`.

Segunda actualización: v0.4/A_BASELINE-02 terminó con exit_code=0 en 353.136 segundos. Uso reportado: 256606 tokens de entrada, 109824 cacheados, 21856 de salida y 18601 de razonamiento de salida; total del benchmark 278462. Declaró uso de deep-research y consultó `AGENTS.md`, `docs/token-efficiency.md` y la skill. La tercera corrida no alcanzó a ejecutarse: el servicio devolvió límite de uso y pidió reintentar a las 18:45. Ese intento tiene exit_code=1 y uso vacío; se excluye de las medias y será archivado automáticamente al reanudar.

Tercera actualización: las seis corridas de v0.4 finalizaron correctamente tras reanudar A3. Cuatro de seis respuestas omitieron el `TRACE_JSON` solicitado, incluidas las tres condiciones explícitas; la ausencia se conserva como incumplimiento y no se reconstruye por inferencia. El juez originalmente configurado como gpt-5.4 no es compatible con autenticación ChatGPT: seis intentos terminaron con exit_code=1 y sin Q. Se cambió a gpt-5.4-mini, modelo comprobado en esta cuenta. Esto da sesiones evaluadoras separadas, pero no independencia entre familias de modelo; considerar posible sesgo de autoevaluación.

## Conclusión disponible
Todavía no hay evidencia automatizada para atribuir ahorro de tokens o mejora de calidad a AGENTS.md. Se puede usar el candidato como convención provisional para retomar proyectos; no se presenta como una optimización demostrada.

## Qué quedó preparado
- Ruta del repositorio fuente corregida y existencia comprobada.
- Piloto local ABBA de cuatro corridas y rúbrica específica en [PROTOCOLO_REANUDACION.md](PROTOCOLO_REANUDACION.md).
- Candidato adaptable en `fixtures/AGENTS.resume.md`.
- Logs del runner escritos durante la ejecución; límite de 180 segundos por corrida del piloto y detención ante el primer fallo.
- Doctor comprueba también el estado de autenticación.

## Resultado de la ejecución
Actualización de preparación: v0.4 (6 corridas) y v0.5 (10 corridas) pasaron la ejecución en seco. Se comprobaron los 16 metadatos, la ausencia/presencia y contenido de AGENTS.md según condición, y la igualdad SHA-256 del resto de archivos entre copias de cada experimento. Esto valida la preparación local, no el modelo, la investigación externa ni la calidad. Los artefactos están en `output/dry-run/`; las corridas reales con metadatos existentes ahora están protegidas contra sobrescritura.

La primera tentativa se interrumpió sin resultado; el runner anterior retenía los logs en memoria. Se reinició tras habilitar escritura continua. La segunda tentativa registró HTTP 401 Unauthorized y reintentos de conexión. `codex login status` devolvió `Not logged in`.

Se detuvo exclusivamente el proceso hijo de esa corrida; el runner conservó los logs, registró salida fallida y detuvo el experimento. No hubo respuesta evaluable, métricas de uso ni corridas B. La duración y el código de salida del intento fallido no son resultados comparativos del modelo.

Evidencia: `results/resume-pilot/A_NO_AGENTS_FIRST/A_NO_AGENTS_FIRST-01/` contiene eventos JSONL, stderr y metadatos. No confundir fallo de autenticación con desempeño de AGENTS.md.

## Para terminar la comparación
Actualización tras leer la sesión compartida el 2026-09-07: el cierre original es v0.4 (valor de solicitar la skill) seguido de v0.5 (comparación sin/con AGENTS.md), evaluando calidad, tokens y tiempo. El piloto de reanudación es complementario y no reemplaza esas pruebas.

Secuencia principal recuperada: `doctor` → `list` → `run v0.5 -DryRun` → `run v0.4` → `run v0.5` → evaluación de calidad → `analyze`. No es necesario repetir de inmediato v0.1–v0.3.1. Antes de interpretar resultados, atender las limitaciones metodológicas ya identificadas: orden fijo, configuración global, baseline v0.4 que puede activar la skill y trazabilidad autodeclarada.

Para el piloto complementario:

1. Autenticar Codex CLI en una terminal propia con `codex login`; no compartir credenciales en el chat.
2. Ejecutar `python scripts/runner.py doctor`.
3. Archivar el intento fallido antes de repetir `python scripts/runner.py run resume-pilot`, porque el runner reutiliza identificadores.
4. Aplicar la rúbrica manual y registrar resultados por condición, incluidos errores y variación. No usar el juez de investigación para esta tarea.

## Para construir AGENTS.md en los proyectos
Usar instrucciones breves y específicas: propósito, rutas reales de contexto, cómo verificar el estado, comandos comprobados y límites del proyecto. Mantener decisiones y pendientes en los documentos de continuidad que ya existan. Si faltan, acordar un documento mínimo de estado; no llenar AGENTS.md de historial.

Antes de generalizar, adaptar el candidato a un proyecto real y verificar que una sesión nueva recupere sus pendientes sin inventar avances. El candidato actual corresponde al framework de skills y no debe copiarse literalmente a proyectos con otro propósito.

## Alcance
Solo se modificó el benchmark activo. El framework fuente y los demás proyectos no se editaron. El benchmark queda preparado, con ejecución empírica bloqueada por autenticación; no cerrado como experimento exitoso.

## Antecedentes recuperados
Fuente: https://chatgpt.com/share/6a9eeac8-31cc-83e9-9fcb-4edde32ceec4, título «Equivalentes entre Claude y Codex». Texto visible guardado en `output/playwright/sesion-compartida.txt`. Se recuperaron acuerdos textuales, no se verificaron imágenes ni archivos adjuntos; las cifras históricas siguen siendo antecedentes documentados, no resultados reproducidos. Las filas numéricas del CSV ilustrativo de esa conversación son ejemplos, no mediciones.
