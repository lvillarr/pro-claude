# Skill: review — Síntesis y Control de Calidad (Orquestador)

## Propósito

Integrar los outputs de los agentes, verificar su calidad y coherencia, identificar inconsistencias o vacíos, y preparar la síntesis ejecutiva antes de la entrega final. Es el punto de control de calidad del orquestador: nada llega al usuario sin haber pasado por este filtro.

---

## Cuándo usar este skill

- Todos los agentes han completado sus entregas (EO, IA, TD según el plan)
- Se necesita integrar outputs de múltiples fuentes en una síntesis coherente
- Se detectan inconsistencias entre los entregables de los agentes
- El usuario solicita validar la calidad de un entregable antes de presentarlo a gerencia

**El orquestador sintetiza y eleva: no reformatea, analiza y conecta.**

---

## Protocolo de ejecución

### Paso 1 — Leer y verificar todos los entregables
Para cada archivo de salida de agente:
```
read_file datos/YYYY-MM-DD_[entregable-EO].md
read_file datos/YYYY-MM-DD_[entregable-IA].ext
read_file datos/YYYY-MM-DD_[entregable-TD].py (o .md)
```

Verificar que cada entregable:
- [ ] Responde la tarea delegada en el plan
- [ ] Incluye fecha, área responsable y próximo paso
- [ ] Tiene los KPIs o métricas solicitadas con números reales (no estimados sin fuente)
- [ ] No asume ni inventa datos sin declararlo

### Paso 2 — Cruzar hallazgos entre agentes

Buscar:
- **Consistencias que refuerzan la hipótesis**: cuando EO, IA y TD llegan a conclusiones alineadas, el hallazgo es más robusto
- **Inconsistencias que requieren explicación**: ¿el análisis de IA contradice el diagnóstico de EO? Investigar antes de consolidar
- **Vacíos que deben declararse**: si ningún agente pudo responder una parte del mandato, decirlo explícitamente

### Paso 3 — Evaluar calidad por dimensión

| Dimensión | Criterio | Estado |
|---|---|---|
| Completitud | ¿Todos los entregables del plan llegaron? | ✅ / ⚠️ / ❌ |
| Coherencia | ¿Los hallazgos entre agentes son consistentes? | |
| Cuantificación | ¿Los impactos están en números, no en adjetivos? | |
| Accionabilidad | ¿El entregable permite tomar una decisión concreta? | |
| Nivel ejecutivo | ¿El lenguaje es apropiado para la audiencia? | |

### Paso 4 — Estructurar la síntesis ejecutiva (pirámide de Minto)

```
1. SITUACIÓN
   [Contexto que el usuario ya conoce. 2-3 líneas.]

2. COMPLICACIÓN
   [Por qué la situación actual es problemática o urgente. Con datos.]

3. PREGUNTA IMPLÍCITA
   [¿Qué debemos hacer? — esta es la pregunta que la síntesis responde]

4. HALLAZGOS CLAVE
   [Máximo 3. Cada uno cuantificado. Ordenados por impacto.]
   → Hallazgo 1: [dato] → implica [consecuencia]
   → Hallazgo 2: [dato] → implica [consecuencia]
   → Hallazgo 3: [dato] → implica [consecuencia]

5. RECOMENDACIONES
   [Máximo 3. Accionables, con responsable y plazo.]
   → Acción 1: [qué] — [quién] — [cuándo]
   → Acción 2: [qué] — [quién] — [cuándo]

6. PRÓXIMOS PASOS
   [Qué debe decidir o aprobar el usuario para continuar]
```

### Paso 5 — Verificar antes de entregar al usuario

Checklist final:
- [ ] ¿El resumen ejecutivo cabe en media página?
- [ ] ¿Cada recomendación tiene responsable, plazo y criterio de éxito?
- [ ] ¿Los números son consistentes a lo largo de todo el documento?
- [ ] ¿Se declararon las limitaciones y supuestos?
- [ ] ¿El lenguaje es apropiado para la audiencia (gerencia vs. equipo técnico)?

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_review-orq-[nombre-iniciativa].md
```

---

## Restricciones de este skill

- No presentar al usuario resultados con inconsistencias no resueltas entre agentes
- Si un entregable de agente es incompleto, devolver con instrucciones específicas de qué falta — no completarlo el orquestador
- Los adjetivos sin número (mejora "significativa", impacto "alto") no pasan el filtro de calidad
- El orquestador sintetiza: no copia y pega los outputs de los agentes, los transforma en insight ejecutivo
