# Skill: plan — Planificación de Proyecto

> **Alcance:** Implementación de referencia del área IA (fases EDA → modelado → evaluación → entrega). EO adapta a EDT/cronograma/riesgos PMBoK. TD adapta a arquitectura de integración, fases de conectores y dependencias TI. Prevalece lo definido en el CLAUDE.md del agente.

## Propósito

Transformar la especificación validada en un plan de desarrollo concreto: fases de datos, modelado, evaluación y entrega. Define el entorno técnico, las dependencias de datos, los experimentos a correr y los hitos de validación. Evita iniciar desarrollo sin haber planificado la obtención y preparación de datos.

---

## Cuándo usar este skill

- El skill `spec` fue completado con datos confirmados y métricas definidas
- El orquestador solicita planificar el desarrollo de un proyecto IA
- Se necesita estimar esfuerzo y dependencias antes de asignar recursos

**Prerequisito:** `spec` aprobado con tipo de solución, datos y métricas definidos.

---

## Protocolo de ejecución

### Paso 1 — Revisar la especificación
Leer `datos/YYYY-MM-DD_spec-ia-[proyecto].md` y extraer:
- Tipo de solución, datos requeridos, métricas de éxito, audiencia del entregable

### Paso 2 — Definir fases del proyecto IA

| Fase | Descripción | Hito verificable |
|---|---|---|
| **1. Ingesta y exploración de datos** | Extraer datos, análisis exploratorio (EDA), perfil de calidad | EDA aprobado, datos suficientes confirmados |
| **2. Preparación y feature engineering** | Limpieza, transformación, variables derivadas | Dataset listo para modelar |
| **3. Modelado / desarrollo** | Entrenamiento, tuning de hiperparámetros, experimentos | Modelo o solución con métricas en rango meta |
| **4. Evaluación y validación** | Test en datos no vistos, validación con expertos operacionales | Métricas de éxito cumplidas |
| **5. Entrega (build → test → ship)** | Empaquetado, documentación, hand-off | Entregable en producción o uso operacional |

### Paso 3 — Definir entorno técnico
- Python version, librerías principales (scikit-learn, XGBoost, LangGraph, GeoPandas, etc.)
- Fuentes de datos y método de acceso (SQLite, API, CSV, SGL export)
- Estructura de archivos del proyecto IA

### Paso 4 — Planificar experimentos (para proyectos ML)
Definir antes de correr el primer modelo:
- Baseline simple (regla heurística o modelo trivial) como punto de comparación
- Hipótesis de features más relevantes
- Modelos candidatos a evaluar
- Protocolo de validación (train/val/test split, cross-validation, walk-forward para series de tiempo)

### Paso 5 — Identificar riesgos técnicos
| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Datos insuficientes o inconsistentes | A/M/B | A/M/B | Validar muestra antes de iniciar |
| Modelo no alcanza métrica meta | M | M | Definir umbral de "suficientemente bueno" |
| Entregable no adoptado por el equipo | M | A | Involucrar usuarios en la validación |

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_plan-ia-[nombre-proyecto].md
```

---

## Plantilla de plan IA

```markdown
# Plan de Proyecto IA — [Nombre]
**Fecha:** YYYY-MM-DD
**Área:** Inteligencia Artificial
**Responsable:** [Nombre]

---

## Fases y hitos

| Fase | Tareas principales | Responsable | Inicio | Fin | Hito |
|---|---|---|---|---|---|
| Ingesta / EDA | | | | | EDA aprobado |
| Feature engineering | | | | | Dataset listo |
| Modelado | | | | | Modelo en rango meta |
| Evaluación | | | | | Validado con expertos |
| Entrega | | | | | En uso operacional |

---

## Entorno técnico
- **Python:** [versión]
- **Librerías:** [lista]
- **Fuente de datos:** [sistema + método de acceso]
- **Estructura de archivos:**
```
datos/[proyecto]/
├── raw/        ← datos originales sin tocar
├── processed/  ← datos limpios y transformados
├── models/     ← modelos entrenados (.pkl, .joblib)
└── outputs/    ← entregables finales
```

---

## Plan de experimentos (ML)
| Experimento | Modelo | Features | Validación | Métrica objetivo |
|---|---|---|---|---|
| Baseline | Media / regla simple | — | — | Referencia |
| Exp-01 | [modelo] | [features] | [protocolo] | [meta] |

---

## Criterio de inicio de ejecución (build)
- [ ] Datos accesibles y perfil de calidad conocido
- [ ] Entorno técnico configurado
- [ ] Plan de experimentos definido
- [ ] Riesgos críticos con plan de mitigación
```

---

## Restricciones de este skill

- No iniciar desarrollo sin haber definido el baseline: sin baseline no hay forma de saber si el modelo agrega valor
- El protocolo de validación debe definirse antes de entrenar el primer modelo (para evitar data leakage)
- Para proyectos GenAI, definir los criterios de evaluación humana antes de construir
