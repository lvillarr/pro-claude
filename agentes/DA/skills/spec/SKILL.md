# Skill: spec — Definicion de la pregunta de negocio antes de analizar

> **Agente:** DA — Analisis de Datos

## Proposito

Estructurar y validar la pregunta de negocio antes de tocar cualquier archivo. Sin spec definido no hay plan ni build. Previene construir dashboards que no responden lo que el area necesita y KPIs calculados sobre columnas equivocadas.

## Cuando usar

- Al recibir un encargo de analisis: "analiza este Excel de cosecha", "dame los KPIs de mantenimiento de este mes"
- Cuando el orquestador entrega un archivo sin pregunta concreta
- Cuando el archivo tiene multiples hojas o secciones y no esta claro que parte analizar
- Cuando la solicitud mezcla distintas preguntas (produccion + mantenimiento + costos) que requieren priorizar

**Prerequisito:** El archivo fuente debe existir en `datos/` o haber sido recibido via Telegram (JSON, PDF, DOCX). Sin archivo no hay spec. Estado: BLOQUEADO hasta que el solicitante provea el archivo.

## Protocolo

### Paso 1 — Inspeccion inicial del archivo fuente

Antes de formular la pregunta, conocer la estructura del archivo. Usar `excel-mcp` para hojas `.xlsx`, `markitdown` para PDF/DOCX, o `bash` con pandas para CSV.

```python
import pandas as pd

# Inspeccion rapida: shape, columnas, tipos, nulos
df = pd.read_excel('datos/archivo.xlsx', sheet_name=0, nrows=5)
print("Shape:", pd.read_excel('datos/archivo.xlsx', sheet_name=0).shape)
print("Columnas:", df.columns.tolist())
print("Tipos:\n", df.dtypes)
print("Nulos:\n", pd.read_excel('datos/archivo.xlsx', sheet_name=0).isnull().sum())
print("Muestra:\n", df.to_string())
```

Output esperado del Paso 1:
```
Shape: 1.247 filas x 14 columnas
Columnas: ['FECHA', 'LINEA', 'TURNO', 'EQUIPO', 'TIPO_PERDIDA', 'MINUTOS', ...]
Tipos: FECHA=object, LINEA=object, MINUTOS=float64, ...
Nulos: TURNO=23, TIPO_PERDIDA=0, MINUTOS=4
Muestra: [5 filas representativas]
```

Para Excel con multiples hojas:
```python
xf = pd.ExcelFile('datos/archivo.xlsx')
print("Hojas:", xf.sheet_names)
for hoja in xf.sheet_names:
    df_h = pd.read_excel('datos/archivo.xlsx', sheet_name=hoja, nrows=3)
    print(f"\n--- {hoja} ---")
    print("Cols:", df_h.columns.tolist())
    print("Shape:", pd.read_excel('datos/archivo.xlsx', sheet_name=hoja).shape)
```

### Paso 2 — Identificar columnas clave segun contexto forestal

Mapear columnas del archivo a conceptos del negocio:

| Concepto | Columnas tipicas en archivos Arauco |
|---|---|
| Tiempo | FECHA, TURNO, MES, SEMANA, PERIODO |
| Produccion | TONELADAS, M3, HA_COSECHADAS, RENDIMIENTO |
| Equipos | EQUIPO, MAQUINA, CODIGO_SAP, LINEA |
| Perdidas | TIPO_PERDIDA, MINUTOS_PERDIDOS, HORAS_PARADA |
| Eficiencia | OEE, DISPONIBILIDAD, RENDIMIENTO_OEE, CALIDAD |
| Contratistas | CONTRATISTA, RUT_EMPRESA, FAENA |
| Costos | COSTO_HORA, COSTO_TONELADA, PRESUPUESTO |

Si una columna tiene nombre ambiguo (ej: "COL_A", "CAMPO1"), reportar como dato_pendiente y solicitar al solicitante que aclare su significado antes de continuar.

### Paso 3 — Formular la pregunta de negocio

La pregunta de negocio sigue esta estructura:

> "Usando [archivo/hoja], calcular [metrica principal] por [dimension de agrupacion], para el periodo [rango de fechas], con el objetivo de [decision operacional que se tomara con el resultado]."

Ejemplos validos:
- "Usando SGL_Perdidas_Junio.xlsx / hoja Detalle, calcular minutos perdidos por equipo y tipo de perdida, para 2026-06, para identificar los equipos con mayor impacto en el OEE de la Linea 3."
- "Usando Informe_Cosecha_Q1.pdf (paginas 3-12), extraer hectareas cosechadas por faena y contratista, para Q1-2026, para verificar cumplimiento del plan mensual."

