# Skill: plan — Plan de delegacion por agente

> **Agente:** Orquestador — Subgerente de Mejora Continua

## Proposito

Traducir el brief estrategico aprobado en un plan de delegacion ejecutable: que agente hace que, en que orden (paralelo o secuencial), con que insumos, con que contexto estrategico y con que criterios de calidad. Produce los bloques `TAREA PARA [AGENTE]:` listos para enviar.

## Cuando usar

- Brief estrategico (`spec`) en estado APROBADO
- Siempre que haya mas de un agente involucrado o que la secuencia importe
- Cuando el usuario necesita visibilidad del plan antes de ejecutar
- Al retomar una iniciativa pausada para verificar que los insumos siguen vigentes

**Prerequisito:** `orquestador/skills/spec/SKILL.md` ejecutado con brief en estado APROBADO. Sin brief aprobado, cualquier delegacion esta basada en supuestos no validados.

## Protocolo

### Paso 1 — Determinar el patron de orquestacion

Elegir el patron que corresponde al brief:

| Patron | Cuando aplica | Ejemplo operacional |
|---|---|---|
| **Unico agente** | 1 area, causa clara, sin dependencias | Analisis de fallas en equipo especifico → solo IA |
| **Paralelo puro** | Areas independientes, no se necesitan entre si | EO (KPIs) + TD (telemetria) al mismo tiempo |
| **Secuencial** | Cada agente necesita el output del anterior | IA (historico) → EO (plan Lean con los datos) |
| **Paralelo + convergencia** | Primero paralelo, luego sintesis del Orquestador | EO + IA en paralelo → Orquestador integra → TD implementa |
| **Reactivo con DA** | Hay archivo de datos sin procesar | DA primero → luego el agente que usa esos datos |

El Orquestador nunca ejecuta analisis de datos directamente: delega en el agente correcto.

### Paso 2 — Definir insumos por agente

Para cada agente involucrado, verificar que los insumos existen antes de incluirlos en la tarea:

| Insumo | Agente receptor | Existe en `datos/` | Observacion |
|---|---|---|---|
| [archivo / tabla / output de otro agente] | [EO / TD / IA / DA] | SI / NO | [riesgo o condicion] |

Si un insumo no existe aun (depende de otro agente): marcarlo como "disponible tras output de [agente X]" y reflejarlo en la secuencia.

### Paso 3 — Redactar los bloques de delegacion

Un bloque por agente. Usar la estructura exacta del protocolo de orquestacion:

```
TAREA PARA [AGENTE]:
Contexto estrategico: [por que importa para Arauco — impacto en EBITDA / OEE / costo logistico]
Hipotesis a validar: [que esperamos encontrar — debe ser falseable]
Objetivo: [que debe producir el agente — verbo + resultado especifico]
Insumos disponibles: [datos/YYYY-MM-DD_archivo.ext / arauco_mc.db tabla X / output de agente Y]
Entregable esperado: [formato + nombre de archivo + seccion clave]
Criterio de calidad: [que hace util y accionable el output — campos obligatorios del Paso 3.5]
Plazo: inmediato / iteracion siguiente / [fecha]
```

### Paso 4 — Establecer la secuencia y dependencias

Representar en texto plano el flujo:

```
FASE 1 — PARALELO:
  [Agente A]: [tarea A]
  [Agente B]: [tarea B]

FASE 2 — SECUENCIAL (requiere outputs de Fase 1):
  [Agente C]: [tarea C — insumos: output A + output B]

FASE 3 — ORQUESTADOR:
  Integrar outputs A + B + C → entregable final [nombre]
```

Si hay un solo agente: no hace falta numeracion de fases.

### Paso 5 — Definir criterios de aceptacion por agente (Paso 3.5)

Antes de que cada ENTREGA se acepte como valida, verificar:

| Agente | Campos obligatorios en la ENTREGA | Señal de alerta |
|---|---|---|
| EO | Hallazgos clave + Causa raiz + Limitaciones + Plan de accion | Causa raiz ausente o plan sin responsable |
| TD | Estado + Dependencias + Limitaciones + Impacto esperado | Estado "en desarrollo" sin plazo ni bloqueador |
| IA | Hallazgos clave + Limitaciones + Impacto esperado | Limitaciones vacias o confianza no declarada |
| DA | Fuente del archivo + Caveats de muestra | Cifras sin origen o sin indicar total de registros |

Incluir estos criterios en el campo "Criterio de calidad" de cada bloque de delegacion.

### Paso 6 — Guardar el plan

```
datos/YYYY-MM-DD_plan-orq-[area]-[tipo].md
```

## Plantilla de Plan de Delegacion

