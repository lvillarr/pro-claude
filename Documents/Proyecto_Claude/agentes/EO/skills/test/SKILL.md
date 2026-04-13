# Skill: test — Verificación y Validación de Mejoras

## Propósito

Verificar en terreno que la solución construida funciona como se diseñó y que los KPIs de éxito se están moviendo en la dirección correcta. Combina observación directa (GEMBA de validación), análisis de datos y comparación contra la línea base definida en `spec`. No avanza a `review` si la evidencia no es suficiente.

---

## Cuándo usar este skill

- Los entregables del skill `build` están completos y validados por el equipo técnico
- Se necesita ejecutar el piloto de la mejora en terreno
- Se requiere validar que los datos fluyen correctamente por los sistemas (SGL, SAP, Historian)
- Se debe confirmar si los KPIs de éxito se cumplen antes del cierre

**Prerequisito:** build completado con todos los entregables aprobados.

---

## Protocolo de ejecución

### Paso 1 — Definir el plan de prueba
Antes de ir a terreno, definir:
- ¿Qué se va a probar? (proceso, herramienta, KPI, integración de sistema)
- ¿Dónde? (faena, línea, equipo, área específica)
- ¿Por cuánto tiempo? (duración mínima del piloto para tener datos representativos)
- ¿Con quién? (operadores, supervisores, contratistas involucrados)
- ¿Cuál es el criterio de aprobación del test?

### Paso 2 — GEMBA de validación
Observar directamente en terreno:
- ¿El proceso TO-BE se ejecuta como fue diseñado en el BPMN?
- ¿Los operadores tienen las herramientas y el conocimiento necesario?
- ¿Hay desviaciones respecto al estándar? ¿Cuáles y por qué?
- ¿Los sistemas digitales están registrando correctamente (SGL, SAP)?

Registrar observaciones con: actividad, quién, cuándo, desviación observada, causa probable.

### Paso 3 — Validar datos y KPIs
Para cada KPI de éxito definido en `spec`:

| KPI | Línea base | Meta | Valor durante piloto | Tendencia | ¿Cumple? |
|---|---|---|---|---|---|

Reglas de validación de datos:
- Completitud: ¿todos los registros esperados están en el sistema?
- Consistencia: ¿los datos del SGL coinciden con lo observado en GEMBA?
- Exactitud: ¿las fórmulas de cálculo producen resultados correctos?
- Oportunidad: ¿los datos están disponibles en la frecuencia comprometida?

### Paso 4 — Probar integraciones de sistemas
Si la mejora involucra sistemas digitales:
- Verificar que los flujos de datos entre sistemas funcionan (SGL ↔ SAP, Historian → Power BI)
- Confirmar que los roles correctos tienen acceso a las herramientas
- Documentar errores o excepciones encontradas

### Paso 5 — Registrar resultado del test
Clasificar el resultado:
- **APROBADO**: todos los criterios de aceptación cumplidos → avanzar a `review`
- **APROBADO CON OBSERVACIONES**: criterios principales cumplidos, ajustes menores → documentar y avanzar
- **REPROBADO**: criterios críticos no cumplidos → volver a `build` con hallazgos documentados

### Paso 6 — Entregar
```
datos/YYYY-MM-DD_test-reporte-[nombre-iniciativa].md
```

---

## Plantilla de reporte de test

```markdown
# Reporte de Test / Validación — [Nombre Iniciativa]
**Fecha piloto:** YYYY-MM-DD a YYYY-MM-DD
**Área / Faena:** [Nombre del área o faena]
**Responsable EO:** [Nombre]
**Observadores en terreno:** [Nombres]

---

## Plan de prueba
**Qué se probó:** [proceso / herramienta / integración]
**Duración:** [N días / turnos]
**Criterio de aprobación:** [descripción de cuándo se considera exitoso]

---

## Resultados de KPIs

| KPI | Línea base | Meta | Valor piloto | Tendencia | Cumple |
|---|---|---|---|---|---|
| | | | | ↑ / ↓ / → | Sí / No |

---

## Observaciones GEMBA de validación

| Actividad observada | ¿Conforme con TO-BE? | Desviación (si la hay) | Causa probable |
|---|---|---|---|

---

## Validación de calidad de datos (D.A.M.A.)

| Dimensión | Estado | Hallazgo |
|---|---|---|
| Completitud | OK / NOK | |
| Consistencia | OK / NOK | |
| Exactitud | OK / NOK | |
| Oportunidad | OK / NOK | |

---

## Problemas encontrados

| ID | Descripción | Impacto | Acción requerida | Responsable |
|---|---|---|---|---|

---

## Resultado final del test
**Estado:** APROBADO / APROBADO CON OBSERVACIONES / REPROBADO

**Justificación:**
[Resumen de por qué se toma esta decisión]

**Próximo paso:** Avanzar a `review` / Volver a `build` (ajuste: [descripción])
```

---

## Restricciones de este skill

- No se puede cerrar un test como "aprobado" solo con datos del sistema: se requiere confirmación GEMBA
- La duración mínima del piloto debe ser representativa del ciclo operacional (al menos 1 semana completa o 3 turnos completos)
- Si un KPI crítico no muestra tendencia positiva, el test es REPROBADO aunque otros KPIs mejoren
- Las desviaciones del proceso TO-BE observadas en terreno deben quedar registradas, no ignoradas
