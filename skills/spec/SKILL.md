# Skill: spec — Especificación de Proyecto IA/GenAI

> **Agente:** IA — Inteligencia Artificial. EO y TD tienen implementaciones propias en `agentes/EO/skills/spec/` y `agentes/TD/skills/spec/`.

## Propósito

Definir con precisión un proyecto de inteligencia artificial o GenAI antes de planificar o desarrollar. Produce un documento de especificación que alinea al equipo sobre qué problema resuelve la IA, con qué datos, qué tipo de solución y cómo se medirá el éxito. Evita construir modelos para preguntas mal formuladas.

---

## Cuándo usar este skill

- El orquestador asigna un nuevo proyecto IA, ML o GenAI
- Se detecta una oportunidad donde un modelo o agente puede reducir incertidumbre operacional
- Se solicita un análisis de datos sin haber definido la pregunta de negocio
- Se necesita alinear a stakeholders antes de invertir en datos o desarrollo

**Prerequisito:** ninguno. Es el punto de partida de todo proyecto IA.

---

## Protocolo de ejecución

### Paso 1 — Entender el problema de negocio
Antes de pensar en algoritmos, responder:
- ¿Qué decisión operacional o de negocio mejora esta solución IA?
- ¿Qué hace hoy el equipo sin esta IA? ¿Cuánto tiempo/error cuesta?
- ¿Es un problema de predicción, clasificación, generación, detección o automatización?
- ¿Qué datos existen hoy y en qué sistema viven?

### Paso 2 — Clasificar el tipo de solución
| Tipo | Cuándo aplica |
|---|---|
| **Modelo predictivo / ML** | Predecir productividad, fallos, rendimiento; necesita datos históricos etiquetados |
| **GenAI / LLM** | Resumir reportes, clasificar texto, generar fichas, asistentes especializados |
| **Agente Claude** | Flujos de razonamiento multi-step, tool use, consulta de sistemas |
| **Dashboard / análisis** | Visualización de KPIs, series de tiempo, detección de patrones |
| **Cartografía IA** | Análisis geo-espacial, imágenes satelitales, productividad de terreno |

### Paso 3 — Definir requerimientos de datos
Para cada fuente de datos necesaria:
| Dato | Sistema fuente | Formato | Disponibilidad | Responsable |
|---|---|---|---|---|

Señalar explícitamente si los datos no existen o tienen problemas de calidad.

### Paso 4 — Definir métricas de éxito
Para proyectos ML: accuracy, F1, RMSE, AUC según el tipo de problema.
Para proyectos GenAI: calidad de output (humana), tiempo ahorrado, tasa de adopción.
Para dashboards: KPIs correctos, frecuencia de actualización, adopción del equipo.

| Métrica | Definición | Línea base actual | Meta | Cómo se mide |
|---|---|---|---|---|

### Paso 5 — Definir entregable y audiencia
- ¿Qué forma tiene el entregable? (modelo `.pkl`, dashboard `.html`, agente, API)
- ¿Quién lo usa? (operador de terreno, supervisor, gerencia, otro sistema)
- ¿Cómo se interpreta? (el usuario final debe poder usarlo sin el equipo IA)

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_spec-ia-[nombre-proyecto].md
```

---

## Plantilla de especificación IA

```markdown
# Especificación de Proyecto IA
**Fecha:** YYYY-MM-DD
**Área:** Inteligencia Artificial
**Proyecto:** [Nombre corto]
**Solicitante / Orquestador:** [Nombre o sistema]

---

## 1. Problema de negocio
[¿Qué decisión o proceso mejora esta solución? ¿Qué cuesta el problema hoy?]

## 2. Tipo de solución IA
☐ Modelo predictivo / ML   ☐ GenAI / LLM   ☐ Agente Claude
☐ Dashboard / análisis      ☐ Cartografía IA  ☐ Otro: ___

## 3. Requerimientos de datos
| Dato | Sistema | Formato | Disponible | Responsable |
|---|---|---|---|---|

**Problemas de calidad de datos identificados:** [lista o "ninguno detectado aún"]

## 4. Métricas de éxito
| Métrica | Línea base | Meta | Cómo se mide |
|---|---|---|---|

## 5. Entregable esperado
**Forma:** [modelo / dashboard / agente / API / otro]
**Audiencia:** [quién lo usa]
**Criterio de interpretabilidad:** [cómo lo entiende alguien sin perfil técnico IA]

## 6. Alcance
**Incluye:** [qué entra en scope]
**Excluye:** [qué no se abordará]

## 7. Supuestos y riesgos de datos
- [Supuesto 1: datos disponibles desde fecha X con frecuencia Y]
- [Riesgo 1: baja calidad de etiquetas en historial SGL]

## 8. Criterio de inicio del plan
- [ ] Problema de negocio validado con stakeholder operacional
- [ ] Datos confirmados como accesibles (aunque sea muestra)
- [ ] Métricas de éxito acordadas
- [ ] Tipo de solución IA definido
```

---

## Restricciones de este skill

- No se puede avanzar al skill `plan` sin métricas de éxito definidas y datos confirmados como accesibles
- No proponer tipo de solución sin entender el problema: no elegir "LLM" por defecto
- Si los datos no existen o tienen calidad insuficiente, documentarlo y escalar antes de continuar
- El entregable debe ser interpretable por el equipo operacional, no solo por el área IA
