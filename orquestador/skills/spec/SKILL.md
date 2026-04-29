# Skill: spec — Encuadre estrategico del problema antes de delegar

> **Agente:** Orquestador — Subgerente de Mejora Continua

## Proposito

Convertir una solicitud ambigua en un brief estrategico claro: problema de negocio cuantificado, hipotesis explícita, areas involucradas, datos disponibles y entregable con audiencia definida. Sin spec aprobado no hay delegacion.

## Cuando usar

- Al recibir cualquier encargo del usuario antes de activar sub-agentes
- Cuando la solicitud mezcla sintomas ("el OEE bajo") con soluciones ("necesito un dashboard")
- Cuando no esta claro que areas o agentes involucrar
- Cuando hay inconsistencia entre lo que dice el usuario y los datos disponibles en `datos/`

**Prerequisito:** Acceso al directorio `datos/` para verificar que archivos existen. Si el usuario menciona cifras o KPIs, confirmar fuente antes de estructurar el brief. Si no hay datos disponibles y son necesarios, el spec queda en estado BLOQUEADO.

## Protocolo

### Paso 1 — Identificar el problema de negocio real

No aceptar la formulacion superficial. Pregunta de diagnóstico:

| Pregunta | Por que importa |
|---|---|
| ¿Cual es la brecha entre el estado actual y el esperado? | Separa sintoma de causa |
| ¿Quien sufre el impacto? ¿Operaciones, logistica, planta, gerencia? | Define audiencia y urgencia |
| ¿En que periodo ocurrio? ¿Es puntual o recurrente? | Determina si hay patron o evento |
| ¿Hay cifras disponibles? ¿De que sistema provienen? | Valida o descarta la hipotesis inicial |
| ¿Existe una decision pendiente que este analisis debe informar? | Define formato y plazo del entregable |

Si alguna de estas preguntas no tiene respuesta, documentar como "dato faltante" y hacer **una sola pregunta al usuario** antes de continuar.

### Paso 2 — Verificar datos disponibles en `datos/`

Usar `list_dir` sobre `datos/` y subdirectorios. Clasificar:

- **Disponibles y usables:** archivo existe, fecha reciente, formato legible
- **Disponibles pero con riesgo:** archivo muy antiguo (> 90 dias), formato cerrado (.pdf escaneado), cobertura parcial
- **Faltantes:** no existe archivo para el periodo o area indicada

Nunca asumir que un archivo existe por su nombre probable. Verificar antes de declararlo disponible.

### Paso 3 — Formular la hipotesis estrategica

Una hipotesis valida tiene la forma:

> "Creemos que [causa] esta generando [efecto cuantificado] en [area/proceso/equipo], durante [periodo]. Si esto se confirma, la oportunidad de mejora es [estimacion de impacto en EBITDA / OEE / costo logistico / m³]."

La hipotesis debe ser falseable: si no puede ser refutada con datos, reformular.

### Paso 4 — Identificar areas involucradas (MECE)

Clasificar sin solapamiento ni omisiones:

| Area | Involucrada | Rol | Agente |
|---|---|---|---|
| Excelencia Operacional | SI / NO | Diagnostico de proceso / KPIs / Lean | EO |
| Transformacion Digital | SI / NO | Datos, automatizacion, telemetria, integraciones | TD |
| Inteligencia Artificial | SI / NO | Analisis historico, modelos, dashboards | IA |
| Analisis de Datos | SI / NO | Archivo fuente con datos estructurados | DA (reactivo) |

Si solo una area es necesaria, delegar directo. Si hay dependencias entre areas, definir el orden de ejecucion en el `plan`.

### Paso 5 — Definir entregable y audiencia

| Campo | Opciones |
|---|---|
| Audiencia | Gerencia / Subgerencia / Jefatura / Terreno |
| Formato | Informe ejecutivo / Ficha tecnica / Dashboard HTML / Presentacion / Plan de accion |
| Nivel de detalle | Ejecutivo (1 pagina) / Gerencial (3-5 paginas) / Tecnico (sin limite) |
| Plazo | Inmediato / Iteracion siguiente / [fecha especifica] |

