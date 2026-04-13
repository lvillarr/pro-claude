# Skill: review — Revisión y Auditoría de Mejoras

## Propósito

Evaluar de forma estructurada los resultados del piloto y la calidad de los entregables antes del cierre formal. Combina análisis crítico de datos, revisión de proceso y retroalimentación del equipo operacional. Identifica qué funcionó, qué no funcionó y qué debe ajustarse antes de estandarizar. Es el control de calidad del ciclo de mejora.

---

## Cuándo usar este skill

- El test/piloto fue completado (skill `test` con resultado APROBADO o APROBADO CON OBSERVACIONES)
- Se necesita una revisión formal antes del cierre del proyecto
- El orquestador solicita auditar un proceso o iniciativa existente
- Se detectan desviaciones post-implementación que requieren revisión estructurada

**Prerequisito:** reporte de test completado y disponible en `datos/`.

---

## Protocolo de ejecución

### Paso 1 — Revisar todos los entregables del ciclo
Leer en orden:
1. `datos/YYYY-MM-DD_spec-[iniciativa].md` → ¿el problema original fue atendido?
2. `datos/YYYY-MM-DD_plan-[iniciativa].md` → ¿se ejecutó según lo planificado?
3. `datos/YYYY-MM-DD_build-log-[iniciativa].md` → ¿los entregables fueron los comprometidos?
4. `datos/YYYY-MM-DD_test-reporte-[iniciativa].md` → ¿los KPIs se cumplieron?

### Paso 2 — Evaluar el impacto operacional real
Comparar línea base vs. resultado post-piloto:
- ¿Cuánto mejoró cada KPI de éxito?
- ¿Hubo impacto positivo no planificado? ¿Negativo?
- ¿El impacto es sostenible en el tiempo o fue puntual?
- ¿Qué registra el SGL desde la implementación?

### Paso 3 — Revisar la calidad del proceso TO-BE
GEMBA de auditoría (si aplica):
- ¿El nuevo proceso se sigue de forma consistente por todos los turnos?
- ¿Hay variabilidad entre operadores o contratistas?
- ¿El estándar documentado en BPMN refleja lo que realmente se hace?
- ¿Las herramientas digitales son utilizadas correctamente?

### Paso 4 — Recoger retroalimentación del equipo
Entrevistar o encuestar a:
- Operadores que usaron el nuevo proceso
- Supervisores de turno
- Analistas de datos que usan los KPIs
- Contratistas afectados (si aplica)

Preguntas clave:
- ¿Qué funcionó bien?
- ¿Qué fue difícil o confuso?
- ¿Qué cambiarías?
- ¿Usarías esto de nuevo?

### Paso 5 — Identificar ajustes necesarios
Clasificar hallazgos:
- **Críticos**: deben corregirse antes de estandarizar (volver a `build` si es necesario)
- **Importantes**: deben incorporarse en el estándar o la próxima iteración
- **Menores**: deseables pero no bloquean el cierre

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_review-[nombre-iniciativa].md
```

---

## Plantilla de review

```markdown
# Review — [Nombre Iniciativa]
**Fecha:** YYYY-MM-DD
**Revisado por:** [Nombre, cargo]
**Estado de la iniciativa al momento del review:** Post-piloto / Post-implementación

---

## 1. Cumplimiento de KPIs de éxito

| KPI | Meta | Resultado | % cumplimiento | Evaluación |
|---|---|---|---|---|
| | | | | Logrado / Parcial / No logrado |

**Conclusión general:** [La iniciativa logró su objetivo operacional? Sí / Parcialmente / No]

---

## 2. Cumplimiento del plan de proyecto

| Fase | Planificado | Ejecutado | Desviación | Causa |
|---|---|---|---|---|
| Diagnóstico | | | | |
| Análisis | | | | |
| Build | | | | |
| Piloto | | | | |

---

## 3. Auditoría GEMBA del proceso TO-BE

| Actividad revisada | ¿Se ejecuta según estándar? | Variabilidad observada | Riesgo |
|---|---|---|---|

**Conformidad general del proceso:** Alta / Media / Baja

---

## 4. Retroalimentación del equipo operacional

| Grupo | Punto positivo | Punto de mejora | Solicitud |
|---|---|---|---|
| Operadores | | | |
| Supervisores | | | |
| Analistas | | | |
| Contratistas | | | |

---

## 5. Hallazgos y ajustes necesarios

### Críticos (bloquean el cierre)
| ID | Hallazgo | Ajuste requerido | Responsable | Plazo |
|---|---|---|---|---|

### Importantes (incorporar en estándar)
| ID | Hallazgo | Acción | Responsable |
|---|---|---|---|

### Menores (próxima iteración)
| ID | Hallazgo | Nota |
|---|---|---|

---

## 6. Evaluación global del ciclo de mejora

| Dimensión | Calificación (1-5) | Comentario |
|---|---|---|
| Calidad del diagnóstico | | |
| Robustez del diseño TO-BE | | |
| Efectividad del piloto | | |
| Adopción del equipo operacional | | |
| Calidad de los datos | | |
| Impacto en KPIs | | |

---

## 7. Decisión de cierre
**Decisión:** Aprobar cierre y estandarizar / Requiere ajustes antes de cerrar

**Condiciones para cerrar (si hay ajustes pendientes):**
- [ ] [Ajuste crítico 1 resuelto]
- [ ] [Ajuste crítico 2 resuelto]
```

---

## Restricciones de este skill

- No se puede recomendar el cierre si hay hallazgos críticos sin plan de resolución
- La retroalimentación de operadores es obligatoria: no se revisa solo con datos, se habla con la gente
- Si el GEMBA de auditoría muestra baja conformidad con el estándar, se debe investigar causa antes de cerrar
- El review evalúa también el proceso de mejora, no solo el resultado: un buen resultado con mal proceso es una lección aprendida
