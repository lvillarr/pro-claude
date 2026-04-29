# Skill: build — Construccion de entregables EO

> **Agente:** EO — Excelencia Operacional

## Proposito

Producir los artefactos tecnicos del proyecto: BPMN TO-BE en XML, diccionario de KPIs, dashboard HTML con branding Arauco, A3/PDCA, plan de accion con responsables y plazos. Cada entregable debe ser funcional e independiente del agente que lo genero.

## Cuando usar este skill

- Plan aprobado y diagnostico completado (BPMN AS-IS validado, causa raiz confirmada)
- El spec define el tipo de solucion: Lean, BPMN, KPI o PMBoK
- Se requiere un documento ejecutivo para presentar a la Subgerencia MC

**Prerequisito:** `datos/YYYY-MM-DD_spec-*.md` en estado APROBADO y `datos/YYYY-MM-DD_plan-*.md` en estado APROBADO. Si la solucion es BPMN, el AS-IS debe estar documentado y validado.

## Protocolo de ejecucion

### Paso 1 — Identificar entregables del build segun tipo de solucion

| Tipo de solucion | Entregables principales |
|---|---|
| Lean / Kaizen | A3 completo, plan de accion con fechas, checklist 5S si aplica |
| BPMN / Rediseno | BPMN TO-BE en XML + descripcion de cambios + analisis de valor |
| KPI / Gobierno de datos | Diccionario de KPIs (fórmula, fuente, meta, frecuencia, responsable) |
| PMBoK / Proyecto | Charter, EDT detallada, matrix RACI si > 2 areas |
| Dashboard ejecutivo | HTML standalone con branding Arauco (sin dependencias externas) |

### Paso 2 — BPMN TO-BE (cuando aplica)

Generar XML BPMN 2.0 valido. Estructura minima:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             targetNamespace="http://arauco.com/mc/[proceso]">
  <process id="[id]" name="[nombre TO-BE]" isExecutable="false">
    <!-- StartEvent, Tasks, Gateways, EndEvent -->
    <!-- Marcar actividades eliminadas con annotation: "ELIMINADO - desperdicio puro" -->
    <!-- Marcar automatizaciones con annotation: "AUTOMATIZADO - TD" -->
  </process>
</definitions>
```

Regla: cada tarea del BPMN TO-BE debe tener clasificacion de valor:
- `VA` — Valor agregado (cliente o negocio)
- `NVA-N` — No valor agregado pero necesario (regulatorio, control)
- `NVA` — Desperdicio puro — candidato a eliminar

### Paso 3 — Diccionario de KPIs (cuando aplica)

Usar `write_file` o `excel-mcp` para generar tabla. Columnas obligatorias:

| KPI | Definicion | Formula | Unidad | Fuente | Meta | Frecuencia | Responsable | Sistema de reporte |
|---|---|---|---|---|---|---|---|---|

Ejemplo:
| OEE Linea 3 | Eficiencia global del equipo | Disp x Rend x Cal | % | Historian / SAP PM | >= 85,0% | Diario (turno) | Jefe Mantenimiento | Power BI |

### Paso 4 — A3 / PDCA (cuando aplica)

El A3 sigue la estructura de 8 secciones en formato markdown. Ver plantilla abajo.

### Paso 5 — Plan de accion

Tabla con: ID, accion, responsable (cargo), plazo, recurso, indicador de cierre, estado.

### Paso 6 — Dashboard HTML con branding Arauco

Paleta Arauco: verde `#007A33`, negro `#1A1A1A`, gris claro `#F4F4F4`, blanco `#FFFFFF`.
Tipografia: sistema (`-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`).
Requisito: funciona abriendo el `.html` directamente — sin CDN, sin servidor.

### Paso 7 — Guardar entregables

```
datos/YYYY-MM-DD_bpmn-[proceso]-tobe.xml
datos/YYYY-MM-DD_kpi-[area]-diccionario.md
datos/YYYY-MM-DD_a3-[area]-[problema].md
datos/YYYY-MM-DD_dashboard-[area].html
datos/YYYY-MM-DD_plan-accion-[area].md
```

## Plantilla de A3

```markdown
# A3 — [Titulo del problema]

**Area:** [Planta / Linea / Equipo]
**Fecha inicio:** YYYY-MM-DD
**Responsable:** [Cargo]
**Version:** 1.0

---

## 1. Situacion actual

[Descripcion factual del problema con cifras del spec. Sin causas ni soluciones aqui.]

- KPI actual: [valor con fuente]
- Perdida cuantificada: [h, ton, $ — con fuente]
- Periodo: [inicio — fin]

---

## 2. Meta

| KPI | Actual | Meta | Plazo |
|---|---|---|---|
| [KPI] | [valor] | [meta] | [fecha] |

---

## 3. Analisis de causa raiz

### 5 Porques

1. ¿Por que ocurre [sintoma]? — [respuesta con evidencia]
2. ¿Por que [respuesta 1]? — [respuesta con evidencia]
3. ¿Por que [respuesta 2]? — [respuesta con evidencia]
4. ¿Por que [respuesta 3]? — [respuesta con evidencia]
5. ¿Por que [respuesta 4]? — **Causa raiz: [enunciado]**

### Diagrama Ishikawa (categorias)

| Categoria | Causa identificada | Evidencia |
|---|---|---|
| Maquina | | |
| Metodo | | |
| Mano de obra | | |
| Material | | |
| Medicion | | |
| Medio ambiente | | |

---

## 4. Contramedidas

| ID | Accion | Tipo (elimina / mitiga / detecta) | Responsable | Plazo | Costo estimado |
|---|---|---|---|---|---|

---

## 5. Plan de implementacion

[Referencia al plan: datos/YYYY-MM-DD_plan-*.md]

---

## 6. Resultados esperados

| KPI | Antes | Despues | Delta esperado |
|---|---|---|---|

---

## 7. Seguimiento

| Fecha | KPI medido | Valor | Desviacion | Accion correctiva |
|---|---|---|---|---|

---

## 8. Estandarizacion

[Que cambia en el procedimiento estandar, checklist o SGL. Referencia al entregable ship.]
```

## Plantilla de Plan de Accion

```markdown
# Plan de Accion — [Area / Problema]

**Fecha:** YYYY-MM-DD
**Referencia A3:** datos/YYYY-MM-DD_a3-*.md

| ID | Accion | Responsable | Plazo | Recurso necesario | Indicador de cierre | Estado |
|---|---|---|---|---|---|---|
| A1 | | | YYYY-MM-DD | | | PENDIENTE |
| A2 | | | YYYY-MM-DD | | | PENDIENTE |
```

## Restricciones de este skill

- BPMN XML debe ser valido segun BPMN 2.0; no inventar elementos del esquema
- Cada tarea del BPMN TO-BE debe tener clasificacion de valor (VA / NVA-N / NVA)
- KPIs sin formula, fuente o responsable no se incluyen en el diccionario — quedan marcados como INCOMPLETOS
- Dashboard HTML: sin dependencias externas (no CDN, no APIs, no fuentes de Google)
- Plan de accion: plazo sin fecha concreta no es aceptable — usar YYYY-MM-DD
- A3: la seccion de causa raiz no puede estar vacia ni contener hipotesis sin evidencia de GEMBA o datos
- No mezclar entregables en un solo archivo; un archivo por tipo de entregable
- Formato numerico chileno en todos los entregables: `1.234,5 h`, `87,3%`, `$12.500`
