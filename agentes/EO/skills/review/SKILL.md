# Skill: review — GEMBA de verificacion y analisis de resultados

> **Agente:** EO — Excelencia Operacional

## Proposito

Cerrar el ciclo PDCA: verificar que los resultados del piloto se sostienen en el tiempo, que los operadores adoptaron el nuevo estandar, y que no surgieron desviaciones no previstas. Producir un informe de revision que habilite o bloquea el paso a estandarizacion (ship).

## Cuando usar este skill

- Test completado con veredicto APROBADO o APROBADO CONDICIONAL
- Han transcurrido al menos 2 semanas desde el inicio del piloto (suficiente para detectar regresion)
- El orquestador requiere confirmacion de sostenibilidad antes de estandarizar
- Se detectaron desviaciones durante el test que deben verificarse resueltas

**Prerequisito:** `datos/YYYY-MM-DD_test-*.md` con veredicto APROBADO o APROBADO CONDICIONAL. Datos del periodo post-piloto disponibles en `arauco_mc.db` o SGL.

## Protocolo de ejecucion

### Paso 1 — GEMBA de verificacion en terreno

El GEMBA de review es distinto al GEMBA de diagnostico: aqui se verifica adopcion, no se busca causa raiz.

Observar durante un turno real:
1. ¿El operador ejecuta el proceso segun el BPMN TO-BE sin desviaciones?
2. ¿El registro en SGL sigue el nuevo flujo sin omisiones?
3. ¿Los KPIs se miden con la frecuencia definida en el diccionario?
4. ¿Aparecieron nuevos desperdicios o pasos no previstos en el TO-BE?
5. ¿El jefe de turno puede explicar el nuevo estandar sin consultar el documento?

Documentar cada observacion con: actividad BPMN de referencia, desviacion detectada (si existe), severidad (critica / menor / informativa).

### Paso 2 — Obtener datos del periodo de seguimiento

```sql
-- Tendencia post-piloto: comparar con piloto y linea base
SELECT 
    strftime('%Y-%W', fecha) AS semana,
    equipo,
    SUM(minutos_perdidos) / 60.0 AS horas_perdidas,
    COUNT(*) AS n_eventos
FROM perdidas
WHERE equipo = '[id_equipo]'
  AND fecha >= '[fecha_inicio_piloto]'
GROUP BY semana, equipo
ORDER BY semana;
```

### Paso 3 — Analizar resultados vs. hipotesis del spec

Para cada hipotesis de causa raiz del spec y del A3:

| Hipotesis | Evidencia esperada | Evidencia observada | Confirmada |
|---|---|---|---|
| "La causa raiz es [X]" | KPI Y mejora >= Z% | KPI Y mejora X,X% | SI / NO / PARCIAL |

Si una hipotesis no se confirma: documentar la discrepancia y proponer ajuste al A3 antes de estandarizar.

### Paso 4 — Evaluar adopcion operacional

Escala de adopcion (usar para cada elemento del TO-BE):
- **3 — Adoptado:** operador ejecuta sin consultar, jefe de turno valida
- **2 — Parcial:** se ejecuta con asistencia o con variaciones menores aceptables
- **1 — No adoptado:** se omite, se ejecuta distinto o se usa el metodo anterior

Adopcion promedio < 2,5: no habilitar ship hasta resolver.

### Paso 5 — Analisis de desviaciones del estandar

Por cada desviacion detectada en el GEMBA:

| ID | Actividad BPMN | Desviacion observada | Severidad | Impacto en KPI | Accion recomendada |
|---|---|---|---|---|---|
| D1 | [tarea TO-BE] | [descripcion] | Critica / Menor | SI / NO | [accion con plazo] |

Desviacion critica: bloquea el ship hasta resolverse.

### Paso 6 — Emitir habilitacion para ship

- **HABILITADO:** resultados sostenidos, adopcion >= 2,5, sin desviaciones criticas
- **HABILITADO CON CONDICIONES:** adopcion parcial o desviaciones menores con plan de cierre claro
- **BLOQUEADO:** regresion en KPIs, desviacion critica sin resolver, o hipotesis de causa raiz no confirmada

### Paso 7 — Guardar informe de review

```
datos/YYYY-MM-DD_review-[area]-[equipo].md
```

## Plantilla de Informe de Review

```markdown
# Review EO — [Area / Equipo / Proceso]

**Fecha GEMBA:** YYYY-MM-DD
**Referencia test:** datos/YYYY-MM-DD_test-[area]-*.md
**Responsable:** [Cargo]
**Habilitacion para ship:** HABILITADO | HABILITADO CON CONDICIONES | BLOQUEADO

---

## Contexto

| Campo | Valor |
|---|---|
| Linea / Equipo | |
| Periodo de seguimiento | YYYY-MM-DD a YYYY-MM-DD |
| Semanas post-piloto | [N semanas] |
| Turnos observados en GEMBA | [N turnos — fechas] |

---

## Resultados KPI — Tendencia post-piloto

| KPI | Linea base | Piloto | Post-piloto | Meta | Tendencia |
|---|---|---|---|---|---|
| | | | | | Sostenida / Regresion / Mejora adicional |

---

## Analisis de hipotesis de causa raiz

| Hipotesis (del A3) | Confirmada | Evidencia | Observacion |
|---|---|---|---|

---

## Adopcion operacional

| Elemento TO-BE | Score (1-3) | Observacion |
|---|---|---|
| [Actividad 1] | | |
| [Actividad 2] | | |

**Promedio de adopcion:** X,X / 3,0

---

## Desviaciones detectadas (GEMBA)

| ID | Actividad BPMN | Desviacion | Severidad | Impacto KPI | Accion |
|---|---|---|---|---|---|

---

## Observaciones abiertas del test (condiciones pendientes)

[Listar condiciones del veredicto APROBADO CONDICIONAL del test. Indicar si fueron resueltas.]

| Condicion | Estado | Evidencia |
|---|---|---|

---

## Habilitacion para ship

**Estado:** HABILITADO | HABILITADO CON CONDICIONES | BLOQUEADO

**Fundamento:**
- [KPI: tendencia sostenida / regresion / mejora adicional]
- [Adopcion: promedio X,X — describe el punto mas debil]
- [Hipotesis confirmadas: N de M]

**Condiciones para ship (si aplica):**
| Condicion | Responsable | Plazo |
|---|---|---|

---

## Firma de revision

| Rol | Cargo | Fecha | Firma |
|---|---|---|---|
| Responsable EO | Jefe EO | | |
| Validador terreno | Jefe de Turno | | |
| Supervisor MC | Subgerente MC | | |
```

## Restricciones de este skill

- GEMBA de review es obligatorio: no habilitar ship solo con datos de sistema sin observacion directa
- Periodo minimo de seguimiento: 2 semanas post-piloto; con justificacion puede reducirse a 1 semana en contextos urgentes
- Si la adopcion promedio es < 2,5 el ship queda BLOQUEADO independientemente de los KPIs
- Desviacion critica (seguridad, calidad de producto, perdida mayor no prevista) bloquea ship sin excepcion
- No actualizar el A3 sin citar la evidencia del periodo de seguimiento
- Hipotesis no confirmada no invalida el proyecto si el KPI mejora, pero debe documentarse para lecciones aprendidas (ship)
- Informe de review debe referenciar explicitamente el informe de test; no puede existir review sin test previo