Preguntas invalidas (no proceder):
- "Analiza el archivo" — sin dimension ni metrica definida
- "Dame todo lo que puedas" — alcance indefinido
- "Compara con el mes pasado" — sin definir que archivo es el mes pasado

### Paso 4 — Completar la plantilla de spec

Ver plantilla al final de este documento. El spec queda en estado BORRADOR hasta que el solicitante confirme. En Telegram, mostrar el spec y pedir confirmacion antes de avanzar. En Claude Code, reportar al orquestador con el bloque spec y solicitar aprobacion.

### Paso 5 — Identificar formato de output requerido

| Audiencia | Output preferido |
|---|---|
| Subgerente MC / Gerencia | Reporte HTML con KPI cards y graficos — ejecutivo |
| Jefe de Area / Planta | Reporte HTML con tabla filtrable y detalle por equipo/turno |
| Analista EO | Tabla markdown + script Python reutilizable |
| Orquestador (Claude Code) | HTML en datos/ + bloque ENTREGA DA: |
| Telegram (respuesta rapida) | Tabla markdown + resumen en 3-5 puntos |

### Paso 6 — Registrar spec en datos/

Solo en contexto Claude Code (no Telegram):
```
datos/YYYY-MM-DD_spec-[area]-[tipo].md
```

## Plantilla de Spec

```markdown
# Spec DA — [Area / Archivo / Tipo de analisis]

**Fecha:** YYYY-MM-DD
**Solicitante:** [nombre o agente que invoca — orquestador / EO / usuario Telegram]
**Estado:** BORRADOR | APROBADO | BLOQUEADO | PENDIENTE

---

## Archivo fuente

| Campo | Valor |
|---|---|
| Archivo | [datos/YYYY-MM-DD_nombre.ext o "recibido via Telegram"] |
| Hoja / Seccion | [nombre de hoja o paginas PDF] |
| Total registros | [N filas x M columnas — o "N paginas, N caracteres"] |
| Periodo cubierto | [rango de fechas detectado en los datos] |
| Fuente original | [SGL / SAP PM / Historian / Planex / Forest Data 2.0 / "no identificado"] |

---

## Pregunta de negocio

[Formulacion completa: "Usando [archivo/hoja], calcular [metrica] por [dimension], para el periodo [rango], con el objetivo de [decision]."]

---

## Metricas a calcular

| Metrica | Formula o logica | Columnas involucradas | Unidad |
|---|---|---|---|
| [Ej: Minutos perdidos por equipo] | SUM(MINUTOS) GROUP BY EQUIPO | MINUTOS, EQUIPO | min |
| [Ej: OEE promedio por linea] | AVG(OEE) GROUP BY LINEA | OEE, LINEA | % |

---

## Dimensiones de analisis

- [ ] Tiempo: [turno / dia / semana / mes]
- [ ] Equipo / Linea: [columna]
- [ ] Tipo de perdida / proceso: [columna]
- [ ] Contratista / Faena: [columna — si aplica]
- [ ] Otro: [especificar]

---

## Audiencia y formato de output

| Campo | Valor |
|---|---|
| Audiencia | [Subgerente MC / Jefe de Area / Analista EO / Orquestador] |
| Formato | [HTML interactivo / tabla markdown / texto resumen / script Python] |
| Nivel de detalle | [ejecutivo (KPIs + graficos) / operacional (tabla filtrable) / tecnico (script)] |

---

## Columnas sin uso en este analisis

[Lista de columnas presentes en el archivo que NO se usaran y por que — evita confusion posterior]

---

## Datos faltantes / bloqueadores

- [ ] [dato o columna que falta para responder la pregunta]
- [ ] [aclaracion pendiente del solicitante]

---

## Aprobacion

Solicitante confirma spec: [ ] SI  [ ] NO — Observacion: ___
```

## Restricciones

- No avanzar a `plan` sin spec en estado APROBADO
- Si el archivo tiene columnas ambiguas sin aclaracion del negocio, marcar spec como PENDIENTE
- La pregunta de negocio debe incluir: archivo, metrica, dimension de agrupacion y decision a tomar
- No inventar el significado de columnas con nombres tecnicos o codigos SAP sin confirmar con el solicitante
- Formato numerico chileno en el spec: `1.247 filas`, `87,3%`, `1.234,5 min`
- Si el archivo supera 100.000 filas, documentarlo en el spec y advertir que el build usara muestreo o agregacion; nunca silenciar este hecho
- El spec debe listar explicitamente las columnas que NO se usaran — previene calculos accidentales sobre campos irrelevantes
