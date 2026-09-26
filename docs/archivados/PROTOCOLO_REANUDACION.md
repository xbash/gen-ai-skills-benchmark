# Cierre práctico del benchmark personal

Fecha: 2026-09-07.

Estado actualizado tras recuperar la sesión compartida: este es un piloto complementario. El cierre experimental principal conserva v0.4 → v0.5 → evaluación de calidad y análisis; véase [CIERRE_PERSONAL.md](CIERRE_PERSONAL.md). La prioridad de calidad de recuperación descrita aquí se aplica solo a este piloto, no reemplaza el objetivo original de eficiencia sin degradación de calidad.

## Decisión que se busca
Determinar si conviene adoptar un AGENTS.md breve para retomar proyectos con contexto correcto. La calidad de recuperación es el criterio principal propuesto; tokens y tiempo son secundarios. Este piloto no pretende demostrar ahorro universal ni reemplazar los experimentos históricos de investigación.

## Evidencia previa
El proyecto fuente está en `C:/rutinas-local/gen-ai-skills/gen-ai-skills-v0.2`. Sus archivos `.context/CONTEXT.md`, `.context/DECISIONS.md` y `.context/HANDOFF.md` registran pruebas manuales hasta v0.3.1 y v0.4 pendiente. Esos antecedentes son declaraciones documentadas; en esta sesión no se verificaron las capturas ni se reprodujeron sus cifras.

El README del proyecto fuente está vacío. La arquitectura y la continuidad existen en otros documentos. La carpeta benchmark-v0.2 vecina está vacía. Este benchmark v0.1 no tenía resultados automatizados completos al comenzar la sesión.

## Piloto
- Un proyecto local, mismo prompt, modelo configurado gpt-5.4-mini, esfuerzo medium.
- A: copia del framework sin AGENTS.md raíz.
- B: misma copia con `fixtures/AGENTS.resume.md` como AGENTS.md raíz.
- Cuatro sesiones independientes, orden ABBA; dos observaciones por condición.
- Solo lectura local, sin investigación externa ni juez automático.
- Mantener el proyecto fuente sin cambios durante las corridas.
- La configuración global del agente y posibles instrucciones anidadas no se aíslan: la comparación representa este entorno personal, no ausencia absoluta de instrucciones.
- El orden ABBA reduce una tendencia lineal simple; no sustituye aleatorización ni controla caché, carga del servicio o todas las tendencias temporales.

## Evaluación manual
Puntuar cada dimensión 0 (ausente/incorrecta), 1 (parcial) o 2 (correcta con evidencia). Esta es una rúbrica específica del piloto, no la Q de investigación del juez existente.

1. Propósito y componentes fieles a los archivos.
2. Recuperación del estado y próximos pasos de `.context/`.
3. Distinción entre resultados históricos documentados y verificación actual.
4. Reconocimiento de vacíos: README sin contenido y ausencia de historial Git en la copia.
5. Próximo paso accionable coherente con los pendientes, sin presentar recomendaciones como acuerdos del usuario.
6. Trazabilidad a rutas realmente consultadas y respeto de solo lectura.

Errores críticos: inventar resultados, afirmar validación no realizada o modificar archivos. Revisar eventos disponibles para contrastar el resumen final; no equiparar autodeclaración con registro exhaustivo.

## Regla de decisión propuesta
Adopción provisional si ambas respuestas B recuperan la continuidad, no tienen errores críticos y su calidad no es inferior a A. Si empatan, adoptar solo como convención de trabajo, sin atribuir una mejora al archivo. Si no se completa la ejecución, mantener el candidato como propuesta sin validación empírica. Dos repeticiones y un proyecto no permiten generalizar; comprobar después en un proyecto real distinto.

No calcular costos monetarios sin precios y modalidad de uso verificados. No equiparar tokens reportados por CLI con el indicador de contexto de las pruebas manuales.

## Estructura recomendada para cada proyecto
AGENTS.md: propósito breve, dónde buscar contexto, reglas de trabajo y comandos verificados. Documentos de continuidad existentes: estado, decisiones, evidencia y pendientes. Adaptar nombres y rutas al proyecto; no crear archivos vacíos para satisfacer una plantilla.

El candidato inicial está en `fixtures/AGENTS.resume.md`; aún requiere adaptación por proyecto. Usar el nombre exacto `AGENTS.md`. Codex combina instrucciones globales y de proyecto, y da prioridad a AGENTS.override.md en el mismo nivel: [documentación oficial consultada](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

## Ejecución
`python scripts/runner.py run resume-pilot`

Los resultados quedan en `results/resume-pilot/`. El runner original reutiliza identificadores; no repetir este comando sobre resultados que se desee conservar sin archivarlos antes. No usar `judge.py` para este piloto: su rúbrica de fuentes externas no corresponde a la tarea local.
