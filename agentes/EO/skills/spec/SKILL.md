# Skill: spec — Definicion del problema operacional

> **Agente:** EO — Excelencia Operacional

## Proposito

Estructurar y validar el problema antes de cualquier accion. Sin spec aprobado no hay plan, build ni entregable. Este skill previene diagnosticar con datos incorrectos o atacar el sintoma en lugar de la causa.

## Cuando usar este skill

- Al iniciar cualquier iniciativa de mejora (Kaizen, A3, rediseno de proceso, diseno de KPI)
- Cuando el orquestador entrega un encargo vago: "mejorar el OEE de la linea 3", "reducir paradas"
- Cuando hay inconsistencia entre el dato reportado en SGL y lo observado en terreno
- Cuando se detecta una perdida operacional pero no se conoce su magnitud ni periodo exacto

**Prerequisito:** Acceso al SGL (exportacion o `arauco_mc.db`) o a un archivo fuente con datos del periodo relevante. Sin datos, el spec queda en estado BLOQUEADO hasta que el solicitante los provea.

## Protocolo de ejecucion

### Paso 1 — Leer la fuente disponible

Usar `sqlite` o `read_file` / `excel-mcp` para obtener registros del periodo indicado:

```sql
-- Perdidas por equipo y turno, ultimas 4 semanas
SELECT fecha, equipo, linea, turno, tipo_perdida, minutos_perdidos
FROM perdidas
WHERE fecha >= date('now', '-28 days')
ORDER BY minutos_perdidos DESC
LIMIT 50;
```

Si no hay base de datos, leer el archivo exportado del SGL con `markitdown` o `excel-mcp`. Nunca asumir cifras.

### Paso 2 — Cuantificar la perdida base

Calcular:
- **Perdida total (h):** suma de minutos_perdidos / 60 en el periodo
- **Frecuencia:** numero de eventos
- **Equipos/lineas mas afectados:** top 3 por minutos perdidos
- **Turnos con mayor concentracion**
- **OEE actual** si hay datos de produccion: `OEE = Disponibilidad x Rendimiento x Calidad`

Formato numerico chileno: `1.234,5 h`, `87,3%`.

### Paso 3 — Formular el problema con evidencia

Completar la plantilla de spec (ver abajo). El enunciado del problema sigue la estructura:

> "En [area/linea/equipo], durante [periodo], se registraron [N eventos / X horas] de [tipo de perdida], equivalente a [impacto cuantificado]. La meta es reducir a [meta] para [fecha]."

### Paso 4 — Identificar el tipo de solucion requerida

| Tipo | Cuando aplica |
|---|---|
| **Lean / Kaizen** | Perdida recurrente, causa raiz en el proceso o habito operacional |
| **BPMN / Rediseno** | Proceso sin documentar o con actividades sin valor identificadas |
| **KPI / Gobierno de datos** | Indicador inexistente, mal definido o sin responsable asignado |
| **PMBoK / Proyecto** | Alcance mayor a 4 semanas, requiere presupuesto o multiples areas |
| **GEMBA** | Causa raiz desconocida, datos insuficientes o contradictorios |

### Paso 5 — Validar con el solicitante

Presentar el spec en formato tabla. Esperar confirmacion antes de avanzar a `plan`. Si hay datos faltantes, listarlos explicitamente y marcar el spec como PENDIENTE.

### Paso 6 — Registrar en datos/

```
datos/YYYY-MM-DD_spec-[area]-[tipo].md
```

## Plantilla de Spec

```markdown
# Spec EO — [Area / Equipo / Proceso]

**Fecha:** YYYY-MM-DD
**Solicitante:** [nombre o area]
**Estado:** BORRADOR | APROBADO | BLOQUEADO | PENDIENTE

---

## Problema

| Campo | Valor |
|---|---|
| Area / Linea | [Ej: Planta Celulosa — Linea 3] |
| Equipo principal | [Ej: Bomba P-421, Descortezador L2] |
| Periodo analizado | [Ej: 2026-01-01 a 2026-03-31] |
| Tipo de perdida | [Ej: parada no planificada, baja eficiencia, rechazo de calidad] |
| Frecuencia | [N eventos en el periodo] |
| Magnitud | [X horas perdidas / Y ton no producidas / Z% OEE] |
| Impacto economico estimado | [$ o ton — si hay fuente, si no: "no disponible"] |
| Turno(s) afectados | [Manana / Tarde / Noche / todos] |
| Fuente de datos | [SGL tabla perdidas / arauco_mc.db / archivo datos/YYYY-MM-DD_...] |

---

## KPI base y meta

| KPI | Formula | Valor actual | Meta | Frecuencia | Responsable |
|---|---|---|---|---|---|
| [Ej: OEE Linea 3] | Disp x Rend x Cal | [valor real con fuente] | [meta] | Semanal | [cargo] |

---

## Tipo de solucion

- [ ] Lean / Kaizen
- [ ] BPMN / Rediseno de proceso
- [ ] Diseno de KPI / Gobierno de datos
- [ ] Proyecto PMBoK
- [ ] GEMBA exploratorio

---

## Hipotesis inicial de causa raiz

[1-2 oraciones maximo. Si no hay evidencia: "causa raiz pendiente — requiere GEMBA".]

---

## Datos faltantes / bloqueadores

- [ ] [dato 1 necesario]
- [ ] [dato 2 necesario]

---

## Aprobacion

Solicitante confirma spec: [ ] SI  [ ] NO — Observacion: ___
```

## Restricciones de este skill

- No avanzar a `plan` sin spec en estado APROBADO
- No inventar la magnitud de la perdida: si no hay datos, el spec queda en BLOQUEADO
- El KPI base debe tener fuente real (SGL, `arauco_mc.db`, exportacion SAP PM); no estimaciones sin origen
- Si hay conflicto entre dato SGL y observacion de terreno, documentarlo en "Datos faltantes" y proponer GEMBA
- Impacto economico: solo incluir si hay tasa de conversion real (ton/hora, precio ton); no usar benchmarks inventados
- El enunciado del problema no puede incluir la solucion — describe la brecha, no la intervencion
