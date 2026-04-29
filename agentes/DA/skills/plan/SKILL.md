# Skill: plan — Plan de analisis paso a paso

> **Agente:** DA — Analisis de Datos

## Proposito

Definir el recorrido exacto del analisis antes de ejecutarlo: que datos limpiar, que calculos hacer, que graficos construir y en que orden. Previene analisis incompletos o graficos que no responden la pregunta del spec.

## Cuando usar

- Spec en estado APROBADO
- El archivo fuente tiene mas de 3 columnas o mas de 500 filas (complejidad suficiente para necesitar plan)
- Se requiere un dashboard HTML (siempre planificar graficos antes de escribir Chart.js)
- El analisis tiene multiples dimensiones (tiempo + equipo + tipo de perdida) que pueden combinarse de varias formas

**Prerequisito:** `datos/YYYY-MM-DD_spec-[area]-[tipo].md` en estado APROBADO (o spec confirmado por el solicitante en Telegram). Sin spec aprobado, el plan queda en estado PENDIENTE.

## Protocolo

### Paso 1 — Inspeccion de calidad de datos

Diagnosticar problemas antes de planificar limpiezas. Ejecutar sobre el archivo completo, no solo sobre la muestra del spec.

```python
import pandas as pd
import numpy as np

df = pd.read_excel('datos/archivo.xlsx', sheet_name='NombreHoja')

# Reporte de calidad
reporte = {
    'shape': df.shape,
    'nulos_por_col': df.isnull().sum().to_dict(),
    'pct_nulo': (df.isnull().sum() / len(df) * 100).round(1).to_dict(),
    'duplicados': df.duplicated().sum(),
    'tipos': df.dtypes.astype(str).to_dict()
}

# Detectar strings en columnas que deberian ser numericas
for col in df.columns:
    if df[col].dtype == object:
        numerico = pd.to_numeric(df[col], errors='coerce')
        if numerico.notna().sum() > len(df) * 0.5:
            print(f"ALERTA: {col} parece numerica pero es string — {numerico.isna().sum()} no convertibles")

# Detectar fechas como strings
for col in df.columns:
    if 'fecha' in col.lower() or 'date' in col.lower():
        if df[col].dtype == object:
            print(f"ALERTA: {col} es fecha pero tipo string — requiere pd.to_datetime()")
```

Registrar en el plan: columnas con > 10% nulos, duplicados detectados, columnas de tipo incorrecto.

### Paso 2 — Definir limpiezas necesarias

Listar cada transformacion que se aplicara, en orden. Ser especifico: no "limpiar nulos" sino "reemplazar NaN en columna TURNO con 'Sin turno' para no perder registros en el GROUP BY".

Tabla de limpiezas del plan:

| # | Columna | Problema detectado | Accion | Justificacion |
|---|---|---|---|---|
| 1 | TURNO | 23 nulos (1,8%) | Reemplazar con 'Sin turno' | Evitar perdida de filas en agrupacion |
| 2 | MINUTOS | 4 nulos (0,3%) | Eliminar filas — valor requerido para KPI | Imputable si se elimina < 1% |
| 3 | FECHA | tipo string | pd.to_datetime(format='%d/%m/%Y') | Necesario para filtros temporales |
| 4 | COSTO | strings con '$' y '.' | str.replace + pd.to_numeric | Dato numerico mal formateado |

Documentar qué NO se limpia y por que (ej: columna ADDRESS no se usa en este analisis).

### Paso 3 — Definir calculos del analisis

Listar cada calculo con su logica exacta. No ML ni modelos predictivos.

```
ANALISIS 1: Minutos perdidos por equipo
  logica: df.groupby('EQUIPO')['MINUTOS'].sum().sort_values(ascending=False)
  resultado esperado: Serie con equipos ordenados por impacto
  KPI derivado: top_equipo, total_minutos

ANALISIS 2: Distribucion por tipo de perdida
  logica: df.groupby('TIPO_PERDIDA')['MINUTOS'].sum() / df['MINUTOS'].sum() * 100
  resultado esperado: % de cada tipo sobre el total
  KPI derivado: tipo_dominante, pct_mecanica

ANALISIS 3: Evolucion semanal de paradas
  logica: df.resample('W', on='FECHA')['MINUTOS'].sum()
  resultado esperado: Serie temporal semanal
  KPI derivado: tendencia (creciente/decreciente/estable)

ANALISIS 4: Cruce equipo x turno
  logica: df.pivot_table(values='MINUTOS', index='EQUIPO', columns='TURNO', aggfunc='sum')
  resultado esperado: Matriz de calor equipos vs turnos
  KPI derivado: turno_critico, equipo_turno_peor
```

Regla: cada KPI card del dashboard debe tener su calculo listado aqui antes de construirlo.

### Paso 4 — Definir graficos a incluir

