# Skill: plan — Plan de Delegación (Orquestador)

## Propósito

Traducir el mandato de la especificación en instrucciones precisas de delegación a cada agente: qué debe hacer, con qué insumos, qué debe entregar y cuándo. Es el puente entre el problema de negocio y la ejecución de los agentes especializados.

---

## Cuándo usar este skill

- El skill `spec` fue completado con mandato y agentes identificados
- Se necesita redactar las instrucciones de delegación antes de lanzar los agentes
- La iniciativa involucra coordinación entre más de un agente con dependencias

**El orquestador planifica quién hace qué, no cómo se hace.**

---

## Protocolo de ejecución

### Paso 1 — Revisar el mandato
Leer `datos/YYYY-MM-DD_spec-orq-[iniciativa].md` y confirmar:
- Agentes involucrados y sus roles
- Secuencia: ¿paralelo o serial?
- Datos disponibles y gaps

### Paso 2 — Redactar instrucciones de delegación por agente

Usar el formato estándar para cada agente:
```
TAREA PARA [AGENTE — EO / IA / TD]:

Contexto estratégico:
[Por qué importa esta tarea para Arauco en 2-3 líneas. El agente necesita entender el "para qué".]

Hipótesis a validar:
[Qué esperamos que el agente encuentre o produzca.]

Objetivo:
[Qué debe producir. Ser específico: no "un análisis" sino "una tabla de KPIs con fórmula, fuente y meta".]

Insumos disponibles:
- datos/YYYY-MM-DD_[archivo].ext
- arauco_mc.db → tabla [nombre]

Entregable esperado:
[Nombre exacto del archivo de salida y formato: datos/YYYY-MM-DD_descripcion.ext]

Criterio de calidad:
[Qué hace que el output sea útil: completitud, formato, nivel de detalle, métricas incluidas.]

Plazo: inmediato / iteración siguiente
```

### Paso 3 — Definir dependencias entre agentes

```
Secuencia A (serial):
EO (diagnóstico AS-IS) → IA (análisis de datos) → TD (arquitectura digital) → Orquestador (síntesis)

Secuencia B (paralelo):
IA + TD trabajan simultáneamente → Orquestador espera ambas entregas → síntesis ejecutiva

Secuencia C (híbrida):
EO primero → IA + TD en paralelo con output de EO → Orquestador consolida
```

### Paso 4 — Definir protocolo de consolidación
Cuando los agentes entreguen:
- ¿Cómo se integran los outputs? (tabla comparativa, síntesis narrativa, mapa de calor)
- ¿Qué hacer si hay inconsistencias entre agentes?
- ¿Qué formato tiene el entregable final para el usuario?

### Paso 5 — Entregar plan de delegación
```
datos/YYYY-MM-DD_plan-orq-[nombre-iniciativa].md
```

---

## Plantilla de plan de delegación

```markdown
# Plan de Delegación — [Nombre Iniciativa]
**Fecha:** YYYY-MM-DD | **Orquestador:** Subgerente Mejora Continua

---

## Secuencia de delegación
**Tipo:** Serial / Paralelo / Híbrido
```
[diagrama de flujo textual: EO → IA+TD → Orquestador]
```

---

## Instrucciones por agente

### TAREA PARA EO
**Contexto estratégico:** [...]
**Hipótesis a validar:** [...]
**Objetivo:** [...]
**Insumos:** [...]
**Entregable:** datos/YYYY-MM-DD_[nombre].md
**Criterio de calidad:** [...]
**Plazo:** [...]

### TAREA PARA IA
[misma estructura]

### TAREA PARA TD
[misma estructura]

---

## Protocolo de consolidación
**Cuando llegan los outputs:**
1. Leer [archivo EO] → extraer [qué]
2. Leer [archivo IA] → extraer [qué]
3. Leer [archivo TD] → extraer [qué]
4. Integrar en [formato] con estructura: situación → hallazgos → recomendaciones → próximos pasos

**Si hay inconsistencias entre agentes:** [protocolo de resolución]

---

## Entregable final para el usuario
**Formato:** [informe ejecutivo / presentación / plan de acción]
**Archivo:** datos/YYYY-MM-DD_[descripcion-final].[ext]
```

---

## Restricciones de este skill

- Las instrucciones de delegación deben ser autocontenidas: el agente no tiene contexto de la conversación
- Cada tarea debe especificar el nombre exacto del archivo de salida esperado
- No lanzar agentes en paralelo si el output de uno alimenta la tarea del otro
- El criterio de calidad en cada tarea previene que el agente entregue outputs incompletos
