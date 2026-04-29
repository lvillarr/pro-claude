# Skill: test — Piloto en terreno y validacion de KPIs

> **Agente:** EO — Excelencia Operacional

## Proposito

Verificar que los entregables del build funcionan en condiciones reales de operacion antes de estandarizar. Validar que los KPIs mejoran respecto a la linea base del spec. Producir un veredicto formal: APROBADO o REPROBADO.

## Cuando usar este skill

- BPMN TO-BE, KPIs y plan de accion completados (build finalizado)
- Se requiere confirmar que la solucion reduce la perdida operacional identificada en el spec
- Antes de actualizar procedimientos, checklists o registros SGL con el nuevo estandar
- Cuando hay duda sobre adopcion del nuevo proceso por parte de los operadores

**Prerequisito:** Entregables del build en `datos/` con fecha. Al menos 1 turno piloto ejecutado con la nueva forma de operar. Acceso a datos del periodo piloto (SGL o `arauco_mc.db`).

## Protocolo de ejecucion

### Paso 1 — Definir periodo y alcance del piloto

Antes de medir, acordar con el jefe de turno:
- Duracion minima del piloto: 5 turnos consecutivos (o el equivalente definido en el plan)
- Equipos / lineas involucrados
- Operadores que participan
- Condiciones de operacion representativas (no elegir turnos con parada programada)

Documentar en la cabecera del informe de test.

### Paso 2 — Obtener datos del periodo piloto

```sql
-- Datos piloto: perdidas del equipo durante el periodo
SELECT fecha, turno, equipo, tipo_perdida, minutos_perdidos, operador_id
FROM perdidas
WHERE equipo = '[id_equipo]'
  AND fecha BETWEEN '[fecha_inicio_piloto]' AND '[fecha_fin_piloto]'
ORDER BY fecha, turno;

-- Comparar con linea base (periodo equivalente antes del piloto)
SELECT fecha, turno, equipo, tipo_perdida, minutos_perdidos
FROM perdidas
WHERE equipo = '[id_equipo]'
  AND fecha BETWEEN '[fecha_inicio_base]' AND '[fecha_fin_base]'
ORDER BY fecha, turno;
```

Si el dato no esta en `arauco_mc.db`, usar `excel-mcp` o `markitdown` sobre el archivo exportado del SGL.

### Paso 3 — Calcular delta KPI vs. linea base

Para cada KPI del diccionario (build):

| KPI | Linea base | Periodo piloto | Delta absoluto | Delta % | Meta spec | Resultado |
|---|---|---|---|---|---|---|
| OEE Linea 3 | 78,4% | 83,1% | +4,7 pp | +6,0% | >= 85,0% | PARCIAL |
| Paradas no planif. | 12 eventos/sem | 7 eventos/sem | -5 | -41,7% | <= 6 | APROBADO |

Calcular con Python si el volumen de datos lo justifica:

```python
import pandas as pd

base = pd.read_csv('datos/linea_base.csv')
piloto = pd.read_csv('datos/piloto.csv')

kpis = ['oee', 'paradas', 'minutos_perdidos']
for k in kpis:
    delta = piloto[k].mean() - base[k].mean()
    pct = delta / base[k].mean() * 100
    print(f"{k}: base={base[k].mean():.2f} | piloto={piloto[k].mean():.2f} | delta={delta:+.2f} ({pct:+.1f}%)")
```

### Paso 4 — Checklist de validacion con operadores

Aplicar el checklist durante GEMBA en el turno piloto. Firmar fisicamente o digitalizar.

### Paso 5 — Emitir veredicto

Criterios:
- **APROBADO:** todos los KPIs criticos alcanzan o superan la meta del spec
- **APROBADO CONDICIONAL:** KPIs criticos cumplen meta pero hay observaciones menores a resolver antes de estandarizar
- **REPROBADO:** al menos un KPI critico no alcanza la meta; o el checklist tiene fallas de seguridad o proceso

