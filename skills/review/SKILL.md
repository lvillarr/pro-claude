# Skill: review — Revisión de Proyectos IA

> **Agente:** IA — Inteligencia Artificial. EO y TD tienen implementaciones propias en `agentes/EO/skills/review/` y `agentes/TD/skills/review/`.

## Propósito

Evaluar de forma estructurada la calidad técnica y el impacto operacional de la solución IA antes del cierre. Combina análisis crítico de métricas, revisión del código y retroalimentación del equipo operacional. Identifica si la solución es robusta, mantenible e interpretable antes de estandarizarla.

---

## Cuándo usar este skill

- El test fue completado con resultado APROBADO o APROBADO CON OBSERVACIONES
- Se necesita una revisión formal antes del cierre del proyecto
- El orquestador solicita auditar una solución IA existente

**Prerequisito:** reporte de test completado.

---

## Protocolo de ejecución

### Paso 1 — Revisar el ciclo completo
Leer en orden: `spec` → `plan` → `build-log` → `test-reporte`.
Verificar que el entregable final responde al problema de negocio definido en `spec`.

### Paso 2 — Evaluar calidad técnica

**Para modelos ML:**
- ¿Las métricas son estables o hay alta varianza entre folds?
- ¿El modelo generaliza a datos de períodos distintos al de entrenamiento?
- ¿Hay data leakage? (features que no estarían disponibles en producción)
- ¿El modelo puede reentrenarse cuando lleguen datos nuevos?

**Para agentes GenAI:**
- ¿Los prompts están versionados y documentados?
- ¿El agente maneja correctamente inputs fuera de dominio?
- ¿Los costos de API son aceptables para el volumen esperado?

**Para dashboards:**
- ¿Los datos se actualizan con la frecuencia comprometida?
- ¿El código es mantenible por alguien más del área IA?

**Para cartografía:**
- ¿Las capas tienen metadatos (CRS, fecha, fuente)?
- ¿Los scripts pueden reprocesarse cuando lleguen datos nuevos?

### Paso 3 — Evaluar impacto operacional real
- ¿Cuánto mejoró la métrica de éxito vs. la línea base?
- ¿El equipo operacional adoptó el entregable?
- ¿Hay evidencia de que se tomaron decisiones mejores gracias a esta solución?

### Paso 4 — Recoger retroalimentación
Entrevistar a usuarios del entregable:
- ¿Lo usan? ¿Con qué frecuencia?
- ¿Confían en sus outputs?
- ¿Qué mejoras necesita para el siguiente ciclo?

### Paso 5 — Identificar ajustes
- **Críticos**: deben resolverse antes de estandarizar (data leakage, alucinaciones no detectadas, bug en fórmula)
- **Importantes**: deben incorporarse en la próxima iteración
- **Menores**: backlog para versiones futuras

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_review-ia-[nombre-proyecto].md
```

---

## Plantilla de review IA

```markdown
# Review — Proyecto IA [Nombre]
**Fecha:** YYYY-MM-DD | **Revisado por:** [Nombre]

## Cumplimiento de métricas
| Métrica | Meta | Resultado | ¿Supera baseline? | Evaluación |
|---|---|---|---|---|

## Calidad técnica
| Dimensión | Estado | Hallazgo |
|---|---|---|
| Generalización del modelo | OK / NOK | |
| Ausencia de data leakage | OK / NOK | |
| Mantenibilidad del código | OK / NOK | |
| Documentación | OK / NOK | |

## Adopción operacional
- Usuarios activos: [N]
- Frecuencia de uso: [diaria / semanal / puntual]
- Decisiones tomadas con esta solución: [ejemplos]

## Ajustes identificados
### Críticos (bloquean cierre)
| Hallazgo | Acción | Responsable | Plazo |
|---|---|---|---|

## Decisión: Aprobar cierre / Requiere ajustes
```

---

## Restricciones de este skill

- No recomendar cierre si hay data leakage detectado o alucinaciones críticas no controladas
- La adopción operacional es un criterio de éxito: un modelo preciso que nadie usa es un proyecto fallido
- Evaluar mantenibilidad: ¿puede el área IA reentrenar o actualizar esto en 6 meses sin el autor original?
