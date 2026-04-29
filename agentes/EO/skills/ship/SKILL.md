# Skill: ship — Estandarizacion, registro SGL y cierre formal

> **Agente:** EO — Excelencia Operacional

## Proposito

Convertir los resultados validados en estandar operacional sostenible: actualizar procedimientos, registrar en SGL, documentar lecciones aprendidas y cerrar formalmente el proyecto con hand-off al area responsable de mantenerlo.

## Cuando usar este skill

- Review con habilitacion HABILITADO o HABILITADO CON CONDICIONES (condiciones resueltas)
- El ciclo PDCA esta completo: spec, plan, build, test, review ejecutados y documentados
- Se requiere acta de cierre para proyecto PMBoK
- Se necesita registrar la mejora como oportunidad cerrada en SGL

**Prerequisito:** `datos/YYYY-MM-DD_review-*.md` con habilitacion HABILITADO (o HABILITADO CON CONDICIONES con evidencia de cierre de condiciones). Sin este documento, no hay ship.

## Protocolo de ejecucion

### Paso 1 — Consolidar lecciones aprendidas

Revisar todos los artefactos del ciclo: spec, plan, build, test, review. Extraer:
- Que funciono (conservar en proyectos futuros)
- Que no funciono o causo retraso (evitar)
- Supuestos del spec que resultaron incorrectos
- Riesgos del plan que se materializaron y como se resolvieron
- Brechas en la calidad de datos (D.A.M.A.) que afectaron el diagnostico

### Paso 2 — Actualizar o crear procedimiento estandar

Por cada actividad del BPMN TO-BE que cambia respecto al AS-IS:
- Actualizar el procedimiento operacional existente (si hay archivo en `datos/plantillas/`)
- O crear un nuevo procedimiento con la plantilla EO estandar
- Incluir: objetivo, alcance, roles, pasos numerados, criterio de calidad, frecuencia

Si el proceso interactua con SGL, SAP PM o Historian: documentar el punto de integracion en el procedimiento.

### Paso 3 — Actualizar checklists operacionales

Para cada checklist impactado por el cambio:
- Agregar / eliminar / modificar items segun el BPMN TO-BE
- Version y fecha de actualizacion visibles en el encabezado
- Si hay checklist en SGL: solicitar al administrador del sistema la actualizacion

### Paso 4 — Registrar en SGL

La entrada SGL de cierre debe contener:
- Tipo de registro: "Oportunidad cerrada" o "Mejora implementada" (segun el catalogo SGL vigente)
- Area y equipo
- Periodo del problema (del spec)
- Causa raiz confirmada
- Contramedida implementada
- KPI impactado: valor antes / despues
- Responsable del estandar (quien mantiene la mejora a futuro)
- Referencias a archivos en `datos/`

### Paso 5 — Hand-off formal al area

El hand-off transfiere la responsabilidad del estandar al area operacional. Debe incluir:
- Quienes reciben: jefe de area, jefe de turno, analista de datos
- Que reciben: lista de entregables, donde estan en `datos/`, acceso confirmado
- Compromisos del area: frecuencia de medicion del KPI, actualizacion del SGL, revision periodica
- Proxima revision programada (fecha para verificar sostenibilidad en 30/60/90 dias)

### Paso 6 — Acta de cierre (si es proyecto PMBoK)

Para proyectos medianos y grandes: generar acta formal con firmas del responsable EO y del Subgerente MC.

### Paso 7 — Guardar artefactos de ship

```
datos/YYYY-MM-DD_lecciones-[area]-[proyecto].md
datos/YYYY-MM-DD_procedimiento-[proceso].md
datos/YYYY-MM-DD_checklist-[proceso].md
datos/YYYY-MM-DD_cierre-[proyecto].md
```

### Paso 8 — Emitir ENTREGA EO al orquestador

```
ENTREGA EO:
Archivo(s): [lista de todos los artefactos del ciclo completo]
Hallazgos clave:
  1. [KPI principal: valor antes → despues, delta %]
  2. [Causa raiz confirmada con evidencia]
  3. [Adopcion operacional: score promedio]
Causa raiz: [enunciado final confirmado por GEMBA y datos]
Limitaciones: [datos con cobertura parcial, supuestos no verificados, riesgos residuales]
Plan de accion: [seguimiento a 30/60/90 dias — responsable y criterio de cierre]
```

## Plantilla de Lecciones Aprendidas