Si REPROBADO: documentar causas, actualizar el A3 (seccion 7) y volver a `build` con ajuste de contramedidas.

### Paso 6 — Guardar informe de test

```
datos/YYYY-MM-DD_test-[area]-[equipo].md
```

## Plantilla de Informe de Test

```markdown
# Informe de Test — [Area / Equipo / Proceso]

**Fecha:** YYYY-MM-DD
**Referencia build:** datos/YYYY-MM-DD_[tipo]-[area]-*.* 
**Responsable:** [Cargo]
**Veredicto:** APROBADO | APROBADO CONDICIONAL | REPROBADO

---

## Contexto del piloto

| Campo | Valor |
|---|---|
| Linea / Equipo | |
| Periodo piloto | YYYY-MM-DD a YYYY-MM-DD |
| Turnos incluidos | [N turnos — Manana / Tarde / Noche] |
| Operadores participantes | [N operadores — cargos, no nombres] |
| Condiciones de operacion | [normales / con restriccion: especificar] |
| Fuente de datos piloto | [SGL / arauco_mc.db / archivo datos/YYYY-MM-DD_...] |

---

## Resultados KPI vs. linea base

| KPI | Formula | Linea base | Piloto | Delta | Meta | Resultado |
|---|---|---|---|---|---|---|
| | | | | | | APROBADO / PARCIAL / REPROBADO |

**Periodo linea base:** YYYY-MM-DD a YYYY-MM-DD (equivalente al piloto en longitud)

---

## Checklist de validacion operacional

| # | Criterio | SI / NO | Observacion |
|---|---|---|---|
| 1 | El operador conoce el nuevo procedimiento sin asistencia | | |
| 2 | El registro en SGL se realiza segun el nuevo flujo | | |
| 3 | No se observan retrabajos o pasos duplicados en el TO-BE | | |
| 4 | Los KPIs se pueden medir con los instrumentos disponibles | | |
| 5 | No hay riesgo de seguridad introducido por el cambio | | |
| 6 | El jefe de turno valida el nuevo estandar | | |
| 7 | Los tiempos de ciclo son iguales o menores al AS-IS | | |
| 8 | Los datos generados tienen calidad suficiente (sin blancos criticos) | | |

---

## Observaciones de terreno (GEMBA durante piloto)

[Descripcion de lo observado directamente. Desviaciones del BPMN TO-BE, comportamientos no previstos, problemas de herramental o sistema.]

---

## Veredicto y fundamento

**Veredicto:** APROBADO | APROBADO CONDICIONAL | REPROBADO

**Fundamento:**
- [Punto 1: KPI critico + valor alcanzado vs. meta]
- [Punto 2: observacion operacional relevante]
- [Punto 3: condicion para condicional, o causa de reprobacion]

---

## Acciones correctivas (si REPROBADO o CONDICIONAL)

| ID | Accion | Responsable | Plazo |
|---|---|---|---|

---

## Firma de validacion

| Rol | Cargo | Fecha | Firma |
|---|---|---|---|
| Responsable EO | Jefe EO | | |
| Validador terreno | Jefe de Turno | | |
```

## Restricciones de este skill

- Minimo 5 turnos de piloto antes de emitir veredicto; excepciones requieren justificacion explicita en el informe
- La linea base debe ser del mismo equipo, en un periodo equivalente, con condiciones comparables (no usar linea base de otro equipo como proxy)
- Checklist debe ser completado en terreno, no retrospectivamente desde datos
- No emitir APROBADO si hay algun criterio de seguridad (item 5) marcado como NO
- Si el delta KPI es positivo pero no alcanza la meta del spec, el veredicto es APROBADO CONDICIONAL como maximo — no APROBADO
- No avanzar a `review` ni `ship` con veredicto REPROBADO; volver a `build`
- Fuente de datos del piloto: siempre citar archivo o tabla exacta; no usar "datos propios" sin origen
