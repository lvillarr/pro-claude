# Skill: review — Sintesis y control de calidad de entregas

> **Agente:** Orquestador — Subgerente de Mejora Continua

## Proposito

Validar cada ENTREGA recibida de los sub-agentes antes de sintetizar, detectar inconsistencias entre areas y traducir hallazgos tecnicos a lenguaje de negocio. Ningun resultado llega al usuario sin pasar por este skill.

## Cuando usar

- Al recibir una o mas ENTREGAs de sub-agentes (EO, TD, IA, DA)
- Antes de ejecutar `ship`
- Cuando hay inconsistencia entre los outputs de dos agentes distintos
- Cuando el usuario pide una revision de un entregable ya generado

**Prerequisito:** Al menos una ENTREGA recibida de sub-agente con sus campos declarados. Si no hay ENTREGA, no hay review: solicitar al agente que emita su ENTREGA antes de continuar.

## Protocolo

### Paso 1 — Aplicar checklist Paso 3.5 por cada ENTREGA

Para cada ENTREGA recibida, verificar campo a campo:

**EO:**
- [ ] Hallazgos clave presentes y cuantificados (con fuente SGL / arauco_mc.db / GEMBA)
- [ ] Causa raiz documentada con evidencia (no solo hipotesis)
- [ ] Limitaciones declaradas (datos faltantes, periodo parcial, supuestos)
- [ ] Plan de accion con responsable de cargo, plazo y criterio de cierre verificable

**TD:**
- [ ] Estado actual confirmado (funcional / con restricciones / bloqueado) — no "en desarrollo" sin mas
- [ ] Dependencias TI identificadas (accesos, credenciales, infraestructura)
- [ ] Limitaciones tecnicas declaradas (conectividad, ciclo de rotacion de tokens, sistemas sin API)
- [ ] Impacto esperado en lenguaje operacional (no solo tecnico)

**IA:**
- [ ] Hallazgos clave cuantificados con fuente de datos declarada
- [ ] Limitaciones del analisis declaradas (cobertura temporal, registros con nulos, supuestos del modelo)
- [ ] Impacto estimado en lenguaje de negocio (OEE, m³, h perdidas, costo logistico)

**DA:**
- [ ] Fuente del archivo explicitada (ruta, nombre, fecha del archivo)
- [ ] Total de registros procesados declarado
- [ ] Caveats de muestra documentados (nulos, inconsistencias, campos sin datos)

**Si algún campo falta:** no inferir ni completar por cuenta propia. Solicitar al agente que complete antes de continuar la sintesis.

### Paso 2 — Detectar inconsistencias entre agentes

Comparar los outputs recibidos buscando:

| Tipo de inconsistencia | Ejemplo | Accion |
|---|---|---|
| Cifras contradictorias | EO reporta OEE 71,2% / IA reporta OEE 74,8% para el mismo periodo | Identificar fuente de cada uno; pedir aclaracion al agente con la cifra discrepante |
| Supuestos incompatibles | EO asume datos completos de SGL / DA reporta 23% de registros nulos en SGL | Revisar si el analisis EO es valido con esa cobertura |
| Periodo distinto | IA analizo 2025-Q4 / EO analizo 2026-Q1 | Alinear o documentar que los resultados no son comparables directamente |
| Causa raiz en conflicto | EO atribuye perdidas a habito operacional / IA muestra patron de falla en turno noche sin correlacion con operadores | Documentar ambas hipotesis y pedir GEMBA si es necesario |

Si la inconsistencia es bloqueante (invalida la hipotesis del brief): escalar al usuario antes de sintetizar.

### Paso 3 — Traducir tecnico a lenguaje de negocio

Reglas de traduccion:

| No usar | Usar en cambio |
|---|---|
| "el modelo de regresion indica..." | "el analisis historico muestra que..." |
| "latencia del pipeline de 12 min" | "los datos estan disponibles 12 minutos despues de cada turno" |
| "OEE = disponibilidad x rendimiento x calidad" | "el equipo opero al [X]% de su capacidad teorica" |
| "p-value < 0,05" | "la relacion es estadisticamente robusta con los datos disponibles" |
| "BPMN TO-BE" | "el proceso rediseñado" |
| "ETL" | "extraccion automatica de datos" |
| "INSERT OR IGNORE" | (no mencionar en entregable ejecutivo) |

Las cifras se mantienen exactas; solo cambia la envoltura narrativa.

### Paso 4 — Estructurar la sintesis con Minto

La sintesis integrada sigue la piramide Minto:

```
SITUACION:
[Contexto que el receptor ya sabe — 1-2 lineas. Estado actual del area/proceso/equipo.]

COMPLICACION:
[Por que la situacion actual es insostenible o representa una oportunidad — cuantificado.
Esto es la brecha identificada en el brief.]

PREGUNTA (implicita o explicita):
[Que debemos hacer? / Cual es la causa? / Como capturar la oportunidad?]

RESPUESTA (la tesis central):
[La recomendacion principal — una oracion, accionable, con responsable implicito.]

ARGUMENTOS DE SOPORTE:
[Hallazgos de EO / IA / TD / DA que sustentan la respuesta — maximos 3, cuantificados.]
```

