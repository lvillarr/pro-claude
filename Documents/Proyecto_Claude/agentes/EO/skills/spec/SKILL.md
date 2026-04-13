# Skill: spec — Especificación de Iniciativa de Mejora

## Propósito

Definir con precisión el problema operacional o la oportunidad de mejora antes de planificar o ejecutar. Produce un documento de especificación que alinea al equipo sobre qué se va a mejorar, por qué, y cómo se sabrá que se logró. Evita iniciar proyectos sobre hipótesis no validadas.

---

## Cuándo usar este skill

- El orquestador asigna una nueva oportunidad de mejora o iniciativa de EO
- Se detecta una pérdida recurrente en el SGL sin causa raíz definida
- Se solicita rediseñar un proceso forestal sin levantamiento previo
- Se necesita alinear a stakeholders antes de asignar recursos a un proyecto

---

## Protocolo de ejecución

### Paso 1 — Contextualizar la pérdida operacional
Responder antes de escribir una línea:
- ¿En qué proceso, equipo o línea ocurre el problema?
- ¿Desde cuándo se registra? ¿Con qué frecuencia?
- ¿Qué datos del SGL, SAP PM o Historian sustentan la magnitud?
- ¿Se ha observado en terreno (GEMBA) o solo en registros?

### Paso 2 — Definir el problema con estructura A3
```
Situación actual:  [descripción cuantificada del estado actual]
Situación deseada: [estado objetivo con métrica concreta]
Brecha:            [diferencia medible entre ambos]
```

### Paso 3 — Identificar stakeholders y alcance
- ¿Qué áreas y roles están involucrados?
- ¿Qué sistemas digitales están en el alcance (SGL, SAP, Planex)?
- ¿Qué queda explícitamente fuera del alcance?

### Paso 4 — Definir KPIs de éxito
Para cada KPI de éxito incluir:

| KPI | Fórmula | Línea base | Meta | Frecuencia | Fuente | Responsable |
|---|---|---|---|---|---|---|

### Paso 5 — Validar hipótesis de causa raíz
- Hipótesis principal (a confirmar con análisis posterior)
- Datos o evidencia que la sustentan
- ¿Se necesita GEMBA adicional antes de planificar?

### Paso 6 — Entregar documento de especificación
Guardar como:
```
datos/YYYY-MM-DD_spec-[nombre-iniciativa].md
```

---

## Plantilla de especificación

```markdown
# Especificación de Iniciativa de Mejora
**Fecha:** YYYY-MM-DD
**Área:** Excelencia Operacional
**Iniciativa:** [Nombre corto de la iniciativa]
**Solicitante / Orquestador:** [Nombre o sistema]

---

## 1. Contexto operacional
[Descripción del proceso forestal afectado: cosecha, transporte, planta, etc.]

## 2. Definición del problema (A3)
| | |
|---|---|
| **Situación actual** | [cuantificada con dato real] |
| **Situación deseada** | [métrica objetivo] |
| **Brecha** | [diferencia medible] |
| **Impacto económico estimado** | [CLP/hora, m³ perdidos, % OEE, etc.] |

## 3. Alcance
**Incluye:**
- [proceso / equipo / área]

**Excluye:**
- [lo que NO se abordará en esta iniciativa]

**Sistemas en scope:** SGL / SAP PM / Historian / Planex / otro

## 4. Stakeholders
| Rol | Nombre | Responsabilidad en la iniciativa |
|---|---|---|

## 5. KPIs de éxito
| KPI | Fórmula | Línea base | Meta | Frecuencia | Fuente | Responsable |
|---|---|---|---|---|---|---|

## 6. Hipótesis de causa raíz
[Hipótesis principal con evidencia disponible]

**¿Requiere GEMBA adicional?** Sí / No — [justificación]

## 7. Restricciones y supuestos
- [Restricción 1: presupuesto, plazo, disponibilidad de equipos]
- [Supuesto 1: disponibilidad de datos en SGL desde fecha X]

## 8. Criterio de inicio del plan
Esta especificación está lista para planificar cuando:
- [ ] Problema validado con datos reales
- [ ] KPIs de éxito acordados con stakeholders
- [ ] Causa raíz hipotética confirmada o GEMBA realizado
```

---

## Restricciones de este skill

- No se puede avanzar al skill `plan` sin KPIs de éxito definidos con fórmula y fuente
- No se asume causa raíz sin evidencia de terreno o datos del SGL
- El alcance debe ser explícito: qué incluye y qué excluye
- Toda magnitud del problema debe tener número real (no "varios", no "frecuente")