Minimo 2 graficos. Seleccionar tipo segun pregunta:

| Pregunta | Tipo de grafico recomendado | Chart.js config |
|---|---|---|
| Ranking de equipos / causas | Bar horizontal | `type: 'bar'` con `indexAxis: 'y'` |
| Evolucion en el tiempo | Line | `type: 'line'` con `tension: 0.3` |
| Distribucion porcentual | Doughnut | `type: 'doughnut'` |
| Cruce dos dimensiones | Bar agrupado | `type: 'bar'` con multiples datasets |
| Distribucion de una variable | Histogram | `type: 'bar'` con bins manuales |
| Comparacion antes/despues | Bar lado a lado | dos datasets con colores Arauco |

Para cada grafico definir:
- Titulo
- Eje X / Eje Y (o etiquetas para pie/doughnut)
- Variable fuente (columna y calculo)
- Filtro: si el grafico debe actualizarse con los `<select>` del dashboard

### Paso 5 — Definir KPI cards del dashboard

Exactamente 4 KPI cards en `.grid.grid-4`. Para cada una:

| Card | Valor | Fuente | Contexto (label inferior) |
|---|---|---|---|
| Total registros | len(df) | df.shape[0] | "N registros analizados" |
| [KPI principal] | sum/avg de columna clave | calculo definido en Paso 3 | periodo o dimension |
| [KPI comparacion] | top valor o categoria | calculo definido en Paso 3 | "equipo/linea/turno mas afectado" |
| [KPI estado] | % nulos o % cobertura | calculo de calidad | caveat de completitud |

### Paso 6 — Definir filtros dinamicos del dashboard

Listar cada `<select>` y la columna que controla. Cada filtro debe actualizar tabla Y todos los graficos.

```
FILTRO 1: Linea — columna LINEA — valores unicos del dataframe
FILTRO 2: Turno — columna TURNO — ['Manana', 'Tarde', 'Noche', 'Sin turno', 'Todos']
FILTRO 3: Tipo de perdida — columna TIPO_PERDIDA — valores unicos del dataframe
```

Documentar interaccion entre filtros: los filtros se aplican en AND (todos activos simultaneamente).

### Paso 7 — Definir tipo de output

| Output | Aplica si |
|---|---|
| HTML interactivo | audiencia ejecutiva u operacional; siempre en contexto Claude Code |
| Tabla markdown | respuesta rapida en Telegram; analisis de menos de 3 columnas |
| Script Python | solicitante necesita replicar localmente o automatizar |
| Texto resumen | complemento de cualquier output; maximo 5 puntos cuantificados |

### Paso 8 — Guardar plan en datos/

Solo en contexto Claude Code:
```
datos/YYYY-MM-DD_plan-[area]-[descripcion].md
```

## Plantilla de Plan

```markdown
# Plan de Analisis DA — [Area / Archivo]

**Fecha:** YYYY-MM-DD
**Referencia spec:** datos/YYYY-MM-DD_spec-[area]-[tipo].md
**Estado:** BORRADOR | APROBADO

---

## Archivo fuente

- Archivo: datos/[nombre.ext]
- Hoja/seccion: [nombre]
- Shape: N filas x M columnas
- Periodo: YYYY-MM-DD a YYYY-MM-DD

---

## Limpiezas necesarias

| # | Columna | Problema | Accion | Impacto en registros |
|---|---|---|---|---|

---

## Calculos

| # | Nombre del calculo | Logica | Columnas | KPI derivado |
|---|---|---|---|---|

---

## KPI cards (4)

| Card | Valor | Fuente |
|---|---|---|

---

## Graficos (minimo 2)

| # | Titulo | Tipo | Eje X / Y | Variable | Filtrable |
|---|---|---|---|---|---|

---

## Filtros dinamicos

| Filtro | Columna | Valores |
|---|---|---|

---

## Output

- [ ] HTML interactivo — datos/YYYY-MM-DD_reporte-[descripcion].html
- [ ] Tabla markdown
- [ ] Script Python — datos/YYYY-MM-DD_script-[descripcion].py
- [ ] Texto resumen
```

## Restricciones

- No modelar ML ni regresiones — el plan se limita a estadistica descriptiva: suma, promedio, frecuencias, tablas cruzadas, percentiles
- Cada grafico del plan debe tener su variable fuente identificada antes de pasar a build
- Si una columna tiene > 30% nulos, documentarlo en el plan Y en los caveats del spec — no silenciar
- Los filtros dinamicos se planifican aqui; en build no se agrega ningun filtro que no este en el plan
- El plan no modifica el spec: si durante la inspeccion se descubren columnas que cambian la pregunta de negocio, actualizar el spec primero
- Formato numerico chileno en el plan: `1.247 filas`, `87,3%`, `1.234,5 min`