### Paso 5 — Verificar coherencia con el brief

Confirmar que la sintesis responde la hipotesis del brief:

- [ ] La hipotesis fue respondida: confirmada / refutada / ajustada (documentar cual)
- [ ] Las cifras presentadas tienen fuente real (no estimaciones de relleno)
- [ ] El entregable responde: problema → hallazgo → recomendacion → proximo paso
- [ ] Audiencia y formato del entregable coinciden con lo definido en el brief

Si la hipotesis no pudo ser respondida con los datos disponibles: declararlo explicitamente antes de recomendar. No presentar una conclusion donde hay incertidumbre real.

### Paso 6 — Producir el informe de revision interna

```
datos/YYYY-MM-DD_review-orq-[area]-[tipo].md
```

Este archivo es de trabajo interno del Orquestador. No se entrega al usuario directamente.

## Plantilla de Revision Interna

```markdown
# Revision Orquestador — [Titulo de la iniciativa]

**Fecha:** YYYY-MM-DD
**Brief de referencia:** datos/YYYY-MM-DD_spec-orq-[area]-[tipo].md
**Entregas recibidas:** [lista de archivos recibidos de cada agente]
**Estado de la revision:** APROBADA | APROBADA CON OBSERVACIONES | BLOQUEADA

---

## Validacion Paso 3.5 por agente

### EO

| Campo | Estado | Observacion |
|---|---|---|
| Hallazgos clave cuantificados | OK / FALTA / PARCIAL | [detalle si no es OK] |
| Causa raiz con evidencia | OK / FALTA | |
| Limitaciones declaradas | OK / FALTA | |
| Plan con responsable, plazo y criterio | OK / FALTA / PARCIAL | |

### TD

| Campo | Estado | Observacion |
|---|---|---|
| Estado actual confirmado | OK / FALTA | |
| Dependencias TI identificadas | OK / FALTA / PARCIAL | |
| Limitaciones tecnicas declaradas | OK / FALTA | |
| Impacto en lenguaje operacional | OK / FALTA | |

### IA

| Campo | Estado | Observacion |
|---|---|---|
| Hallazgos cuantificados con fuente | OK / FALTA / PARCIAL | |
| Limitaciones del analisis | OK / FALTA | |
| Impacto en lenguaje de negocio | OK / FALTA | |

### DA

| Campo | Estado | Observacion |
|---|---|---|
| Fuente del archivo | OK / FALTA | |
| Total de registros declarado | OK / FALTA | |
| Caveats de muestra | OK / FALTA | |

---

## Inconsistencias detectadas

| ID | Tipo | Descripcion | Entre agentes | Accion |
|---|---|---|---|---|
| I-001 | Cifra / Supuesto / Periodo / Causa | [descripcion] | [A] vs [B] | Solicitar clarificacion / Alinear / Documentar como limitacion |

---

## Validacion de hipotesis

| Campo | Valor |
|---|---|
| Hipotesis original (del brief) | "[hipotesis]" |
| Resultado | Confirmada / Refutada / Ajustada |
| Justificacion | [evidencia que soporta el resultado] |
| Incertidumbre residual | [que no se pudo confirmar y por que] |

---

## Sintesis Minto (borrador para ship)

**Situacion:** [1-2 lineas de contexto conocido]

**Complicacion:** [brecha cuantificada]

**Respuesta:** [recomendacion principal — 1 oracion]

**Argumentos de soporte:**
1. [hallazgo cuantificado con fuente]
2. [hallazgo cuantificado con fuente]
3. [hallazgo cuantificado con fuente — si aplica]

---

## Estado final

**APROBADA** — Sintesis coherente, hipotesis respondida, todos los campos Paso 3.5 completos.

**APROBADA CON OBSERVACIONES** — Puede avanzar a ship pero se debe declarar [observacion X] como limitacion.

**BLOQUEADA** — Requiere complemento de [agente X] antes de sintetizar. Motivo: [descripcion].
```

## Restricciones

- Si cualquier ENTREGA tiene un campo obligatorio de Paso 3.5 ausente: solicitar complemento al agente antes de incluirlo en la sintesis; no inferir ni completar
- Una inconsistencia en cifras entre dos agentes para el mismo periodo y area es siempre bloqueante: no se puede presentar al usuario sin aclaracion
- La hipotesis del brief debe quedar respondida (confirmada, refutada o ajustada con evidencia); si los datos no alcanzan para responderla: declararlo, no forzar una conclusion
- El informe de revision interna no es el entregable final: es insumo para `ship`
- Nunca usar jerga tecnica en la sintesis Minto: si un termino requiere explicacion para un subgerente forestal, reemplazarlo
- Precision honesta: si hay incertidumbre en una cifra, indicar rango o fuente de la estimacion; nunca presentar precision falsa