```markdown
# Lecciones Aprendidas — [Proyecto / Iniciativa]

**Fecha cierre:** YYYY-MM-DD
**Area:** [Planta / Linea / Departamento]
**Responsable EO:** [Cargo]
**Duracion total del ciclo:** [N semanas desde spec hasta ship]

---

## Resumen ejecutivo

| Campo | Valor |
|---|---|
| Problema abordado | [del spec — 1 linea] |
| Causa raiz confirmada | [del A3] |
| KPI principal antes | [valor + fuente] |
| KPI principal despues | [valor + fuente] |
| Delta | [absoluto y %] |
| Meta spec | [valor] |
| Meta alcanzada | SI / NO / PARCIAL |

---

## Que funciono bien

| Aspecto | Descripcion | Aplicar en |
|---|---|---|
| [Metodologia / Tool / Coordinacion] | | [Proximos proyectos similares] |

---

## Que no funciono o causo retraso

| Aspecto | Descripcion | Causa | Correccion para el futuro |
|---|---|---|---|

---

## Supuestos del spec que resultaron incorrectos

| Supuesto | Realidad encontrada | Impacto en el proyecto |
|---|---|---|

---

## Riesgos que se materializaron

| Riesgo (del plan) | Como se manifesto | Como se resolvio |
|---|---|---|

---

## Calidad de datos (D.A.M.A.)

| Sistema / Tabla | Problema de calidad detectado | Recomendacion |
|---|---|---|
| [SGL / arauco_mc.db / SAP PM] | [completitud, exactitud, oportunidad] | |

---

## Recomendaciones para proyectos futuros similares

1. [Recomendacion concreta]
2. [Recomendacion concreta]
```

## Plantilla de Acta de Cierre

```markdown
# Acta de Cierre — [Proyecto]

**Fecha:** YYYY-MM-DD
**Proyecto:** [nombre]
**Responsable EO:** [Cargo]

---

## Entregables completados

| Entregable | Archivo | Ubicacion | Estado |
|---|---|---|---|
| Spec | datos/YYYY-MM-DD_spec-*.md | datos/ | APROBADO |
| Plan | datos/YYYY-MM-DD_plan-*.md | datos/ | COMPLETADO |
| BPMN TO-BE | datos/YYYY-MM-DD_bpmn-*-tobe.xml | datos/ | ENTREGADO |
| Diccionario KPIs | datos/YYYY-MM-DD_kpi-*.md | datos/ | ENTREGADO |
| A3 | datos/YYYY-MM-DD_a3-*.md | datos/ | CERRADO |
| Informe test | datos/YYYY-MM-DD_test-*.md | datos/ | APROBADO |
| Informe review | datos/YYYY-MM-DD_review-*.md | datos/ | HABILITADO |
| Lecciones aprendidas | datos/YYYY-MM-DD_lecciones-*.md | datos/ | COMPLETADO |
| Procedimiento actualizado | datos/YYYY-MM-DD_procedimiento-*.md | datos/ | VIGENTE |
| Registro SGL | [ID entrada SGL] | SGL | REGISTRADO |

---

## Resultado del proyecto

**Meta del spec:** [KPI objetivo]
**Resultado alcanzado:** [KPI final con fuente]
**Estado:** EXITOSO | EXITOSO PARCIAL | CERRADO SIN META

---

## Hand-off

**Area receptora:** [nombre del area]
**Responsable del estandar:** [cargo]
**Proxima revision de sostenibilidad:** [fecha — 30/60/90 dias]

---

## Firmas

| Rol | Cargo | Fecha | Firma |
|---|---|---|---|
| Responsable EO | Jefe EO | | |
| Receptor del estandar | Jefe de Area | | |
| Validacion MC | Subgerente MC | | |
```

## Restricciones de este skill

- No emitir acta de cierre sin habilitacion del review en estado HABILITADO
- Registro SGL es obligatorio para toda mejora que impacte un KPI operacional: sin SGL el cierre es incompleto
- Lecciones aprendidas no pueden quedar vacias en ninguna de sus secciones criticas (lo que funciono, lo que no, calidad de datos)
- El hand-off debe identificar un responsable de cargo especifico para el estandar; "el area" no es un responsable valido
- Procedimientos actualizados deben tener version y fecha; no sobrescribir sin control de version
- La proxima revision de sostenibilidad debe quedar agendada antes de cerrar — no es opcional
- El informe ENTREGA EO al orquestador debe referenciar todos los archivos del ciclo, no solo los del ship
