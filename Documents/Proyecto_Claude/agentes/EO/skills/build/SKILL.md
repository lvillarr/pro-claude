# Skill: build — Construcción e Implementación de Mejoras

## Propósito

Ejecutar la fase de construcción de la iniciativa de mejora: modelar el proceso TO-BE en BPMN, diseñar KPIs, configurar herramientas Lean, generar scripts ETL, construir plantillas de seguimiento y preparar los entregables que serán validados en el piloto. Es la fase de producción técnica antes de ir a terreno.

---

## Cuándo usar este skill

- El charter del proyecto está aprobado (skill `plan` completado)
- Se necesita diseñar el proceso futuro (BPMN TO-BE) a partir del análisis AS-IS
- Se solicita construir una herramienta: dashboard, plantilla de KPI, script de datos
- Se debe preparar un evento Kaizen con materiales, formularios y estándares

**Prerequisito:** plan aprobado con EDT y hitos definidos.

---

## Protocolo de ejecución

### Paso 1 — Revisar entradas
Leer antes de construir:
- `datos/YYYY-MM-DD_spec-[iniciativa].md` → problema y KPIs objetivo
- `datos/YYYY-MM-DD_plan-[iniciativa].md` → alcance y entregables comprometidos
- Proceso AS-IS documentado (BPMN o descripción de terreno)

### Paso 2 — Modelar proceso TO-BE (si aplica)
Usar el skill `bpmn-modeling` para:
- Eliminar actividades NVA identificadas en el AS-IS
- Rediseñar flujos con menor desperdicio
- Incorporar integración con sistemas digitales (SGL, SAP, Planex)
- Documentar cambios respecto al AS-IS en tabla comparativa

### Paso 3 — Diseñar o actualizar KPIs
Para cada KPI comprometido en la spec:
```
Nombre:       [nombre del indicador]
Definición:   [qué mide exactamente]
Fórmula:      [numerador / denominador × factor]
Fuente:       [sistema o registro de origen]
Frecuencia:   [diaria / semanal / mensual / por turno]
Meta:         [valor objetivo con plazo]
Línea base:   [valor actual medido]
Responsable:  [cargo que mide y reporta]
```

### Paso 4 — Construir herramientas y entregables
Según el tipo de iniciativa, construir:

| Tipo de entregable | Herramienta | Destino |
|---|---|---|
| Dashboard de KPIs | Plantilla Excel / Power BI layout | `datos/plantillas/` |
| Script ETL de datos | Python / SQL | `datos/scripts/` |
| Diagrama BPMN TO-BE | XML BPMN 2.0 | `datos/` |
| Plan de acción Kaizen | Plantilla A3 | `datos/plantillas/` |
| Estándar de trabajo | Documento operacional | `datos/plantillas/` |
| Lista de verificación 5S | Checklist por área | `datos/plantillas/` |

### Paso 5 — Documentar cambios implementados
Registrar en el log de implementación:
- Qué se construyó, cuándo y quién lo validó
- Desviaciones respecto al plan (si las hay)
- Decisiones de diseño tomadas y su justificación

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_proceso-bpmn-[nombre]-to-be.bpmn
datos/YYYY-MM-DD_kpi-[nombre-iniciativa].xlsx
datos/scripts/YYYY-MM-DD_etl-[descripcion].py
datos/plantillas/YYYY-MM-DD_plantilla-[tipo].xlsx
datos/YYYY-MM-DD_build-log-[nombre-iniciativa].md
```

---

## Plantilla de log de construcción

```markdown
# Build Log — [Nombre Iniciativa]
**Fecha inicio build:** YYYY-MM-DD
**Fecha fin build:** YYYY-MM-DD
**Responsable:** [Nombre]

---

## Entregables construidos

| Entregable | Archivo | Fecha | Estado | Validado por |
|---|---|---|---|---|
| BPMN TO-BE | datos/... | | Completo / En revisión | |
| KPI dashboard | datos/... | | | |
| Script ETL | datos/scripts/... | | | |

---

## Cambios respecto al proceso AS-IS

| Actividad AS-IS | Cambio aplicado | Tipo (eliminar/automatizar/rediseñar) | Impacto esperado |
|---|---|---|---|

---

## KPIs diseñados

| KPI | Fórmula | Meta | Fuente | Responsable |
|---|---|---|---|---|

---

## Decisiones de diseño
[Registro de decisiones no obvias: por qué se eligió esta solución, qué alternativas se descartaron y por qué]

---

## Criterio de paso a test/piloto
- [ ] BPMN TO-BE revisado por al menos un operador clave
- [ ] KPIs con fórmula, fuente y responsable definidos
- [ ] Herramientas probadas con datos reales (aunque sea muestra)
- [ ] Equipo de terreno informado sobre el piloto
```

---

## Restricciones de este skill

- No construir sin leer el AS-IS: no se puede diseñar el TO-BE sin entender el proceso actual
- Todo KPI construido debe tener fórmula, fuente y responsable antes de pasar a `test`
- Los scripts ETL deben probarse con datos reales del SGL o sistema fuente, no con datos simulados
- El BPMN TO-BE debe ser revisado por al menos un actor del proceso antes de ir a piloto