### Paso 6 — Validar con el usuario (si hay ambiguedad)

Si el spec tiene campos en PENDIENTE o la hipotesis no es verificable sin confirmacion del usuario: presentar el draft del brief y esperar confirmacion antes de avanzar a `plan`.

Si el spec esta completo y los datos existen: avanzar directamente a `plan` sin preguntar.

### Paso 7 — Guardar brief estrategico

```
datos/YYYY-MM-DD_spec-orq-[area]-[tipo].md
```

## Plantilla de Brief Estrategico

```markdown
# Brief Estrategico — [Titulo del problema]

**Fecha:** YYYY-MM-DD
**Solicitante:** [cargo o area]
**Estado:** BORRADOR | APROBADO | BLOQUEADO | PENDIENTE

---

## Problema de negocio

| Campo | Valor |
|---|---|
| Area / Proceso / Equipo | [Ej: Cosecha — Sector Norte / Linea 3 Celulosa] |
| Periodo de analisis | [Ej: 2026-01-01 a 2026-03-31] |
| Brecha identificada | [Ej: OEE Linea 3 en 71,2% vs meta 82,0% — delta -10,8 pp] |
| Impacto estimado | [ton/mes, $/mes, h/mes — con fuente; si no hay: "pendiente de cuantificar"] |
| Recurrencia | Puntual / Recurrente [desde YYYY-MM] |
| Fuente de datos disponible | [arauco_mc.db / datos/YYYY-MM-DD_archivo.ext / SGL / SAP PM / "no disponible"] |
| Decision que informa | [Ej: priorizar inversion en equipo, redisenar proceso, escalar a Gerencia] |

---

## Hipotesis estrategica

> "[Hipotesis falseable con causa, efecto y magnitud estimada]"

**Confianza inicial:** Alta / Media / Baja — [justificacion en 1 linea]

---

## Areas involucradas

| Agente | Involucrado | Rol especifico | Dependencias |
|---|---|---|---|
| EO | SI / NO | [Ej: diagnostico de proceso y plan Lean] | [ej: requiere output IA primero] |
| TD | SI / NO | [Ej: telemetria disponible, estado de integracion] | |
| IA | SI / NO | [Ej: analisis historico ON/OFF, patrones de falla] | |
| DA | SI / NO | [Ej: lectura de planilla Excel adjunta] | |

---

## Entregable esperado

| Campo | Valor |
|---|---|
| Formato | [Informe ejecutivo .docx / Dashboard HTML / Presentacion .pptx / Plan de accion .md] |
| Audiencia | [Gerencia / Subgerencia / Jefatura de area] |
| Nivel de detalle | [Ejecutivo / Gerencial / Tecnico] |
| Nombre del archivo | datos/YYYY-MM-DD_[tipo]-[descripcion].ext |
| Plazo | Inmediato / [fecha] |

---

## Datos disponibles

| Archivo | Ruta | Periodo | Estado | Riesgo |
|---|---|---|---|---|
| [nombre] | datos/YYYY-MM-DD_... | [fechas] | Disponible / Riesgo / Faltante | [antiguedad, cobertura parcial, etc.] |

---

## Datos faltantes / bloqueadores

- [ ] [dato necesario para confirmar o refutar la hipotesis]
- [ ] [sistema o exportacion que debe proveer el usuario]

---

## Aprobacion del brief

Solicitante confirma hipotesis y entregable: [ ] SI  [ ] NO — Observacion: ___
```

## Restricciones

- No delegar (no avanzar a `plan`) sin brief en estado APROBADO
- La hipotesis no puede incluir la solucion: describe la brecha y la causa probable, no la intervencion
- Impacto economico: solo incluir si hay fuente real (ton/h, precio ton, costo logistico unitario); no usar benchmarks de industria sin citar origen
- Si el usuario entrega datos contradictorios entre si o contradictorios con `arauco_mc.db`: documentar la discrepancia en "Datos faltantes" y pedir clarificacion antes de avanzar
- El brief es para guiar la delegacion, no para publicar al usuario: lenguaje ejecutivo pero sin formato de informe final
- No inventar cifras de contexto ("la industria forestal pierde en promedio...") sin citar fuente real
