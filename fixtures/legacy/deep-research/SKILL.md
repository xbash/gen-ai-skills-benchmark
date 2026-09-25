---
name: deep-research
version: 0.2.0
description: Investigación profunda, verificable y trazable sobre una pregunta o tema definido.
category: academia
---

# Deep Research

## Objetivo

Realizar investigación profunda y estructurada sobre una pregunta, problema o tema, utilizando evidencia verificable y distinguiendo claramente hechos, evidencia, inferencias, incertidumbre y recomendaciones.

La prioridad es la calidad y trazabilidad de la investigación, no la cantidad de información recopilada.

## Cuándo usar

Usa esta skill cuando la tarea requiera una o más de las siguientes capacidades:

- investigar un tema en profundidad;
- revisar el estado del arte;
- buscar y contrastar fuentes;
- responder una pregunta que requiera evidencia externa;
- comparar métodos, tecnologías, modelos o enfoques;
- identificar consenso, controversias o vacíos de conocimiento;
- construir una base documental para una investigación posterior;
- verificar afirmaciones técnicas o académicas.

No la uses para preguntas simples que puedan resolverse de manera directa y confiable sin investigación adicional.

## Entradas

Identifica, cuando estén disponibles:

- pregunta u objetivo de investigación;
- alcance;
- periodo temporal;
- dominio;
- contexto geográfico;
- restricciones;
- tipo de fuentes requeridas;
- profundidad esperada;
- formato de salida.

Si falta información crítica, solicita únicamente lo indispensable.

Cuando sea posible continuar mediante supuestos razonables, decláralos explícitamente en lugar de detener innecesariamente la investigación.

## Procedimiento

### 1. Definir la pregunta

Reformula internamente el objetivo como una o más preguntas investigables.

Separa:

- pregunta principal;
- subpreguntas necesarias;
- restricciones;
- criterios de éxito.

No amplíes el alcance sin justificación.

### 2. Diseñar la búsqueda

Determina qué evidencia sería necesaria para responder cada subpregunta.

Prioriza fuentes según el dominio:

1. artículos científicos y publicaciones revisadas por pares;
2. documentación oficial y estándares;
3. organismos públicos, universidades e instituciones reconocidas;
4. repositorios oficiales mantenidos por autores u organizaciones;
5. literatura técnica de alta calidad;
6. fuentes secundarias cuando aporten contexto o permitan localizar evidencia primaria.

No uses popularidad como sustituto de autoridad.

### 3. Buscar evidencia

Realiza búsquedas suficientemente diversas para evitar depender de una única formulación o fuente.

Cuando corresponda, combina:

- términos técnicos;
- sinónimos;
- nombres de métodos;
- autores o instituciones;
- periodos temporales;
- contexto geográfico.

Para afirmaciones importantes, intenta obtener evidencia independiente cuando sea razonable.

### 4. Evaluar las fuentes

Evalúa al menos:

- autoridad;
- relevancia;
- actualidad;
- metodología;
- evidencia presentada;
- posibles conflictos de interés;
- aplicabilidad al problema investigado.

Una fuente reciente no reemplaza automáticamente una fuente primaria o fundacional.

### 5. Contrastar

No acumules fuentes sin analizarlas.

Identifica:

- resultados coincidentes;
- resultados contradictorios;
- diferencias metodológicas;
- condiciones bajo las cuales cambian las conclusiones;
- limitaciones;
- vacíos de evidencia.

Cuando las fuentes discrepen, presenta la discrepancia en lugar de seleccionar silenciosamente una posición.

### 6. Sintetizar

Construye la respuesta desde la evidencia encontrada.

Distingue explícitamente cuando sea relevante:

- **hecho:** respaldado directamente por evidencia;
- **inferencia:** conclusión razonada a partir de evidencia;
- **hipótesis:** explicación todavía no demostrada;
- **estimación:** valor aproximado;
- **recomendación:** decisión propuesta;
- **incertidumbre:** información insuficiente o contradictoria.

No presentes inferencias como hechos.

### 7. Validar

Antes de finalizar, verifica:

- que la pregunta original fue respondida;
- que las afirmaciones importantes tienen respaldo;
- que las fuentes citadas realmente sustentan las afirmaciones asociadas;
- que no se inventaron referencias, datos, métricas o resultados;
- que las limitaciones relevantes fueron declaradas;
- que hechos y recomendaciones están diferenciados.

Cuando la tarea requiera una revisión más rigurosa, utiliza `CHECKLIST.md`.

## Uso de fuentes

Prefiere fuentes primarias y verificables.

No inventes:

- autores;
- títulos;
- DOI;
- URL;
- fechas;
- resultados experimentales;
- benchmarks;
- estadísticas;
- citas textuales.

Si una afirmación no puede verificarse adecuadamente, indícalo.

Para información dependiente del tiempo, verifica su vigencia antes de utilizarla.

## Salida

Adapta la estructura a la pregunta. Como mínimo, una investigación profunda debería permitir identificar:

1. respuesta o hallazgos principales;
2. evidencia que los sustenta;
3. controversias o alternativas relevantes;
4. limitaciones e incertidumbres;
5. fuentes utilizadas.

Usa `TEMPLATE.md` cuando se requiera un informe estructurado y reutilizable.

Consulta `EXAMPLES.md` únicamente cuando sea necesario resolver ambigüedades sobre el uso de la skill.

## Criterios de calidad

Una investigación es satisfactoria cuando:

- responde directamente al problema;
- utiliza fuentes pertinentes y verificables;
- prioriza evidencia primaria;
- contrasta evidencia relevante;
- evita afirmaciones no respaldadas;
- distingue evidencia de interpretación;
- declara incertidumbre y limitaciones;
- mantiene trazabilidad entre afirmaciones y fuentes.

## Eficiencia de contexto

Aplica progressive disclosure.

No cargues automáticamente todos los documentos relacionados con el tema.

Busca, selecciona y profundiza iterativamente según la evidencia necesaria para responder la pregunta.

No aumentes el número de fuentes si las nuevas fuentes no aportan evidencia, contraste o cobertura adicional relevante.

## Limitaciones

Esta skill no garantiza:

- revisión sistemática exhaustiva;
- metaanálisis;
- acceso a literatura cerrada o no disponible;
- validez de fuentes que no puedan inspeccionarse;
- actualidad de información que no pueda verificarse.

Cuando la tarea requiera una revisión sistemática formal, metaanálisis u otro protocolo especializado, utiliza una metodología específica en lugar de asumir que `deep-research` la sustituye.