```markdown
# Plan de Delegacion — [Titulo de la iniciativa]

**Fecha:** YYYY-MM-DD
**Brief de referencia:** datos/YYYY-MM-DD_spec-orq-[area]-[tipo].md
**Patron de orquestacion:** [Unico / Paralelo puro / Secuencial / Paralelo+convergencia / Reactivo DA]
**Estado:** BORRADOR | ACTIVO | COMPLETADO

---

## Resumen ejecutivo del plan

| Campo | Valor |
|---|---|
| Hipotesis a validar | [del brief — 1 linea] |
| Agentes activos | [lista: EO / TD / IA / DA] |
| Fases | [N fases] |
| Entregable final | [nombre del archivo y formato] |
| Plazo total estimado | [inmediato / N iteraciones / [fecha]] |

---

## Fases y dependencias

### FASE 1 — [PARALELO / SECUENCIAL]

**Condicion de inicio:** [brief aprobado / output de fase anterior / archivo en datos/]

[Bloque de delegacion por agente en esta fase]

---

### FASE 2 — [PARALELO / SECUENCIAL] (si aplica)

**Condicion de inicio:** outputs de Fase 1 recibidos y validados por Paso 3.5

[Bloque de delegacion]

---

### FASE FINAL — ORQUESTADOR

**Condicion de inicio:** todos los outputs validados
**Accion:** ejecutar `review` y luego `ship`

---

## Bloques de delegacion

---

TAREA PARA EO:
Contexto estrategico: [impacto en OEE / perdidas / proceso — cuantificado si es posible]
Hipotesis a validar: [lo que EO debe confirmar o refutar]
Objetivo: [verbo + resultado: "Identificar causa raiz de X y proponer plan Lean con responsable y plazo"]
Insumos disponibles: [datos/YYYY-MM-DD_archivo.ext / arauco_mc.db / output IA si aplica]
Entregable esperado: datos/YYYY-MM-DD_[tipo]-[descripcion].md — incluir hallazgos, causa raiz, plan
Criterio de calidad: causa raiz con evidencia + plan de accion con responsable y plazo verificable + limitaciones declaradas
Plazo: inmediato / iteracion siguiente

---

TAREA PARA TD:
Contexto estrategico: [que habilita digitalmente esta iniciativa — visibilidad, automatizacion, telemetria]
Hipotesis a validar: [estado de la integracion o sistema que TD debe diagnosticar]
Objetivo: [verbo + resultado: "Evaluar disponibilidad de datos en Forest Data 2.0 para X y proponer arquitectura de integracion"]
Insumos disponibles: [datos/YYYY-MM-DD_archivo.ext / BPMN TO-BE de EO si aplica]
Entregable esperado: datos/YYYY-MM-DD_[tipo]-[descripcion].md — incluir estado, dependencias, impacto
Criterio de calidad: estado actual confirmado (no supuesto) + dependencias TI identificadas + limitaciones tecnicas declaradas
Plazo: inmediato / iteracion siguiente

---

TAREA PARA IA:
Contexto estrategico: [que insight de datos soporta la decision de negocio]
Hipotesis a validar: [patron o tendencia que IA debe buscar en los datos historicos]
Objetivo: [verbo + resultado: "Analizar historico ON/OFF de equipo X en periodo Y e identificar patrones de falla"]
Insumos disponibles: [arauco_mc.db tabla X / datos/YYYY-MM-DD_archivo.ext]
Entregable esperado: datos/YYYY-MM-DD_analisis-[descripcion].md — hallazgos con cifras, limitaciones, impacto
Criterio de calidad: hallazgos cuantificados con fuente + limitaciones del modelo o muestra declaradas + impacto estimado en lenguaje de negocio
Plazo: inmediato / iteracion siguiente

---

TAREA PARA DA:
Contexto estrategico: [por que se necesita este archivo procesado — que decision informa]
Objetivo: Leer y estructurar datos del archivo indicado para consumo de [agente receptor]
Insumos disponibles: datos/YYYY-MM-DD_archivo.xlsx (o .pdf / .docx)
Entregable esperado: resumen estructurado con fuente declarada, total de registros y caveats de muestra
Criterio de calidad: origen del archivo explicitado + caveats de calidad de datos declarados + cifras sin interpretacion (DA no analiza, extrae)
Plazo: inmediato

---

## Riesgos del plan

| ID | Riesgo | Probabilidad (1-3) | Impacto (1-3) | Score | Contingencia |
|---|---|---|---|---|---|
| R1 | Datos SGL insuficientes para el periodo solicitado | 2 | 3 | 6 | Solicitar exportacion SAP PM como respaldo antes de iniciar |
| R2 | Output de agente X llega incompleto (Paso 3.5 no pasa) | 2 | 2 | 4 | Solicitar complemento al agente antes de avanzar a fase siguiente |
| R3 | Insumo clave no existe en `datos/` | 1 | 3 | 3 | Escalar al usuario con pregunta unica antes de activar agentes |
```

## Restricciones

- No activar ningun agente sin brief en estado APROBADO
- Las dependencias entre agentes son obligatorias: si EO necesita el output de IA, EO no puede empezar hasta que IA entregue
- Los insumos declarados en cada bloque deben existir verificados; no poner "datos probablemente en `datos/`"
- Criterio de calidad en cada bloque debe incluir los campos del Paso 3.5 correspondientes al agente receptor
- Si un agente devuelve una ENTREGA que no pasa el Paso 3.5: solicitar complemento antes de avanzar; no inferir ni completar por cuenta propia
- No comprometer plazos sin confirmar disponibilidad de datos: un plan con insumos faltantes tiene plazo BLOQUEADO
- El Orquestador no ejecuta analisis de datos ni codifica: delega en el agente correcto y coordina
